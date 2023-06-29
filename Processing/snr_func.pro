;+
;
; :Description:
; 
;  Calcule le rapport signal sur bruit d'un tableau 1D
;  
;   INPUT : 
;     x : data
;     angles : tableau angle
;     coeff : coefficients sorits de gaussfit
;   
;   OUTPUT : rapport amplitude du pic (- valeur moyenne du spectre) / deviation standard ou la moyenne et la deviation standard sont calculés sur une plage ou le signal est plat
;   
;   
;-


function snr_func, x, angles, coeff

  ampl=coeff(0)
  wm=coeff(1)
  w=where((angles le wm-(2*coeff(2))) or (angles ge wm+(2*coeff(2))),nw)

  if (nw ne 0) then std=stddev(x(w)) else std=stddev(x)
  
  result=ampl/std

  return, result
  
end

