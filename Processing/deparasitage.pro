;+
;
; :Description:
;
; Fonction qui permet de retirer les parasites trop importants d'un tableau x
;
; supprime les parasites supérieurs à seuil * sigma
; dans une fenetre glissante de taille largeur
;
; si /db, les données sont traitees en db
; si /time ou /freq, on deparasite uniquement selon cet axe [defaut = selon les 2]
;
; Utilise le_auto_ et interpol_ze
;
;-
;

function deparasitage, data, seuil, largeur, db=db, time=time, freq=freq

  if n_elements(seuil) eq 0 then seuil=3.5
  if n_elements(largeur) eq 0 then largeur=51
  if not(keyword_set(time)) and not(keyword_set(freq)) then begin
	time=1 & freq=1
  endif

  dim=size(data)
  nt=dim(1) & nf=dim(2)
  x=float(data)

  if keyword_set(freq) then begin
    if keyword_set(db) then xtest=10.*alog10(x) else xtest=x
    xf=reform(rebin(xtest,1,nf))
    le_auto_,xf,largeur,seuil,1,xnet,p,EDGE=2,npix=1
    w=where(p eq 0,nw)
    if w(0) ne -1 then begin
      for i=0,nt-1 do begin
        xx=reform(x(i,*))*p
        interpol_ze,xx
        x(i,*)=xx
      endfor
    endif
  endif

  if keyword_set(time) then begin
    if keyword_set(db) then xtest=10.*alog10(x) else xtest=x
    xt=reform(rebin(xtest,nt,1))
    le_auto_,xt,largeur,seuil,1,xnet,p,EDGE=2,npix=1
    w=where(p eq 0,nw)
    if w(0) ne -1 then begin
      for i=0,nf-1 do begin
        xx=reform(x(*,i))*p
        interpol_ze,xx
        x(*,i)=xx
      endfor
    endif
  endif
  

  return, x
end

