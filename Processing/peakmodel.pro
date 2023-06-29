;+ 
;
; :Description:
;
; Compute a Gaussian modelisation of a given radon transform, for d an interval of +- 30 degrees around the maximum.
;
; :Parameters:
;
; INPUT :
;
;  x : abscissa of the radon transform
;  y : radon transform
;  pmax : position of the maximum
;  
;
; OUTPUT :
;
;  fity : values of the fitted function
;  theta : abscissa corresponding to the fit
;  coeff : coefficients computed by the fit  
;  chi2 : chi squared value of the fit 
;  snr : signal to noise ratio of the 
;  err_par : errors on the fit parameters
;  err_rd : mean error of the fit with respect to the given radon transform
;
;
;-


pro peakmodel,x,y,pmax, fity,theta, coeff, chi2, snr, err_par, err_rd

  dim=size(x)
  n=dim(1)

  xmin = n/2 - n/4
  xmax = n/2 + n/4

  fity=gaussfit(x[xmin :xmax],y[xmin :xmax], coeff, chisq=chi2, nterms=4, sigma=err_par, yerror=err_rd)
  theta=x[xmin :xmax]

  snr=snr_func(y,x, coeff)

  return

end
