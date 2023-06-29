;+
;
;
; :Description:
; 
;  Fonction permmettant de masquer les parasites trop intenses sur une transformée de Fourier carrée
;  
;  :Parameters:
;  
;  INPUT :
;  
;  data : 2D - array de la TF
;  seuil : seuil au-dela du quel on masque
;  
;  OUTPUT :
;  
;  res : 2D - array de la TF avec les parasites trop intenses masqués
;  
;-


function mask_TF, data

  dim=size(data)                ; shape of the data
  n=dim(1)
  p=dim(2)
  
  x=data

  xt=rebin(x,n,1)  ;integration over frequencies
  
  x=x/rebin(xt, n,p)
  
  xf=rebin(x,1,p) ;integration over time
  
  x=x/rebin(xf,n,p)
  
  return, x
end

