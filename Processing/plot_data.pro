;+
;
; :Description:
;
; Plots the dynamic spectrum, the 2D FFT and the Radon transform along
; with its Gaussian fit
;
; :Parameters:
;
; INPUT:
;
; X : the dynamic spectra
; TF : the 2D-FFT
; RDW : the Radon transform
; RDfit : its gaussian fit
; angles : angles for the plot
; pola : 'LH' or 'RH'
; slope : slope of the structure
; SNR : value of the SNR
; chi2p : value of the Chi^2 of the fit
; sig : value of the sigma of the fit
; tmin, tmax : time interval of the plot
; fmin, fmax : frequency interval of the plot
;
;-

pro plot_data, x, tf, rdw,angles, pola, slope, snr, chi2p, sig, tmin, tmax, fmin, fmax, fullres=fullres

  if not (keyword_set(fullres)) then begin
     dim=size(x)
     n=dim(1)
     p=dim(2)
     x=rebin(x, n/5, p/5)
     tf=rebin(tf, n/5,p/5)
  endif
       

  loadct, 0
  y=x & xmin=1.0 &  xmax=1.5
  y=y>xmin<xmax
  y(0,0)=xmin & y(1,0)=xmax
  spdynps, y,0, (tmax-tmin)*3600., fmin, fmax, 'Time [s] from '+strtrim(tmin,2)+' h', 'Frequency [MHz]', 'SPDYN, '+pola+string(slope, format='(", pente=",f7.3)')+' MHz/s', 0,0,0,0.,1., 1.

  loadct, 13
  oplot, ((tmax-tmin)*3600./2.)+[-0.4,0.4]*5,((fmin+fmax)/2.)+[-0.4,0.4]*slope*5 , thick=15, line=2, color=250.

  spdynps,alog10(tf),0, (tmax-tmin)*3600.,fmin, fmax, 'Time!U-1!N [s]', 'Frequency!U-1!N [MHz]','TF', 0,0,0,0.01,0.99,1., 'dB'

  plot, angles, rdw, xtitle='Angle de Radon [deg]', ytitle='RD + Gaussfit', title=string(snr, chi2p, sig, format='("SNR=",f8.3,", chi2=",f8.3, ", sig=", f8.2)'), yrange=[min(rdw), max(rdw)+0.1*max(rdw)]
  oplot, [60,60], [-100,100], line=2
  oplot, [0.,120.], [0.,0.], line=2
  

  return
end

