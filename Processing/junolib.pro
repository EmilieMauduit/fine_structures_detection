;+
; :Description:
;    returns data file header
;
; :Params:
;    file: data file
;
;-

function junoHeader, file

  OpenR, lun, /GET_LUN, file
  sz=0ul
  stream_10G=0ul
  readu, lun, sz, stream_10G

; stream_10g=1 spectre, =2 wave  
  if stream_10g EQ 1 then begin
    nbchan=0ul
    acc=0ul
    bw=0.0
    fech=0.0
    f0=0.0
    dt=0.0
    nfreq=0uL
    ; read nfreq value
    readu, lun, nbchan, acc,bw,fech,f0,dt, nfreq
    desc={$
      size:0ul, $         ; nbre d'octets en entete du fichier
      stream_10G:0ul,$    ; 1-spectres, 2-waves
      nbchan:0ul, $       ; nombre de canaux
      acc:0ul, $          ; facteur d'accumulation
      bw:0.0,$            ; largeur de bande, en MHz
      fech:0.0,$          ; facteur d'echantillonnage, en MHz
      f0:0.0,$            ; frequence centrale
      dt:0.0,$            ; temps d'integration, en millisecondes
      nfreq:0uL, $        ; nbre de frequences
      freq:fltarr(nfreq)$  ; liste des frequences
    }
  endif else begin
    desc={$
      size:0ul, $         ; nbre d'octets en entete du fichier
      stream_10G:0ul,$    ; 1-spectres, 2-waves
      bw:0.0,$            ; largeur de bande, en MHz
      fech:0.0,$          ; facteur d'echantillonnage, en MHz
      f0:0.0 $             ; frequence centrale
    }
  endelse  
  
; read header
  point_lun, lun, 0L
  readu, lun, desc
  close, lun
  free_lun, lun
  return, desc
  
end

;+
; :Description:
;    Appends a string in a file
;
; :Params:
;    log: Log file
;    s: string
;
;-

PRO junoWriteLog, log, s
  openw, unit,log,/append,/get_lun
  printf, unit, s
  close, unit
  free_lun, unit
  return
end

;+
; :Description:
;    Returns the name of the log file
;
; :Params:
;    file: data file
;
;-

Function JunoLog, file
  datej=bin_date(systime())
  str_date=string(format='(i4.4,i2.2,i2.2)',datej[0:2])
  return,file_dirname(file)+path_sep()+file_basename(file,'dat')+'log'
end

;+
; :Description:
;    Copies the log file to /data_dam/web/temps_reel/juno/Log/observations/
;
; :Params:
;    file: data file
;
;-

pro junoCopyLog, file, log=log
  log=JunoLog(file)
  if keyword_set(log) then begin
    log=JunoLog(file)
    junoWriteLog, log, ''
    junoWriteLog, log, 'junoCopyLog: copy '+Log+' to //datadam/web/temps_reel/juno/Log/observations/'  
  endif
  s = "scp "+log+" damobs@datadam:/data_dam/web/temps_reel/juno/Log/observations/";
  spawn, s
  return
end

;+
; :Description:
;   Remove the raw file 
;
; :Params:
;    file: data file
;
;-

pro junoRemove, file
  log=JunoLog(file)
  junoWriteLog, log, ''
  junoWriteLog, log, 'junoRemove: remove '+file
  s = "rm -f "+file;
  spawn, s
  return
end

;+
; :Description:
;    Returns the most recent file
;
; :Params:
;    path: data file path
;
;-

function junoGetLastFileName
  file=''
  liste=file_basename([file_search('/data1/*.dat'),file_search('/data2/*.dat')]) 
  if N_elements(liste) GT 0 then begin
    liste=liste[sort(liste)]
    file1=liste[n_elements(liste)-1]
    if (file_test('/data1/'+file1) EQ 1) then begin
      file='/data1/'+file1
    endif else file='/data2/'+file1
  endif
  return, file
end

;+
; :Description:
;    size format (octets/Mo/Go/To)
;
; :Params:
;    sz:size, in octets
;
;-

function affiche_sz, sz
  s=strcompress(string(FORMAT ='(F7.2)',sz))+' octets'
  sz=sz/1024.0
  if sz GT 1024.0 then begin
    sz=sz/1024.0
    if sz GT 1024.0 then begin
      sz=sz/1024.0
      if sz GT 1024.0 then begin
        sz=sz/1024.0
        s=strcompress(string(FORMAT ='(F7.2)',sz))+' To'        
      endif else begin
        s=strcompress(string(FORMAT ='(F7.2)',sz))+' Go'
      endelse
    endif else begin
      s=strcompress(string(FORMAT ='(F7.2)',sz))+' Mo'
    endelse
  endif else begin
     s=strcompress(string(FORMAT ='(F7.2)',sz))+' Ko'
  endelse
  return, s
end

;+
; :Description:
;    Convert Juno date format to Julian date.
;    WARNING: it is the date of the end of the spectrum.
;
; :Params:
;    date: 'DATE' field 
;    
;-

function JunoDate, date
  return, double(date.ijd) + date.isec/86400d0 + date.nsub/(date.dsub*86400d0)
end

function JunoWaveDate, d
  return, double(d[0]) + d[1]/86400d0 + (d[2]/ 2E8)/86400d0
end

function junoWaveDiffDate, d1, d2, fe
  offset = long(d2[0]-d1[0]) * 86400L+long(d2[1]-d1[1])
  return, offset*Fe+long(d2[2]-d1[2])
end

;+
; :Description:
;    display header description of the file
;
; :Params:
;    file: data file
;    desc: structure header
;    repli: replicate number
;
;-

pro JunoVerb, file, desc, repli, LOG=LOG

  ; Taille du fichier
  stat=fstat(desc.lun)
  s=affiche_sz(stat.size)
  print, ' '
  print, 'File description:'
  print,   '--File:         ', file
  print,   '--File size:    ', s, FORMAT='(a,a)'
  print,   "--size of the Header:       ", desc.size, ' octets',FORMAT='(a,i-8, a)'
  case desc.stream_10G of
    0: print,   "--data: Nothing"
    1: print,   "--data: Spectrum"
    2: print,   "--data: Wave"
  end
  fmt = '(a, C(CYI4.4,''-'',CMOI2.2,''-'',CDI2.2,1x,CHI2.2,'':'',CMI2.2,'':'',CSF09.6))'
  if desc.nbcubes GT 0 then begin
    print, '--start time:        ', desc.jd1, FORMAT=fmt
    print, '--stop  time:          ', desc.jd2, FORMAT=fmt
    print, '--duration (min):  ', (desc.jd2-desc.jd1)*86400.0/60.0
  endif
  print, '--dt (msec):    ', desc.dt, FORMAT='(a,f12.6)'
  print, '--accumulation: ', desc.acc, FORMAT='(a,i-8)'
  print, '--number of channels:       ', desc.nbchan, FORMAT='(a,i-8)'
  print, '--number of cubes:     ', desc.nbcubes, FORMAT='(a,i-8)'
  if repli ne 0 then print, '--replicate by:     ', repli, FORMAT='(a,i-8)'
  print, '--number of frequencies:           ', desc.nfreq
  print, '--central freq (MHz):    ', desc.f0, FORMAT='(a,f6.2)'
  print, '--freq echantillon (MHz): ', desc.fech, FORMAT='(a,f6.2)'
  print, '--Bandwidth (MHz): ', desc.bw, FORMAT='(a,f6.2)'
  print, '--first frequency (MHz):       ', desc.freq[0], FORMAT='(a,f6.2)'
  print, '--last frequency (MHz):       ', desc.freq[desc.nfreq-1], FORMAT='(a,f6.2)'

  if keyword_set(LOG) then begin
    log=file_dirname(file)+path_sep()+file_basename(file,'dat')+'txt'
    file_delete, log, /ALLOW_NONEXISTENT
    junoWriteLog, log, ' '
    junoWriteLog, log, '===================================================='
    junoWriteLog, log,        'File description:'
    junoWriteLog, log, '===================================================='
    junoWriteLog, log,        '--File:                   '+file
    junoWriteLog, log, string('--File size:              ',s, FORMAT='(a,a)')
    junoWriteLog, log, string("--size of the Header:     ",desc.size, ' octets',FORMAT='(a,i-8, a)')
    case desc.stream_10G of
      0: junoWriteLog, log,   "--data:                   Nothing"
      1: junoWriteLog, log,   "--data:                   Spectrum"
      2: junoWriteLog, log,   "--data:                   Wave"
    end
    if desc.nbcubes GT 0 then begin
      junoWriteLog, log, string('--start time:             ',desc.jd1, FORMAT=fmt)
      junoWriteLog, log, string('--stop  time:             ',desc.jd2, FORMAT=fmt)
      junoWriteLog, log, string('--duration (min):         ',(desc.jd2-desc.jd1)*86400.0/60.0)
    endif
    junoWriteLog, log, string('--dt (msec):              ',desc.dt, FORMAT='(a,f12.6)')
    junoWriteLog, log, string('--accumulation:           ',desc.acc, FORMAT='(a,i-8)')
    junoWriteLog, log, string('--number of channels:     ',desc.nbchan, FORMAT='(a,i-8)')
    junoWriteLog, log, string('--number of cubes:        ',desc.nbcubes, FORMAT='(a,i-8)')
    junoWriteLog, log, string('--number of frequencies:  ',desc.nfreq, FORMAT='(a,i-8)')
    junoWriteLog, log, string('--central freq (MHz):     ',desc.f0, FORMAT='(a,f6.2)')
    junoWriteLog, log, string('--freq echantillon (MHz): ',desc.fech, FORMAT='(a,f6.2)')
    junoWriteLog, log, string('--Bandwidth (MHz):        ',desc.bw, FORMAT='(a,f6.2)')
    junoWriteLog, log, string('--first frequency (MHz):  ',desc.freq[0], FORMAT='(a,f6.2)')
    junoWriteLog, log, string('--last frequency (MHz):   ',desc.freq[desc.nfreq-1], FORMAT='(a,f6.2)')
  endif
end


;+
; :Description:
;    search the beginning of data
;
; :Params:
;    file: file path.
;
;-

function junoGetPosFirstCube, file

  desc=junoHeader(file)
  if desc.stream_10G EQ 1 then begin
    cube_size= 8uL+desc.nbchan*(desc.nfreq+2)
    magic_word='7F800000'xul
  endif else begin
    cube_size= 2048L    
    magic_word='FF800000'xul
  endelse  
  data=ulonarr(cube_size) 
  
  openr, lun, file, /Get_Lun
  point_lun, lun, desc.size
  readu, lun, data
  close, lun
  free_lun, lun
  
; search magic word 
  ind=where(data EQ magic_word, count)
  if count LT 1 then begin
    ptr0=-1L
  endif else begin
    ptr0=desc.size+ind[0]*4uL
  endelse

  return, ptr0
end

;+
; :Description:
;    Open a juno file and create associated variable
;    for manipulating the data.
;
; :Params:
;    file: file path.
;    desc: data descriptor.
;
; :Keywords:
;   MULTI:   merging several cubes in each call of associated variable
;
;-

function junoOpen, file, desc, MULTI=multi
  compile_opt IDL2
  
; header structure
  desc1=junoHeader(file)
  
  if desc1.stream_10G NE 1 then begin
    return, {}
  endif

  eCube = {magic:0UL, id:0UL, $
      date:{iJD:0UL, iSec:0UL, nSub:0UL, dSub:0UL}, $
      undef0:0UL, undef1:0UL, $
      corr:replicate({magic:0UL, no:0UL, data:fltarr(desc1.nfreq)},desc1.nbchan) }

; a = associated variable
  ptr0=junoGetPosFirstCube(file)
  OpenR, lun, /GET_LUN, file
  a = Assoc(lun, eCube, ptr0)

; compute starting and ending dates of data
  jd1=0.0
  jd2=0.0
  nbcubes = ((fStat(lun)).Size - ptr0)/N_Tags(eCube, /LENGTH)-1L
  if nbcubes GT 0 then begin
    jd1 = junoDate((a[0]).date)
    jd2 = junoDate((a[nbcubes-1L]).date)
  endif
;"multi-cubes" for efficiency reason
if Keyword_Set(MULTI) then begin
  if multi GT nbcubes then multi=nbcubes
  eCube = replicate(eCube, multi)
  nbcubes /= Multi
  a = Assoc(lun, eCube, ptr0)
endif
desc={$
  lun:lun, $
  size:ptr0, $              ; nbre d'octets en entete du fichier
  stream_10G:desc1.stream_10G, $
  nbchan:desc1.nbchan, $    ; nombre de canaux
  acc:desc1.acc, $          ; facteur d'accumulation
  bw:desc1.bw,$             ; largeur de bande, en MHz
  fech:desc1.fech,$         ; facteur d'echantillonnage, en MHz
  f0:desc1.f0,$             ; frequence centrale
  dt:desc1.dt,$             ; temps d'integration, en millisecondes
  nfreq:desc1.nfreq,$       ; nbre de frequences
  freq:desc1.freq,$         ; liste des frequences, en MHz
  jd1:jd1, $                ; date julienne debut du fichier
  jd2:jd2, $                ; date julienne de fin du fichier
  nbcubes:nbcubes $         ; nombre de cubes dans le fichier
}

return, a

end

;+
; :Description:
;    description
;
; :Params:
;    file: data file
;
; :Keywords:
;   LOG:   write a log file
;
;-

pro junoDesc, file, LOG=LOG
  if n_params() EQ 0 then begin
    file= dialog_pickfile(PATH='\\datadam\data\juno\Current10G\', filter=['*.dat'],/MUST_EXIST, title='Select a data file')
    if (file EQ '') then begin
      error = DIALOG_MESSAGE(['No file '], /Error)
      RETURN
    endif
  endif
  a=junoOpen(file, desc)
  junoVerb, file, desc, 1, LOG=LOG
  close, desc.lun
  free_lun, desc.lun
  return
end

;+
; :Description:
;    Build a compressed Juno file from an original
;    one by averaging over a number of spectra and over a number of frequencies 
;    File header is updated.
;
; :Params:
;    file:  input file path.
;    jd_intervall: Julian date intervall.
;    secint: integration interval in milliseconds or number of spectra.
;    dfreq: frequency integration

; :Keywords:
;    fileout: output file name
;    FACT: if set, 'secint' is interpreted as a number of spectra.
;    ALL:  if set the entire data set is output.
;    VERBOSE:  control output messages.
;    COPYDATA: copy to \\datadam\data\juno\Current10G
;-

pro junoComp, file, jd_intervall, secint, dfreq, fileOut=FileOut, FACT=FACT, ALL=ALL, VERBOSE=verbose, COPYDATA=COPYDATA
  compile_opt IDL2
  on_error, 2
  
  Log = JunoLog(file)

  desc=junoHeader(file)
  
; wave data file
  if (desc.stream_10G EQ 2) then begin
    junoWriteLog, log, 'junoComp: wave File'
    return
  endif
  if keyword_set(fileOut) then begin
    fileOut=fileOut
  endif else begin
    fileOut=file_dirname(file)+path_sep()+file_basename(file,'.dat')+'_comp.dat'
  endelse
  
  junoWriteLog, log, 'junoComp: debut de la compression '+systime()
  junoWriteLog, log, 'junoComp: Outpout File= '+fileOut
      
  a = JunoOpen(file, desc)

  ; [debut, fin]
  fmt = '(a, C(CYI4.4,''-'',CMOI2.2,''-'',CDI2.2,1x,CHI2.2,'':'',CMI2.2,'':'',CSF09.6))'
  jd_inter=jd_intervall
  if keyword_set(ALL) then jd_intervall=[desc.jd1, desc.jd2]
  s=string('Extraction From ', jd_intervall[0], FORMAT=fmt)
  s=s+string(' To ', jd_intervall[1], FORMAT=fmt)
  junoWriteLog, log, 'junoComp: '+s
  print, 'junoComp: '+s

  ni = Keyword_Set(FACT) ? ulong(secint) : round(secint/desc.dt)
  close, desc.lun
  free_lun, desc.lun
  
  a = JunoOpen(file, desc, multi=ni)
  junoWriteLog, log, 'junoComp: integration over' + strcompress(string(ni)) + ' spectra ='+strcompress(string(ni*desc.dt)) + ' msec'
  junoWriteLog, log, 'junoComp: integration over' + strcompress(string(dfreq)) + ' frequencies'
  print, 'junoComp: integration over' + strcompress(string(ni)) + ' spectra ='+strcompress(string(ni*desc.dt)) + ' msec'
  print, 'junoComp: integration over' + strcompress(string(dfreq)) + ' frequencies'

  ;copy file header and frequency list to the output file
  OpenW, lun, /GET_LUN, fileOut
  ; calcul taille de l'entete
  sz=(9+desc.nfreq/dfreq)*4
  writeu, lun, sz               ; nbre d'octets en entete du fichier
  writeu, lun, desc.stream_10G  ; nbre d'octets en entete du fichier
  writeu, lun, desc.nbchan      ; nombre de canaux
  writeu, lun, desc.acc         ; facteur d'accumulation
  writeu, lun, desc.bw          ; largeur de bande, en MHz
  writeu, lun, desc.fech        ; facteur d'echantillonnage, en MHz
  writeu, lun, desc.f0          ; frequence centrale
  writeu, lun, desc.dt*ni       ; temps d'integration, en millisecondes
  writeu, lun, desc.nfreq/dfreq ; nbre de frequences
  if dfreq NE 1 then begin
    freq = mean(reform(desc.freq, dfreq, desc.nfreq/dfreq), DIM=1)
  endif else begin
    freq=desc.freq
  endelse
  writeu, lun, freq
   
; [no du ier cube a traiter, nombre de cubes a traiter]
  nn = (desc.nbcubes - 1)*(jd_intervall - desc.jd1)/(desc.jd2 - desc.jd1)
  nn[0] = floor(nn[0]) > 0 
  nn[1] = ceil(nn[1]) < (desc.nbcubes-1)
  if (nn[0] gt nn[1]) then return
  nn[1] -= nn[0]
  junoWriteLog, log, 'junoComp: Extraction of ' + strcompress(string(nn[1]))+' cubes from cube no' + strcompress(string(nn[0])) 
   
;do the compression
  if Keyword_Set(VERBOSE) then begin
    p = round(nn[1]*findgen(101)/100)
    k = 0
  endif
  
  CubeOut = {magic:0UL, id:0UL, date:{iJD:0UL, iSec:0UL, nSub:0UL, dSub:0UL}, undef0:0UL, undef1:0UL, $
             corr:replicate({magic:0UL, no:0UL, data:fltarr(desc.nfreq/dfreq)},desc.nbchan) }
  b = a[1+nn[0]]
  bb = b[-1]
  CubeOut.magic= bb.magic
  cubeOut.corr.magic=bb.corr.magic
  cubeOut.corr.no=bb.corr.no

  for i=1,nn[1] do begin
    
    b = a[i+nn[0]]
    bb = b[-1]
    
    CubeOut.id   = bb.id
    CubeOut.date = bb.date
 
    ; b.corr.data: FLOAT     = Array[freq, chan, integ]
        
    if ni EQ 1 then begin
      if dfreq EQ 1 then begin
        ; extraction sans compression
       CubeOut.corr = b.corr
      endif else begin
        ; extraction avec compression en frequences
        CubeOut.corr.data = mean(b.corr.data, DIM=3)
      endelse
    endif else begin
      if dfreq EQ 1 then begin
        ; extraction avec compression en temps
        CubeOut.corr.data = mean(b.corr.data, dim=1)
      endif else begin
        ; extraction avec compression en frequences et en temps
        CubeOut.corr.data = mean(reform(mean(b.corr.data, DIM=3), dfreq, N_elements(freq), 4), dim=1)
      endelse
    endelse
    
    writeu, lun, CubeOut

    
    if keyword_set(verbose) then begin
      if (i-1 eq p[k]) then print, k++, FORMAT='(i3,"%",$)'
    endif
  endfor
  
  junoWriteLog, log, '===================================================='
  junoWriteLog, log, 'junoComp: fin de la compression '+systime()
  junoWriteLog, log, '===================================================='
  
;close all files and exit
  close, desc.lun
  Free_Lun, desc.lun
  Free_lun, lun  
  
  junoCopyLog, file
  junoDesc, fileOut, LOG=LOG
  
  if keyword_set(COPYDATA) then juno_copycomp, file
  
  return
end

;+
; :Description:
;    copie du fichier comp
;
; :Params:
;    file:  input file path.
;    
;-

pro juno_copycomp, file


; Log file
  log=JunoLog(file)

; Comp File description
  fileOut=file_dirname(file)+path_sep()+file_basename(file,'.dat')+'_comp.dat'

  txt=file_dirname(fileOut)+path_sep()+file_basename(fileOut,'dat')+'txt'
  junoWriteLog, log, ''
  junoWriteLog, log, 'JunoComp: copy comp File to \\datadam\data\juno\Current10G'
  s = "/home/damobs/bin/rsync_juno datadam data "+file_basename(fileOut)+" "+log
  junoWriteLog, log, 'junoComp:  '+s
  
  openw, unit,"/home/damobs/tmp/copyFile",/get_lun
  printf, unit,"#!/bin/bash"
  printf, unit,"cat "+txt+" >> "+log
  printf, unit, s
  printf, unit, "rm -f "+txt
  printf, unit, "rm -f /home/damobs/tmp/copyFile"
  close, unit
  free_lun, unit

  return
end

;+
; :Description:
;    quick check of the data file
;    Returns: 0:bad spectre, 1: spectre OK, 3: bad start magic word (wave), 4: bad stop magic word (wave),  5: missing wave blocs, 2: wave file OK
;
; :Params:
;    file:  input file path.
;
;-

function junoQuickCheck, file

  fmt = '(a, C(CYI4.4,''-'',CMOI2.2,''-'',CDI2.2,1x,CHI2.2,'':'',CMI2.2,'':'',CSF09.6))'
  log = JunoLog(file)
  junoWriteLog, log, 'junoQuickCheck: File quick checking '+file

  desc=junoHeader(file)
  
; ptr: magic word (7F800000 = 2139095040) position  
  ptr=junoGetPosFirstCube(file)

; wave
  if (desc.stream_10G EQ 2) then begin
    junoWriteLog, log, 'junoQuickCheck: wave File'
    print, 'junoQuickCheck: wave File'
    if (ptr ne desc.size) then begin
      junoWriteLog, log, 'junoQuickCheck: start wave File error, ptr wait/read ='+strcompress(string(desc.size)+' '+string(ptr))
      print, 'junoQuickCheck: start wave File error, ptr wait/read =', strcompress(string(desc.size)+' '+string(ptr))
      return, 3
    endif
    wave_size = 2048L   
    data=ulonarr(wave_size)
    openr, lun, file, /get_lun
    nblocs = ((fStat(lun)).Size - ptr)/(N_Elements(data)*4uL)
    point_lun, lun, ptr
    readu, lun, data
    d0=data[1:3]
    jd0=JunoWaveDate(d0)
    s=string('', jd0, format=fmt)
    junoWriteLog, log, +'junoQuickCheck: '+s+' debut du fichier '
    print, 'junoQuickCheck: '+s+' debut du fichier'

    point_lun, lun, ptr+(nblocs-1)*wave_size*4L
    CMagic='FF800000'XUL
    readu, lun, data
    close, lun
    free_lun, lun
    if (data[0] ne CMagic) then begin
      junoWriteLog, log, 'junoQuickCheck: stop wave File error, bad magic word'
      print, 'junoQuickCheck: start wave File error, bad magic word'
      return, 4
    endif
    d1=data[1:3]
    jd1=JunoWaveDate(d1)
    s=string('', jd1, format=fmt)
    junoWriteLog, log, 'junoQuickCheck: '+s+' fin du fichier '
    print, 'junoQuickCheck: '+s+' fin du fichier'
    expected_blocs = (junoWaveDiffDate(d0,d1,desc.fech*1000000L) / (desc.fech/desc.bw) / 1022L) + 1L
    print, 'junoQuickCheck: blocs expected/read/missing = '+strcompress(string(long(expected_blocs))+'/'+string(nblocs)+'/'+string(long(expected_blocs-nblocs)))    
    junoWriteLog, log,  'junoQuickCheck: blocs expected/read/missing = '+strcompress(string(long(expected_blocs))+'/'+string(nblocs)+'/'+string(long(expected_blocs-nblocs)))
    missing_blocs = expected_blocs - nblocs
    if (missing_blocs  EQ 0 ) then begin
      print, "No error found."
      junoWriteLog, log,  'junoQuickCheck: No error found.'
      return, 2
    endif else begin
      print, "taux d'erreurs = "+string(100.0 * missing_blocs / expected_blocs)+'%'
      junoWriteLog, log,  'junoQuickCheck: taux d''erreurs = '+string(100.0 * missing_blocs / expected_blocs)+'%'
      return, 5
    endelse
  endif
; spectrum
  ret=0
  cube_size= 8uL+desc.nbchan*(desc.nfreq+2)
  data=ulonarr(cube_size)

  openr, lun, file, /get_lun
  point_lun, lun, ptr
  readu, lun, data
; start number
  no0=data[1]
; Start DateTime
  jd = double(data[2]) + data[3]/86400d0 + data[4]/(data[5]*86400d0)
  s=string('', jd, format=fmt)
  junoWriteLog, log, +'junoQuickCheck: '+s+' debut du fichier '
  print, 'junoQuickCheck: '+s+' debut du fichier'

  nbcubes = ((fStat(lun)).Size - ptr)/(N_Elements(data)*4uL)

; no data
  if nbcubes EQ 0 then begin
    junoWriteLog, log, 'junoQuickCheck: Pas de cube dans le fichier'
    print, 'junoQuickCheck: Pas de cube dans le fichier'
    close, lun
    free_lun, lun
    return, ret
  endif else begin
    junoWriteLog, log, 'junoQuickCheck: '+strcompress(string(nbcubes))+' cubes'
    print, 'junoQuickCheck: '+strcompress(string(nbcubes))+' cubes'
  endelse

  ; last cube position
  CMagic='7F800000'XUL
  point_lun, lun, (ptr+(nbcubes-1L)*cube_size*4L)
  readu, lun, data
  close, lun
  free_lun, lun
  if data[0] EQ CMagic then begin
    jd = double(data[2]) + data[3]/86400d0 + data[4]/(data[5]*86400d0)
    s=string('', jd, format=fmt)
    junoWriteLog, log, +'junoQuickCheck: '+s+' fin du fichier '
    print, 'junoQuickCheck: '+s+' fin du fichier'
    if no0+nbcubes-1L EQ data[1] then begin
      junoWriteLog, log, '===================================================='
      junoWriteLog, log, 'junoQuickCheck: verification terminee, pas d''erreur'
      junoWriteLog, log, '===================================================='
      print, 'junoQuickCheck: verification terminee, pas d''erreur'
      ret=1
    endif else begin
      junoWriteLog, log, 'junoQuickCheck: verification terminee, il manque '+strcompress(string(data[1]-no0-nbcubes+1L))+' cubes'
      print, 'junoQuickCheck: verification terminee, il manque '+strcompress(string(data[1]-no0-nbcubes+1L))+' cubes'
    endelse
  endif

  return, ret
end

;+
; :Description:
;    Juno file verification
;
; :Params:
;    file:  input file path.
;
; :Keywords:
;    VERBOSE:  control output messages.
;    COPYLOG: copy log to \\datadam\web\temps_reel\juno\Log\observations
;    
;-

Pro junoVerif, file, VERBOSE=VERBOSE, COPYLOG=COPYLOG

  if keyword_set(COPYLOG) then junoCopyLog, file
  
  ret=junoQuickCheck(file)
  if (ret EQ 1) or (ret GE 2) then begin
    if keyword_set(COPYLOG) then junoCopyLog, file
    return
  endif

  log = JunoLog(file)
  junoWriteLog, log, ''
  junoWriteLog, log, 'junoVerif: debut du controle: '+systime()
  junoWriteLog, log, 'junoVerif: Controle du fichier '+file

  desc=junoHeader(file)
  if (desc.stream_10G EQ 2) then begin
      junoWriteLog, log, 'junoVerif: wave File'
      return
  endif
  
; ptr: mot magique = 7F800000 = 2139095040
  ptr=junoGetPosFirstCube(file)
  cube_size= 8uL+desc.nbchan*(desc.nfreq+2)
  data=ulonarr(cube_size)
  
  openr, lun, file, /get_lun
  point_lun, lun, ptr
  readu, lun, data
  no=data[1]  
  no0=no
  junoWriteLog, log, 'junoVerif: il faut sauter '+strcompress(string(ptr))+' octets depuis le debut du fichier'
  print, 'junoVerif: il faut sauter '+strcompress(string(ptr))+' octets depuis le debut du fichier'
  
  fmt = '(a, C(CYI4.4,''-'',CMOI2.2,''-'',CDI2.2,1x,CHI2.2,'':'',CMI2.2,'':'',CSF09.6))'
  jd = double(data[2]) + data[3]/86400d0 + data[4]/(data[5]*86400d0)
  s=string('', jd, format=fmt)
  junoWriteLog, log, +'junoVerif: '+s+' debut du fichier '
  print, 'junoVerif: '+s+' debut du fichier'

; Pas de cube a traiter
  nbcubes = ((fStat(lun)).Size - ptr)/(N_Elements(data)*4uL)
  if nbcubes EQ 0 then begin
    junoWriteLog, log, 'junoVerif: Pas de cube dans le fichier'
    close, lun
    free_lun, lun
    if keyword_set(COPYLOG) then junoCopyLog, file
    return
  endif else begin
    junoWriteLog, log, 'junoVerif: '+strcompress(string(nbcubes))+' cubes a traiter'
  endelse

; calage au debut d'un bloc
  CMagic='7F800000'XUL
  sz=cube_size*4L
  
  p = round(nbcubes*findgen(101)/100)
  i = 0

  ; Compteur d'erreurs
  nberr=0L
  point_lun, lun, ptr
  k=0
  print, 'valeur du compteur initial = ',no
  junoWriteLog, log, 'junoVerif: compteur ier spectre= '+strcompress(string(no))
  mank=0L

  junoWriteLog, log, 'junoVerif:' 

  while ((fStat(lun)).Size - (fStat(lun)).cur_ptr) GE (N_Elements(data)*4uL) do begin
    readu, lun, data
    ind=where(data EQ '7F800000'xul, count)
    if not ((data[0] EQ CMagic)  and (data[1] EQ no ) and count EQ 1) then begin

      if count LT 1 then begin
        junoWriteLog, log, 'junoVerif: pas de mot magic dans le cube lu '+string(k)
        print, 'pas de mot magic dans le cube lu '+string(k)
        stop
      endif

      if count GT 1 then begin
        print,strcompress('cube '+string(k)+' '+string(count)+' mots magic, position='+string((ind[0])*4)+','+string((ind[1])*4)+', no '+$
        string(data[ind[0]+1])+','+string(data[ind[1]+1])+' saut= '+string(data[ind[1]+1]-data[ind[0]+1]))
        junoWriteLog, log, strcompress('junoVerif: cube '+string(k)+' '+string(count)+' mots magic, position='+string((ind[0])*4)+','+string((ind[1])*4)+',no '+$
        string(data[ind[0]+1])+','+string(data[ind[1]+1])+' saut= '+string(data[ind[1]+1]-data[ind[0]+1]))
      endif

      nberr=nberr+1L
      
      ; recalage sur le debut du dernier spectre
      offset=ind[count-1]*4uL
      stat=fstat(lun)
      ptr=stat.cur_ptr+offset-sz
      point_lun, lun, ptr
      readu, lun, data
      jd = double(data[2]) + data[3]/86400d0 + data[4]/(data[5]*86400d0)
      if mank EQ 0 then jd0=jd
      jd1=jd
      s=string('', jd, format=fmt)
      if count EQ 1 then begin
        print, 'cube '+strcompress(String(k)+' '+string(count)+' mot magic,  position='+string((ind[0])*4)+',no ' +$
          string(data[1])+' attendu= '+string(no)+' saut= '+string(data[1]-no)+' '+s)
        junoWriteLog, log, 'junoVerif: cube '+strcompress(String(k)+' '+string(count)+' mot magic,  position='+string((ind[0])*4)+',no ' +$
          string(data[1])+' attendu= '+string(no)+' saut= '+string(data[1]-no)+' '+s)
      endif
      mank=mank+data[1]-no
      no=data[1]  
    
    endif else begin
      
      jd = double(data[2]) + data[3]/86400d0 + data[4]/(data[5]*86400d0)
   
    endelse
    
    ; Message numero du bloc en cours de traitement
    if keyword_set(verbose) then begin
      if (k eq p[i]) then print, i++, FORMAT='(i3,"%",$)'
    endif
    ;
    no=no+1L
    k=k+1L
;  endfor
   endWhile
   
  close, lun
  jd = double(data[2]) + data[3]/86400d0 + data[4]/(data[5]*86400d0)
  s=string('', jd, format=fmt)
  junoWriteLog, log, +'junoVerif: '+s+' fin du fichier, cube  '+strcompress(string(k))
  if nberr EQ 0 then begin
    junoWriteLog, log, '===================================================='
    junoWriteLog, log, 'junoVerif: verification terminee, pas d''erreur'
    junoWriteLog, log, '===================================================='
  endif else begin
    junoWriteLog, log, 'junoVerif: verification terminee, il manque '+strcompress(string(mank))+ ' cubes ('+strcompress(string((jd1-jd0)*86400.0))+' secondes)'
  endelse
  junoWriteLog, log, 'junoVerif: Fin du controle: '+systime()
  
  if keyword_set(COPYLOG) then junoCopyLog, file
  return
end

;+
; :Description:
;    Juno file extraction from a param file
;
; :Params:
;    fparam:  param file .evt1 ou .evt2
;    4 fields:
;       filename
;       integration factor    
;       start Time   yyyy-mm-ddThh:nn:ss.cccZ
;       stopTime     yyyy-mm-ddThh:nn:ss.cccZ

; ex: /data/20160503_160343.dat 1 2016-05-03T16:40:01.000 2016-05-03T16:45:01.000 
;
;-

pro junoExtract, fparam, LOG=LOG

  if n_params() EQ 0 then begin
    print, 'il manque le nom du fichier parametre'
    return
  endif
  print, 'fichier parametres= ', fparam
  if file_test(fparam) NE 1 then begin
    print, 'fichier non trouve'
    return
  endif

  ; gets Lines number
  nlines = FILE_LINES(fparam)

  ; reading file
  sarr = STRARR(nlines)
  OPENR, unit, fparam,/GET_LUN
  READF, unit, sarr
  FREE_LUN, unit

  ;
  for k=0, nlines-1 do begin
    str=strcompress(sarr[k])
    if strcompress(str,/remove_all) EQ '' then continue
    if StrmId(str,0,1) NE ';' then begin
      s = strcompress(STRSPLIT(str,' ',/EXTRACT, count=count))
      if count EQ 4 then begin
        fileIn=strcompress(s[0], /remove_all)
        TIMESTAMPTOVALUES, s[2], YEAR=year, MONTH=month, DAY=day,HOUR=hour, MINUTE=minute, SECOND=second, OFFSET=offset
        jd0=JULDAY(Month, Day, Year, Hour, Minute, Second)
        TIMESTAMPTOVALUES, s[3], YEAR=year, MONTH=month, DAY=day,HOUR=hour, MINUTE=minute, SECOND=second, OFFSET=offset
        jd1=JULDAY(Month, Day, Year, Hour, Minute, Second)
        tag=fix(s[1])
        if tag EQ 2 then begin
          ; correction nom du fichier
          liste=file_search(fileIn)
          fileIn=liste[0] 
        endif
        
        ; creation arborescence yyyy/mm/ si besoin
        caldat, jd0,  M, D, Y, H, N, S  
        path=  file_dirname(fileIn)+path_sep()+'a_envoyer'+path_sep()+string(format='(I4.4)', Y)
        ret= FILE_SEARCH(path, /TEST_DIRECTORY)
        if ret[0] EQ '' then FILE_MKDIR, path         
        path=path+path_sep()+string(format='(I2.2)', M)
        ret= FILE_SEARCH(path, /TEST_DIRECTORY)
        if ret[0] EQ '' then FILE_MKDIR, path
         
        fileOut=  path+path_sep()+string(format='(I4.4,I2.2,I2.2,"_",I2.2,I2.2,I2.2,"_extract",i1.1,".dat")', Y,M,D,H,N,fix(S),tag)
        dfreq=1
        kint=1

        JunoComp, fileIn, [jd0, jd1], kint, dfreq, fileOut=fileOut, /FACT, /VERBOSE
      endif else begin
        print, 'bad arguments count'
      endelse
    endif
  endfor

; deplace les fichiers dans done
  if tag EQ 1 then begin
    file_move, fparam, file_dirname(fparam)+path_sep()+"done"+path_sep()+file_basename(fparam)
    fits=file_dirname(fparam)+path_sep()+file_basename(fparam,'.evt1')+'.fits'
    fmode=file_dirname(fparam)+path_sep()+file_basename(fparam,'.evt1')+'.mode'
    if file_test(fileIn) EQ 1 then file_move, fileIn, file_dirname(fileIn)+path_sep()+"done"+path_sep()+file_basename(fileIn)
    fich=file_dirname(fileIn)+path_sep()+file_basename(fileIn,'.dat')+'.log'
    if file_test(fich) EQ 1 then file_move, fich, file_dirname(fich)+path_sep()+"done"+path_sep()+file_basename(fich)
    fich=file_dirname(fileIn)+path_sep()+file_basename(fileIn,'.dat')+'.txt'
    if file_test(fich) EQ 1 then file_move, fich, file_dirname(fich)+path_sep()+"done"+path_sep()+file_basename(fich)   
  endif
  if tag EQ 2 then begin
    ; move fichier .evt2 dans Done
    file_move, fparam, file_dirname(fparam)+path_sep()+"done"+path_sep()+file_basename(fparam)
    fits=file_dirname(fparam)+path_sep()+file_basename(fparam,'.evt2')+'.fits'
    fmode=file_dirname(fparam)+path_sep()+file_basename(fparam,'.evt1')+'.mode'
    ; delete .dat
    file_delete, fileIn
    ; delete .log
    fich=file_dirname(fileIn)+path_sep()+file_basename(fileIn,'.dat')+'.log'
    if file_test(fich) EQ 1 then file_delete, fich    
  endif
  if file_test(fits) EQ 1 then file_move, fits, file_dirname(fits)+path_sep()+"done"+path_sep()+file_basename(fits)
  if file_test(fmode) EQ 1 then file_move, fmode, file_dirname(fmode)+path_sep()+"done"+path_sep()+file_basename(fmode)

return
end

;+
; :Description:
;    Traitement des fichiers parametres *.evt2 presents dans le repertoire /data2/a_traiter
;
;-

pro junoTag2, LOG=LOG
  liste=file_search('/data2/a_traiter/*.evt2', count=count)
  if count GT 0 then begin
    for k=0, count-1 do begin
      fparam=liste[k]
      junoExtract, fparam, LOG=LOG
    endfor
  endif  
return
end

;+
; :Description:
;     File reader example
;
;     ecube = {
;             magic:0UL,
;             id:0UL, $
;             date:{iJD:0UL, iSec:0UL, nSub:0UL, dSub:0UL}, $
;             undef0:0UL,
;             undef1:0UL, $
;             corr:replicate({magic:0UL, no:0UL, data:fltarr(desc.nfreq)},desc.nbchan) }
;     ecube = replicate(eCube, ni)
;     a = Assoc(lun, eCube, offset)
;
; :Params:
;    file: file path
;    ni: replicate number (ex : ni=2975)
;
; :Keywords:
;    VERBOSE:  control output messages.
;    
;-

pro junoRead, file, ni, VERBOSE=VERBOSE
  compile_opt IDL2
  on_error, 2

  if n_params() NE 2 then RETURN
  if file_test(file) NE 1 then return

; reading by ni spectra
  a = JunoOpen(file, desc, multi=ni)

; File description
  JunoVerb, file, desc, ni
  
; Traitement de ni spectres
;  pour affichage date: fmt = '(i4.4, " ",C(CYI4.4,''-'',CMOI2.2,''-'',CDI2.2,1x,CHI2.2,'':'',CMI2.2,'':'',CSF09.6))'
  if Keyword_Set(VERBOSE) then begin
    p = round(desc.nbcubes*findgen(101)/100)
    i = 0
  endif
  
  tic
  for k=0L, desc.nbcubes-1L do begin
    
    b=a[k]
    
    ; jd = double(ni)
    jd=junoDate(b[*].date)
    
    ; RG, RD = float(16384,ni)
    RG=b.corr[0].data
    RD=b.corr[3].data
    
    ; verif:
    ; print, k, jd[0], format=fmt
    ; tv, 10*alog10(rebin(RG,512, 2975/5))
    
    ;
    if keyword_set(verbose) then begin
      if (k-1 eq p[i]) then print, i++, FORMAT='(i3,"%",$)'
    endif
  endfor
  toc
  ;close file
  close, desc.lun
  Free_Lun, desc.lun
end

pro junolib
  
end