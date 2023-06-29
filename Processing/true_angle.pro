;+
;
; :Description:
;
; Compute the corresponding obtain by the gaussian fit taking all
;rearragements on the array
;
;
;
;
;
;-

function true_angle, theta, coeff, pmax, n, dtheta

  w=where((theta ge coeff-dtheta) and (theta le coeff+dtheta))
  if (pmax le n/2) then begin
     w=w - (n/2 - pmax)
     angle=mean(theta(w))
  endif else begin
     w=w +  (pmax - n/2)
     angle=mean(theta(w))
  endelse

  if (angle lt 60.) then angle=angle+15. else angle=angle+45.
  
  return, angle
end
