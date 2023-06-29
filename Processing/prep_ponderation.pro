function prep_ponderation,n,p
   
   x=fltarr(n,p)+1.
   rho=[0.] & nt=ceil(!pi*n)
   rx=radon(x,nrho=1, rho=rho, ntheta=nt)
   y=rx
   return,y
end 
