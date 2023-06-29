;+
;
; : Description:
; 
; Split a data file (containing a time-frequency dynamical spectrum) in frequency in bands of a chosen width then find the number of
; corresponding channels which is the most suitable and divide the file according to this number, ni. Some channels may be left aside, those 
; losses will be evaluated.
; Each of these frequency bands will be divided in squared panels of sizes ni*ni (we want to keep the time resolution). Those panels will then
; be integrated in frequency overt two different integers ni1 (3 and 7 here) in order to cover all the drifts we want to study. those ; integers are multiples of ni.
; Then each ni*ni/ni1 panel is divide in smaller ones of sizes (ni/ni1)*(ni/ni1). Traitement_junon.pro will then be applied to each one of 
; them and retrieve useful parameters for the study.
; At the begining, an 3D array is created, for each panel (ni/ni1)*(ni/ni1) it will contain all the informations about it.
; 
; :Uses:
;
; read_junon_data
; traitement_junon
; prep_ponderation
; plot_data
; junolib
; 
; :Parameters:
; 
; INPUT:
; 
;   folder : path of the folder containing the files to process
;   band : width of bands in frequency in which you want to split the spectra (in MHz)
;   dfrecouv : range over which wewant the bands to overlap in MHz
;   ni1: integration factor on which we want to integrate in frequency, determined by the keyword in traitement_massif.pro
;
; OUTPUT :
;
; A saveset containing the list of the read files, their size and the time it took to process them.
; And for each file, a saveset containing two arrays, one for each polarization of dimension (nbandes*(ncarres*ni1)*15) containing  all the 
; parameters about each panel.
;
; KEYWORDS :
;
;   nfstart : set to the index of the file you wanna start with (in case the run crashes), if not set the run starts with the first file of the folder
;
;-
;

pro junon_sampling_v2, folder, wband, ni1, nfstart=nfstart, nfstop=nfstop

  files = file_Search(folder+'/*extract2.dat',count=nfiles)
  restore, '/home/emauduit/lecture/tag2.sav'
  times=fltarr(nfiles)
  sizes=fltarr(nfiles)
  
  if keyword_set (nfstart) then nfstart=nfstart else nfstart=0
  if keyword_set (nfstop) then nfstop=nfstop else nfstop=nfiles-1

  for nf=nfstart,nfstop do begin

     tic, /profiler
     clock=tic()
     rien = JunoOpen(files[nf], desc)
     JunoVerb, files[nf], desc, 0
     stat=fstat(desc.lun)
     close, desc.lun
     free_lun, desc.lun
     sizes(nf)=((stat.size/1024.)/1024.)/1024. ; Size of thefile in Gb
     names=files[nf].split('/')
     path_file=files[nf]
     nf_plot=0  ;number of files containing plots
     nplot=0 ;number of plots for the current file

     header=junoHeader(files[nf])
     fmin=header.freq[0]
     fmax=header.freq[header.nfreq-1]

     if (fmin lt 8. ) then fmin=8.
     if (fmax gt 41.) then fmax=41.

     ; evaluation of the number of bands, their number of channels, and the number of channels for the overlaps

	band_decomp, wband, fmin, fmax, dfkhz, ni1, nbandes,Nc_tot, ni , nrecouv

     
     ;if the file is too big we can't read it in one time, then we read file 20 Go by 20 Go

     if (sizes(nf) le 20.) then begin

        psnames=[names(-1).substring(0,-5)+'_'+strtrim(nf_plot,2)]

        set_ps,psnames(0)+'.ps', /landscape
        device, /color
        !p.multi=[0,3,3,0,0]
      
        read_junon_data, files[nf], LH, RH, t,f,fmin=8., fmax=41.

        dim=size(LH)
        n=dim(1)                ; nombre de colonnes (temps)
        p=dim(2)                ; nombre de lignes (frequence)

        
       ;evaluation of the number of channels in time and frequency to be removed


        perte_freq=(Nc_tot+nrecouv*(nbandes-1)+1) mod ni ; number of frequency channels lost
        perte_time=n mod ni                              ; number of time channels lost
        ncarres=n/ni

        p_lf=perte_freq/2
        p_hf=perte_freq/2
        p_lt=perte_time/2
        p_ht=perte_time/2
        if ((perte_freq mod 2) ne 0) then p_hf=p_hf+1
        if ((perte_time mod 2) ne 0) then p_ht=p_ht+1


        LH=LH(p_lt :n-p_ht-1,p_lf :p-p_hf-1)
        RH=RH(p_lt :n-p_ht-1,p_lf :p-p_hf-1)

       ; preparation of the radon transform

        rho=[0.] & nt=ceil(!pi*ni/(5*ni1))
        theta=findgen(nt)*180./nt
        yc1=prep_ponderation(ni/(5*ni1),ni/(5*ni1))

        wt=where(((theta ge 15.) and (theta le 75.)) or ((theta ge 105.) and (theta le 165.)),nrd)
        theta_rd=findgen(nrd)*120./nrd
        dtheta=120./nrd

       ; preparation of the array containing the parameters of interest

        params_LH=fltarr(nbandes,ncarres*ni1,31)-450.
        params_RH=fltarr(nbandes,ncarres*ni1,31)-450.



        for i=0,(nbandes-1) do begin

           if i ge 1 then nr=nrecouv else nr=0 ;prend en compte le recouvrement dans le découpage
           for j=0,(ncarres-1) do begin

              LH1=LH((j*ni):((j+1)*ni)-1,i*(ni-1-nr):(i+1)*(ni-1)-i*nr)
              RH1=RH((j*ni):((j+1)*ni)-1,i*(ni-1-nr):(i+1)*(ni-1)-i*nr)

           ;integration over ni1 for each panel (ni*ni)

              LH1=rebin(LH1,ni,ni/ni1)
              RH1=rebin(RH1,ni,ni/ni1)

              for k1=0,ni1-1 do begin

                 traitement_junon,LH1[k1*ni/ni1:(k1+1)*ni/ni1-1,*],yc1,xlh1,tflh1,rd_lh1
                 traitement_junon,RH1[k1*ni/ni1:(k1+1)*ni/ni1-1,*],yc1,xrh1,tfrh1,rd_rh1

                 rd_lh1=smooth(rd_lh1(wt),4, /edge_wrap)
                 rd_rh1=smooth(rd_rh1(wt), 4, /edge_wrap)

                 rd_lh1o=rd_lh1
                 rd_rh1o=rd_rh1

                 w_lh=where(rd_LH1 eq max(rd_LH1))
                 w_rh=where(rd_RH1 eq max(rd_RH1))

                 tag_lh=0
                 tag_rh=0

                                ; rearranging the radon transform in
                                ; order to put the maximum peak in the
                                ; center of the array
                 rd_lh1=peakcentering(theta_rd, rd_lh1, w_lh)
                 rd_rh1=peakcentering(theta_rd, rd_rh1, w_rh)

                                ; computing the gaussian fit of the
                                ; radon transform in two cases : on
                                ; the whole array (variables will be
                                ; marked with _all) and on a interval of
                                ; +- 30 degrees around the maximum
                                ;    value (variables will be marked
                                ;    with _30)

                 fit_lh_all=gaussfit(theta_rd,rd_lh1,coeff_lh, chisq=chi2_lh, nterms=4, sigma=err_par_lh, yerror=err_rd_lh)
                 fit_rh_all=gaussfit(theta_rd, rd_rh1, coeff_rh, chisq=chi2_rh, nterms=4, sigma=err_par_rh, yerror=err_rd_rh)

                 snr_lh=snr_func(rd_lh1, theta_rd, coeff_lh)
                 snr_rh=snr_func(rd_rh1, theta_rd, coeff_rh)
                 

		 peakmodel,theta_rd, rd_LH1,w_lh,fit_lh_30, theta_lh, coeff_lh_30, chi2_lh_30, snr_lh_30, err_par_lh_30, err_rd_lh_30
		 peakmodel,theta_rd, rd_RH1,w_rh,fit_rh_30, theta_rh, coeff_rh_30, chi2_rh_30, snr_rh_30, err_par_rh_30, err_rd_rh_30
      
                 
               ; computing the real value corresponding to the position of the maximum, because of the reduction of the interval for the gaussian adjsutement


                 coeff_lh(1)=true_angle(theta_rd, coeff_lh(1), w_lh, nrd, dtheta)
                 coeff_rh(1)=true_angle(theta_rd, coeff_rh(1), w_rh, nrd, dtheta)
                 coeff_lh_30(1)=true_angle(theta_rd, coeff_lh_30(1), w_lh, nrd, dtheta)
                 coeff_rh_30(1)=true_angle(theta_rd, coeff_rh_30(1), w_rh, nrd, dtheta)
                 

                 tmin=t((j*ni+k1*ni/ni1)) & tmax=t(j*ni+(k1+1)*ni/ni1-1)
                 fmin=f(i*(ni-1-nr)) & fmax=f((i+1)*(ni-1)-i*nr)

               ;calculation of the drift

                 slope_lh=tan(coeff_lh(1)*!dtor)*dfkhz*ni1/dtmsec ; pente en MHz/s
                 slope_rh=tan(coeff_rh(1)*!dtor)*dfkhz*ni1/dtmsec
                 slope_lh_30=tan(coeff_lh_30(1)*!dtor)*dfkhz*ni1/dtmsec ; pente en MHz/s
                 slope_rh_30=tan(coeff_rh_30(1)*!dtor)*dfkhz*ni1/dtmsec

                  
                 
                 ;ploting the dynamical spectra, the 2D-FFT and the radon transform if SNR >3, not exceeding 3000 lines of plots in the file

                 if (((snr_lh ge 5.) and (snr_lh_30 ge 5.)) or ((snr_rh ge 5.) and (snr_rh_30 ge 5.))) then begin
                    nplot=nplot+1
                      
                    tag_rh=1 & tag_lh=1
                    plot_data, xlh1, tflh1, rd_lh1, theta_rd, 'LH', slope_lh, snr_lh, chi2_lh, coeff_lh(2), tmin, tmax, fmin, fmax,/fullres
                    oplot, theta_rd, rd_lh1o, line=4, color=25.
                    oplot, theta_rd, fit_lh_all, line=2, color=250.
                    oplot, theta_lh, fit_lh_30, line=2, color=70.
                    oplot,[0,120], [max(rd_lh1), max(rd_lh1)], line=2, color=250.

                    plot_data, xrh1, tfrh1, rd_rh1, theta_rd, 'RH', slope_rh, snr_rh,chi2_rh, coeff_rh(2), tmin, tmax, fmin, fmax,/fullres
                    oplot, theta_rd, rd_rh1o, line=4, color=25.
                    oplot, theta_rd, fit_rh_all, line=2, color=250.
                    oplot, theta_rh, fit_rh_30, line=2, color=70.
                    oplot,[0,120], [max(rd_rh1), max(rd_rh1)], line=2, color=250.
                 endif
                 if (nplot gt 500) then begin
                    device, /close
                    exit_ps
                    ps_pdf, psnames(-1)+'.ps',/remove
                    spawn,'cp '+psnames(-1)+'.pdf ' +'/data/emauduit/results/'+ names(-3)+'/plot/'+ names(-2)+'/'+psnames(-1)+'.pdf'
                    spawn,'rm '+psnames(-1)+'.pdf '
                   
                    nf_plot=nf_plot+1
                    psnames=[psnames,names(-1).substring(0,-5)+'_'+strtrim(nf_plot,2)]
                    set_ps,psnames(-1)+'.ps', /landscape
                    !p.multi=[0,3,3,0,0]
                    nplot=0
                 endif
                 

                 params_LH[i,j*ni1+k1,*]=[nf,tag_lh,i,j,k1,coeff_lh(0),err_par_lh(0), coeff_lh(1),err_par_lh(1) ,coeff_lh(2),err_par_lh(2),coeff_lh(3),err_par_lh(3), chi2_lh, snr_lh, err_rd_lh,coeff_lh_30(0),err_par_lh_30(0), coeff_lh_30(1),err_par_lh_30(1) ,coeff_lh_30(2),err_par_lh_30(2),coeff_lh_30(3),err_par_lh_30(3), chi2_lh_30, snr_lh_30, err_rd_lh_30,tmin, tmax, fmin, fmax]
                 params_RH[i,j*ni1+k1,*]=[nf,tag_rh,i,j,k1,coeff_rh(0),err_par_rh(0), coeff_rh(1),err_par_rh(1) ,coeff_rh(2),err_par_rh(2),coeff_rh(3),err_par_rh(3), chi2_rh, snr_rh,err_rd_rh,coeff_rh_30(0),err_par_rh_30(0), coeff_rh_30(1),err_par_rh_30(1) ,coeff_rh_30(2),err_par_rh_30(2),coeff_rh_30(3),err_par_rh_30(3), chi2_rh_30, snr_rh_30,err_rd_rh_30,tmin, tmax, fmin, fmax]


              endfor

           endfor

        endfor

        device, /close
        exit_ps
        ps_pdf, psnames(-1)+'.ps',/remove
        spawn,'cp '+psnames(-1)+'.pdf ' +'/data/emauduit/results/'+ names(-3)+'/plot/'+ names(-2)+'/'+psnames(-1)+'.pdf'
        spawn,'rm '+psnames(-1)+'.pdf '

        LH=0 & RH=0
        save, path_file , params_LH, params_RH, file='/data/emauduit/results/'+ names(-3)+'/parameters/'+ names(-2)+'/parameters_'+names(-1).substring(0,-5)+'.sav' 
       
     endif else begin

      ; computing the number of subfiles the file has to be split in

        n_open=floor(sizes(nf)/20.)
        r_open=sizes(nf) mod 20.
       
        yy=fix(strmid(files[nf],27,4,/rev))
        mo=fix(strmid(files[nf],23,2,/rev))
        dd=fix(strmid(files[nf],21,2,/rev))
        jd0=julday(mo,dd,yy,0.,0.,0.)

        tini=(desc.jd1-jd0)*24.d0
        dt_coupure=(((desc.jd2-jd0)*24.d0 - (desc.jd1-jd0)*24.d0)/sizes(nf))*20.
        dt_recouv=0.

        psnames=[]


        for nc=0,n_open-1 do begin
           nf_plot=0

           psnames=[psnames,names(-1).substring(0,-5)+'_'+strtrim(nc,2)+'_'+strtrim(nf_plot,2)]

           set_ps,psnames(-1)+'.ps', /landscape
           device, /color
           !p.multi=[0,3,3,0,0]
          
           read_junon_data, files[nf], LH, RH, t,f,tmin=tini+nc*dt_coupure-dt_recouv,tmax=tini+(nc+1)*dt_coupure,fmin=8., fmax=41. 
           dim=size(LH)
           n=dim(1)             ; number of columns (time)
           p=dim(2)             ; number of lines (frequency)


       ;computing the number of channels in time and frequency to be removed


           perte_freq=(Nc_tot+nrecouv*(nbandes-1)+1) mod ni ; frequency channels loss
           perte_time=n mod ni                              ; time channels loss
           dt_recouv=(perte_time+1)*dtmsec
           ncarres=n/ni

           p_lf=perte_freq/2
           p_hf=perte_freq/2
           p_lt=perte_time/2
           p_ht=perte_time/2
           if ((perte_freq mod 2) ne 0) then p_hf=p_hf+1
           if ((perte_time mod 2) ne 0) then p_ht=p_ht+1


           LH=LH(0:n-perte_time-1,p_lf :p-p_hf-1)
           RH=RH(0:n-perte_time-1,p_lf :p-p_hf-1)

       ; preparation of the radon transform

           rho=[0.] & nt=ceil(!pi*ni/(5*ni1))
           theta=findgen(nt)*180./nt
           yc1=prep_ponderation(ni/(5*ni1),ni/(5*ni1))
           wt=where(((theta ge 15.) and (theta le 75.)) or ((theta ge 105.) and (theta le 165.)),nrd)
           theta_rd=findgen(nrd)*120./nrd
           dtheta=120./nrd

       ; preparation of the array containing the parameters of interest

           params_LH=fltarr(nbandes,ncarres*ni1,31)-450.
           params_RH=fltarr(nbandes,ncarres*ni1,31)-450.



           for i=0,(nbandes-1) do begin

              if i ge 1 then nr=nrecouv else nr=0 ;takes the overlap into account for the splitting

              for j=0,(ncarres-1) do begin

                 LH1=LH((j*ni):((j+1)*ni)-1,i*(ni-1-nr):(i+1)*(ni-1)-i*nr)
                 RH1=RH((j*ni):((j+1)*ni)-1,i*(ni-1-nr):(i+1)*(ni-1)-i*nr)


           ;integrating each band over ni1 in frequency
                 LH1=rebin(LH1,ni,ni/ni1)
                 RH1=rebin(RH1,ni,ni/ni1)

                 for k1=0,ni1-1 do begin

                  

                    traitement_junon,LH1[k1*ni/ni1:(k1+1)*ni/ni1-1,*],yc1,xlh1,tflh1,rd_lh1
                    traitement_junon,RH1[k1*ni/ni1:(k1+1)*ni/ni1-1,*],yc1,xrh1,tfrh1,rd_rh1

                    rd_lh1=smooth(rd_lh1(wt),4, /edge_wrap)
                    rd_rh1=smooth(rd_rh1(wt), 4, /edge_wrap)

                    rd_lh1o=rd_lh1
                    rd_rh1o=rd_rh1

                    w_lh=where(rd_LH1 eq max(rd_LH1))
                    w_rh=where(rd_RH1 eq max(rd_RH1))

                    tag_lh=0
                    tag_rh=0

                             ; rearranging the radon transform in
                                ; order to put the maximum peak in the
                                ; center of the array
                    rd_lh1=peakcentering(theta_rd, rd_lh1, w_lh)
                    rd_rh1=peakcentering(theta_rd, rd_rh1, w_rh)

                                ; computing the gaussian fit of the
                                ; radon transform in two cases : on
                                ; the whole array (variables will be
                                ; marked with _all) and on a interval of
                                ; +- 30 degrees around the maximum
                                ;    value (variables will be marked
                                ;    with _30)

                    fit_lh_all=gaussfit(theta_rd,rd_lh1,coeff_lh, chisq=chi2_lh, nterms=4, sigma=err_par_lh, yerror=err_rd_lh)
                    fit_rh_all=gaussfit(theta_rd, rd_rh1, coeff_rh, chisq=chi2_rh, nterms=4, sigma=err_par_rh, yerror=err_rd_rh)

                    snr_lh=snr_func(rd_lh1, theta_rd, coeff_lh)
                    snr_rh=snr_func(rd_rh1, theta_rd, coeff_rh)

                    peakmodel,theta_rd, rd_LH1,w_lh,fit_lh_30, theta_lh, coeff_lh_30, chi2_lh_30, snr_lh_30, err_par_lh_30, err_rd_lh_30
                    peakmodel,theta_rd, rd_RH1,w_rh,fit_rh_30, theta_rh, coeff_rh_30, chi2_rh_30, snr_rh_30, err_par_rh_30, err_rd_rh_30
      
                 
               ; computing the real value corresponding to the position of the maximum, because of the reduction of the interval for the gaussian adjsutement


                    coeff_lh(1)=true_angle(theta_rd, coeff_lh(1), w_lh, nrd, dtheta)
                    coeff_rh(1)=true_angle(theta_rd, coeff_rh(1), w_rh, nrd, dtheta)
                    coeff_lh_30(1)=true_angle(theta_rd, coeff_lh_30(1), w_lh, nrd, dtheta)
                    coeff_rh_30(1)=true_angle(theta_rd, coeff_rh_30(1), w_rh, nrd, dtheta)

                    tmin=t((j*ni+k1*ni/ni1)) & tmax=t(j*ni+(k1+1)*ni/ni1-1)
                    fmin=f(i*(ni-1-nr)) & fmax=f((i+1)*(ni-1)-i*nr)

                    slope_lh=tan(coeff_lh(1)*!dtor)*dfkhz*ni1/dtmsec ; pente en MHz/s
                    slope_rh=tan(coeff_rh(1)*!dtor)*dfkhz*ni1/dtmsec
                    slope_lh_30=tan(coeff_lh_30(1)*!dtor)*dfkhz*ni1/dtmsec ; pente en MHz/s
                    slope_rh_30=tan(coeff_rh_30(1)*!dtor)*dfkhz*ni1/dtmsec

                    if ((nc eq 0) and (i eq 0) and (j eq 0) and (k1 eq 1)) then begin
                       LHs=LH1[k1*ni/ni1:(k1+1)*ni/ni1-1,*]
                       sigs=coeff_lh(2)
                       save, LHs, xlh1, tflh1, rd_lh1o, rd_lh1,fit_lh_all, theta_rd, chi2_lh, snr_lh, slope_lh,sigs, tmin, tmax, fmin , fmax, file='Plot_pente_pos.sav'
                    endif
                    
                    if ((nc eq 1) and (i eq 0) and (j eq 147) and (k1 eq 2)) then begin
                       RHs=RH1[k1*ni/ni1:(k1+1)*ni/ni1-1,*]
                       sigs=coeff_rh(2)
                       save, RHs, xrh1, tfrh1, rd_rh1o, rd_rh1,fit_rh_all, theta_rd, chi2_rh, snr_rh, slope_rh,sigs, tmin, tmax, fmin , fmax, file='Plot_no_detect.sav'
                    endif
                    

                    
                    
                                   
                    if (((snr_lh ge 5.) and (snr_lh_30 ge 5.)) or ((snr_rh ge 5.) and (snr_rh_30 ge 5.))) then begin
                       tag_rh=1 & tag_lh=1
                       nplot=nplot+1
                          
                       plot_data, xlh1, tflh1, rd_lh1, theta_rd, 'LH', slope_lh, snr_lh, chi2_lh, coeff_lh(2), tmin, tmax, fmin, fmax,/fullres
                       oplot, theta_rd, rd_lh1o, line=4, color=25.
                       oplot, theta_rd, fit_lh_all, line=2, color=250.
                       oplot, theta_lh, fit_lh_30, line=2, color=70.
                       oplot,[0,120], [max(rd_lh1), max(rd_lh1)], line=2, color=250.

                       plot_data, xrh1, tfrh1, rd_rh1, theta_rd, 'RH', slope_rh, snr_rh,chi2_rh, coeff_rh(2), tmin, tmax, fmin, fmax,/fullres
                       oplot, theta_rd, rd_rh1o, line=4, color=25.
                       oplot, theta_rd, fit_rh_all, line=2, color=250.
                       oplot, theta_rh, fit_rh_30, line=2, color=70.
                       oplot,[0,120], [max(rd_rh1), max(rd_rh1)], line=2, color=250.
                    endif
                    
                    if (nplot gt 500) then begin

                       device, /close
                       exit_ps
                       ps_pdf, psnames(-1)+'.ps',/remove
                       spawn,'cp '+psnames(-1)+'.pdf ' +'/data/emauduit/results/'+ names(-3)+'/plot/'+ names(-2)+'/'+psnames(-1)+'.pdf'
                       spawn,'rm '+psnames(-1)+'.pdf '
                   
                       nf_plot=nf_plot+1
                       psnames=[psnames,names(-1).substring(0,-5)+'_'+strtrim(nc,2)+'_'+strtrim(nf_plot,2)]
                       set_ps,psnames(-1)+'.ps', /landscape
                       !p.multi=[0,3,3,0,0]
                       nplot=0
                 
                    endif
                    
                    
                      
                    params_LH[i,j*ni1+k1,*]=[nf,tag_lh,i,j,k1,coeff_lh(0),err_par_lh(0), coeff_lh(1),err_par_lh(1) ,coeff_lh(2),err_par_lh(2),coeff_lh(3),err_par_lh(3), chi2_lh, snr_lh, err_rd_lh,coeff_lh_30(0),err_par_lh_30(0), coeff_lh_30(1),err_par_lh_30(1) ,coeff_lh_30(2),err_par_lh_30(2),coeff_lh_30(3),err_par_lh_30(3), chi2_lh_30, snr_lh_30, err_rd_lh_30,tmin, tmax, fmin, fmax]
                 params_RH[i,j*ni1+k1,*]=[nf,tag_rh,i,j,k1,coeff_rh(0),err_par_rh(0), coeff_rh(1),err_par_rh(1) ,coeff_rh(2),err_par_rh(2),coeff_rh(3),err_par_rh(3), chi2_rh, snr_rh,err_rd_rh,coeff_rh_30(0),err_par_rh_30(0), coeff_rh_30(1),err_par_rh_30(1) ,coeff_rh_30(2),err_par_rh_30(2),coeff_rh_30(3),err_par_rh_30(3), chi2_rh_30, snr_rh_30,err_rd_rh_30,tmin, tmax, fmin, fmax]

                 endfor

              endfor


           endfor



           device, /close
           exit_ps
           ps_pdf, psnames(-1)+'.ps',/remove
           spawn,'cp '+psnames(-1)+'.pdf ' +'/data/emauduit/results/'+ names(-3)+'/plot/'+ names(-2)+'/'+psnames(-1)+'.pdf'
           spawn,'rm '+psnames(-1)+'.pdf '
           nf_plot=0

           LH=0 & RH=0
           save, path_file , params_LH, params_RH, file='/data/emauduit/results/'+ names(-3)+'/parameters/'+ names(-2)+'/parameters_'+names(-1).substring(0,-5)+'_'+strtrim(nc,2)+'.sav'
          
        endfor
        nf_plot=0

        psnames=[psnames,names(-1).substring(0,-5)+'_'+strtrim(n_open,2)+'_'+strtrim(nf_plot,2)]

        set_ps,psnames(-1)+'.ps', /landscape
        device, /color
        !p.multi=[0,3,3,0,0]

        read_junon_data, files[nf], LH, RH, t,f,tmin=tini+n_open*dt_coupure-dt_recouv,fmin=8., fmax=41. 
        dim=size(LH)
        n=dim(1)                
        p=dim(2)                


        perte_freq=(Nc_tot+nrecouv*(nbandes-1)+1) mod ni 
        perte_time=n mod ni                              
        dt_recouv=(perte_time+1)*dtmsec
        ncarres=n/ni
        
        p_lf=perte_freq/2
        p_hf=perte_freq/2
        p_lt=perte_time/2
        p_ht=perte_time/2
        if ((perte_freq mod 2) ne 0) then p_hf=p_hf+1
        if ((perte_time mod 2) ne 0) then p_ht=p_ht+1


        LH=LH(0:n-perte_time-1,p_lf :p-p_hf-1)
        RH=RH(0:n-perte_time-1,p_lf :p-p_hf-1)

       
        rho=[0.] & nt=ceil(!pi*ni/(5*ni1))
        theta=findgen(nt)*180./nt
        yc1=prep_ponderation(ni/(5*ni1),ni/(5*ni1))
        wt=where(((theta ge 15.) and (theta le 75.)) or ((theta ge 105.) and (theta le 165.)),nrd)
        theta_rd=findgen(nrd)*120./nrd
        dtheta=120./nrd

       

        params_LH=fltarr(nbandes,ncarres*ni1,31)-450.
        params_RH=fltarr(nbandes,ncarres*ni1,31)-450.



        for i=0,(nbandes-1) do begin

           if i ge 1 then nr=nrecouv else nr=0 
           for j=0,(ncarres-1) do begin

              LH1=LH((j*ni):((j+1)*ni)-1,i*(ni-1-nr):(i+1)*(ni-1)-i*nr)
              RH1=RH((j*ni):((j+1)*ni)-1,i*(ni-1-nr):(i+1)*(ni-1)-i*nr)

           
              LH1=rebin(LH1,ni,ni/ni1)
              RH1=rebin(RH1,ni,ni/ni1)

              for k1=0,ni1-1 do begin
                 
                 traitement_junon,LH1[k1*ni/ni1:(k1+1)*ni/ni1-1,*],yc1,xlh1,tflh1,rd_lh1
                 traitement_junon,RH1[k1*ni/ni1:(k1+1)*ni/ni1-1,*],yc1,xrh1,tfrh1,rd_rh1
                 
                 rd_lh1=smooth(rd_lh1(wt),4, /edge_wrap)
                 rd_rh1=smooth(rd_rh1(wt), 4, /edge_wrap)

                 rd_lh1o=rd_lh1
                 rd_rh1o=rd_rh1

                 w_lh=where(rd_LH1 eq max(rd_LH1))
                 w_rh=where(rd_RH1 eq max(rd_RH1))

                 tag_lh=0
                 tag_rh=0

                                 ; rearranging the radon transform in
                                ; order to put the maximum peak in the
                                ; center of the array
                 rd_lh1=peakcentering(theta_rd, rd_lh1, w_lh)
                 rd_rh1=peakcentering(theta_rd, rd_rh1, w_rh)

                                ; computing the gaussian fit of the
                                ; radon transform in two cases : on
                                ; the whole array (variables will be
                                ; marked with _all) and on a interval of
                                ; +- 30 degrees around the maximum
                                ;    value (variables will be marked
                                ;    with _30)

                 fit_lh_all=gaussfit(theta_rd,rd_lh1,coeff_lh, chisq=chi2_lh, nterms=4, sigma=err_par_lh, yerror=err_rd_lh)
                 fit_rh_all=gaussfit(theta_rd, rd_rh1, coeff_rh, chisq=chi2_rh, nterms=4, sigma=err_par_rh, yerror=err_rd_rh)

                 snr_lh=snr_func(rd_lh1, theta_rd, coeff_lh)
                 snr_rh=snr_func(rd_rh1, theta_rd, coeff_rh)

		 peakmodel,theta_rd, rd_LH1,w_lh,fit_lh_30, theta_lh, coeff_lh_30, chi2_lh_30, snr_lh_30, err_par_lh_30, err_rd_lh_30
		 peakmodel,theta_rd, rd_RH1,w_rh,fit_rh_30, theta_rh, coeff_rh_30, chi2_rh_30, snr_rh_30, err_par_rh_30, err_rd_rh_30
      
                 
               ; computing the real value corresponding to the position of the maximum, because of the reduction of the interval for the gaussian adjsutement


                 coeff_lh(1)=true_angle(theta_rd, coeff_lh(1), w_lh, nrd, dtheta)
                 coeff_rh(1)=true_angle(theta_rd, coeff_rh(1), w_rh, nrd, dtheta)
                 coeff_lh_30(1)=true_angle(theta_rd, coeff_lh_30(1), w_lh, nrd, dtheta)
                 coeff_rh_30(1)=true_angle(theta_rd, coeff_rh_30(1), w_rh, nrd, dtheta)
          
		
                 tmin=t((j*ni+k1*ni/ni1)) & tmax=t(j*ni+(k1+1)*ni/ni1-1)
                 fmin=f(i*(ni-1-nr)) & fmax=f((i+1)*(ni-1)-i*nr)

                 slope_lh=tan(coeff_lh(1)*!dtor)*dfkhz*ni1/dtmsec ; pente en MHz/s
                 slope_rh=tan(coeff_rh(1)*!dtor)*dfkhz*ni1/dtmsec
                 slope_lh_30=tan(coeff_lh_30(1)*!dtor)*dfkhz*ni1/dtmsec ; pente en MHz/s
                 slope_rh_30=tan(coeff_rh_30(1)*!dtor)*dfkhz*ni1/dtmsec

                
                     

                

                 if (((snr_lh ge 5.) and (snr_lh_30 ge 5.)) or ((snr_rh ge 5.) and (snr_rh_30 ge 5.))) then begin
                    nplot=nplot+1
                    tag_rh=1 & tag_lh=1
                    plot_data, xlh1, tflh1, rd_lh1, theta_rd, 'LH', slope_lh, snr_lh, chi2_lh, coeff_lh(2), tmin, tmax, fmin, fmax,/fullres
                    oplot, theta_rd, rd_lh1o, line=4, color=25.
                    oplot, theta_rd, fit_lh_all, line=2, color=250.
                    oplot, theta_lh, fit_lh_30, line=2, color=70.
                    oplot,[0,120], [max(rd_lh1), max(rd_lh1)], line=2, color=250.

                    plot_data, xrh1, tfrh1, rd_rh1, theta_rd, 'RH', slope_rh, snr_rh,chi2_rh, coeff_rh(2), tmin, tmax, fmin, fmax,/fullres
                    oplot, theta_rd, rd_rh1o, line=4, color=25.
                    oplot, theta_rd, fit_rh_all, line=2, color=250.
                    oplot, theta_rh, fit_rh_30, line=2, color=70.
                    oplot,[0,120], [max(rd_rh1), max(rd_rh1)], line=2, color=250.
                 endif

                 if (nplot gt 500) then begin

                    device, /close
                    exit_ps
                    ps_pdf, psnames(-1)+'.ps',/remove
                    spawn,'cp '+psnames(-1)+'.pdf ' +'/data/emauduit/results/'+ names(-3)+'/plot/'+ names(-2)+'/'+psnames(-1)+'.pdf'
                    spawn,'rm '+psnames(-1)+'.pdf '
                   
                    nf_plot=nf_plot+1
                    psnames=[psnames,names(-1).substring(0,-5)+'_'+strtrim(n_open,2)+'_'+strtrim(nf_plot,2)]
                    set_ps,psnames(-1)+'.ps', /landscape
                    !p.multi=[0,3,3,0,0]
                    nplot=0

                    endif
                   
                 params_LH[i,j*ni1+k1,*]=[nf,tag_lh,i,j,k1,coeff_lh(0),err_par_lh(0), coeff_lh(1),err_par_lh(1) ,coeff_lh(2),err_par_lh(2),coeff_lh(3),err_par_lh(3), chi2_lh, snr_lh, err_rd_lh,coeff_lh_30(0),err_par_lh_30(0), coeff_lh_30(1),err_par_lh_30(1) ,coeff_lh_30(2),err_par_lh_30(2),coeff_lh_30(3),err_par_lh_30(3), chi2_lh_30, snr_lh_30, err_rd_lh_30,tmin, tmax, fmin, fmax]
                 params_RH[i,j*ni1+k1,*]=[nf,tag_rh,i,j,k1,coeff_rh(0),err_par_rh(0), coeff_rh(1),err_par_rh(1) ,coeff_rh(2),err_par_rh(2),coeff_rh(3),err_par_rh(3), chi2_rh, snr_rh,err_rd_rh,coeff_rh_30(0),err_par_rh_30(0), coeff_rh_30(1),err_par_rh_30(1) ,coeff_rh_30(2),err_par_rh_30(2),coeff_rh_30(3),err_par_rh_30(3), chi2_rh_30, snr_rh_30,err_rd_rh_30,tmin, tmax, fmin, fmax]

              endfor

           endfor

        endfor

        LH=0 & RH=0
        device, /close
        exit_ps
        ps_pdf, psnames(-1)+'.ps',/remove
        spawn,'cp '+psnames(-1)+'.pdf ' +'/data/emauduit/results/'+ names(-3)+'/plot/'+ names(-2)+'/'+psnames(-1)+'.pdf'
        spawn,'rm '+psnames(-1)+'.pdf '
        
        save, path_file , params_LH, params_RH, file='/data/emauduit/results/'+ names(-3)+'/parameters/'+ names(-2)+'/parameters_'+names(-1).substring(0,-5)+'_'+strtrim(n_open,2)+'.sav'
          
              
      
     endelse
     
     
     
     times(nf)=toc(clock)
    
    ; save the array containing the parameters in a saveset .sav with the same name than the file
     
     print, 'numero du fichier',nf
     
     save, files, sizes, times, filename='/data/emauduit/results/'+names(-3)+'/liste_fichiers_'+names(-2)+'_'+names(-3)+'.sav'
  endfor

  
  return
end




