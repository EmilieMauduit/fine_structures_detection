;+
;
; author : Emilie Mauduit
;
; : Description :
;
; Rearrange an array by putting the peak in the center of the array
;
; : Parameters :
;
; INPUTS:
;
; x : array of the abscissas
; y : array of the radon transform
; pmax : position of the maximum
;
;
; OUTPUTS:
;
; yarr : the arranged array
;
;-


function peakcentering, x,y,pmax

  dim=size(x)
  n=dim(1)

  if pmax le n/2 then begin
     yarr=[y(pmax+n/2-1:*),y(0:pmax+n/2-2)]
  endif else begin
     yarr=[y(pmax-n/2:*),y(0:pmax-n/2-1)]
  endelse

  

  return, yarr
end
