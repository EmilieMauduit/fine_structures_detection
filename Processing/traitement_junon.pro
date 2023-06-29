;+
;
; :Description:
;
; Removes parasites, then does the 2D-Fast Fourier transform and the Radon transform weighted of a 2D data array (t,f).
;
;
; :Parameters:
;
;  INPUT :
;
; data : 2D-array with the data to analyze
; yc : the function to use to ponderate the radon transform, obtained with prep_radon.pro
;
;  OUTPUT :
;
; X : Spectrum without interfering signals
; TF : result of the Fourier transform
; RDW : result of the Radon transform corrected
;
;
;-

pro traitement_junon, data,yc, x, tf, rdw

  dim=size(data)                ; shape of the data
  n=dim(1)
  p=dim(2)

  x=data
  x=deparasitage(x,3.5,17, /db)
  make_background,x,'',b,s
  x=x/nozero(rebin(reform(b,1,p),n,p))
  x=deparasitage(x,3.5,17,/freq)
  x=x>0.5<3


  ; 2D Fourier transform centered

  tf=(abs(fft(x, /center, /double))^2)*n
  tf(n/2,n/2)=mean(tf)
  tf=mask_tf(tf)
  tfr=rebin(tf, n/5, p/5)
  ;tfr=tf>0.5<10
  

  ; Radon transform

  rho=[0.] & nt=ceil(!pi*n/5)
  theta=findgen(nt)*180./nt     ; array of the angles values in degrees
  rd=radon(tfr, nrho=1,rho=rho, ntheta=nt)

  ;Correct the Radon transform by using a ponderation function
  rdw=rd/yc
  ;    background,rdc,bck
  ;    rdc=rdc/bck-1.
  rdw=rdw/median(rdw)-1. 

  return

end


