;+
;
; :Description:
;
;  Compute the most adapted number of bands, of channels for the bands and the overlaps
;
; :Parameters:
;
;  INPUT :
;
; bw : band witdh, in MHz, given by the operator
; fmin,fmax : minimum and maximum frequency of the studied array
; dfkhz : frequency resolution of the array (about 3.05 kHz)
; ni1 : factor of integration depending on the keyword set in traitement_massif.pro
; 
; OUTPUT :
;
; nbandes : number of bands to analyze
; ni : number of frequency channels of the band
; nrecouv : number of channels corresponding to the overlap
;
;-


pro band_decomp, bw, fmin, fmax, dfkhz,ni1, nbandes, Nc_tot,ni,nrecouv

	lfreq=fmax-fmin ;frequency width of the dynamical spectra
	Nc_tot=floor(lfreq*1e3/dfkhz) ; corresponding number of channels

	ni=ceil(bw*1e3/dfkhz ); corresponding number of channels for the band
	nbandes=ceil(Nc_tot/ni) ; number of possible bands in the array

	while ((ni mod (ni1*5)) ne 0) do ni=ni-1

	if (nbandes gt 1) then dfrecouv=abs(((nbandes*long(ni))-Nc_tot)*dfkhz*1e-3/(nbandes-1)) else dfrecouv=0.
	dfreq=dfkhz*ni ; calculation of the real frequency width of the bands
	nrecouv=long(round(dfrecouv*1e3/dfkhz))

	return
end


