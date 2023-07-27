import os
import scipy.io as sio
from scipy.io import readsav
from array import array
import matplotlib.pyplot as plt
import matplotlib.image as img
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import pandas as pd
import jupiter_sf as jup

###################################################
#--------------------- Tools ---------------------#
###################################################

def find_value(value: float, list: array, res: bool = False):
    """Find the index of the value closest to a in a list l.
    :param a:
        Value to find in the list
    :type a:
        float
    :param l:
        List to search into
    :type l:
        array
    :param res:
        If not specified, the function returns the index. If res=True, returns the value associated to the index.
    """
    min = np.abs(list[0] - value)
    indmin = 0
    for i in range(1, len(list)):
        nmin = np.abs(list[i] - value)
        if nmin <= min:
            min = nmin
            indmin = i
    if not res:
        return indmin
    else:
        return list[indmin]


###################################################
#-- Loading the data and applying SNR criterion --#
###################################################

year=str(input('Year ?'))
month=str(input('Month ?'))

data=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/interpol_time_fit_all_'+month+'_'+year+'.sav')

#Central Meridien Longitude (CML) in degrees for every chunk of data processed
cml_lh=data['cmlsf_lh']
cml_rh=data['cmlsf_rh']

#Corresponding Io's phases 
phiio_lh=data['phiosf_lh']
phiio_rh=data['phiosf_rh']

#Corresponding Ganymede's phases 
phiga_lh=data['phigasf_lh']
phiga_rh=data['phigasf_rh']

#Corresponding Europa's phases 
phieu_lh=data['phieusf_lh']
phieu_rh=data['phieusf_rh']

#Reference Julian date 01/01/1990
jd90=2447892.5000000005

#Times and frequencies of every chunk of data
t_lh=data['t90sf_lh'] ; t_rh=data['t90sf_rh']
f_lh=data['f90sf_lh'] ; f_rh=data['f90sf_rh']

#Corresponding intensity measured
i_lh=data['i90sf_lh']
i_rh=data['i90sf_rh']

#Corresponding drift rate measured
s_lh=data['s90sf_lh']
s_rh=data['s90sf_rh']

#Corresponding sigma measured
sig_lh=2*np.sqrt(2*np.log10(2))*data['sig90sf_lh']
sig_rh=2*np.sqrt(2*np.log10(2))*data['sig90sf_rh']

#Corresponding chi squared
chi_lh=data['chi90sf_lh']
chi_rh=data['chi90sf_rh']

#Corresponding SNR measured
snr_lh=data['snr90sf_lh']
snr_rh=data['snr90sf_rh']

#Number of chunk of data processed in each polarization
dim_lh=len(cml_lh) ; dim_rh=len(cml_rh)

#Applying the criterion on the SNR : SNR > 6.

cml_lh = cml_lh[snr_lh > 6.] ; cml_rh = cml_rh[snr_rh > 6.]
phiio_lh=phiio_lh[snr_lh > 6.] ; phiio_rh=phiio_rh[snr_rh > 6.]
phiga_lh=phiga_lh[snr_lh > 6.] ; phiga_rh=phiga_rh[snr_rh > 6.]
phieu_lh=phieu_lh[snr_lh > 6.] ; phieu_rh=phieu_rh[snr_rh > 6.]
t_lh=t_lh[snr_lh > 6.] ; t_rh=t_rh[snr_rh > 6.] 
f_lh=f_lh[snr_lh > 6.] ; f_rh=f_rh[snr_rh > 6.]
i_lh=i_lh[snr_lh > 6.] ; i_rh=i_rh[snr_rh > 6.] 
s_lh=s_lh[snr_lh > 6.] ; s_rh=s_rh[snr_rh > 6.] 
sig_lh=sig_lh[snr_lh > 6.] ; sig_rh=sig_rh[snr_rh > 6.] 
chi_lh=chi_lh[snr_lh > 6.] ; chi_rh=chi_rh[snr_rh > 6.]
snr_lh=snr_lh[snr_lh > 6.] ; snr_rh=snr_rh[snr_rh > 6.]

#Number of detections in each polarization
nlh=len(cml_lh) ; nrh=len(cml_rh)

data_lh = pd.DataFrame({
    'cml' : cml_lh,
    'phi_io' : phiio_lh,
    'phi_gan' : phiga_lh,
    'phi_eu' : phieu_lh,
    'time' : t_lh,
    'freq' : f_lh,
    'intensity' : i_lh,
    'drift_rate' : s_lh,
    'sigma' : sig_lh,
    'chi' : chi_lh,
    'snr' : snr_lh
})

data_rh = pd.DataFrame({
    'cml' : cml_rh,
    'phi_io' : phiio_rh,
    'phi_gan' : phiga_rh,
    'phi_eu' : phieu_rh,
    'time' : t_rh,
    'freq' : f_rh,
    'intensity' : i_rh,
    'drift_rate' : s_rh,
    'sigma' : sig_rh,
    'chi' : chi_rh,
    'snr' : snr_rh
})

with pd.ExcelWriter('data_figure_1_bis.xlsx') as writer:
    data_lh.to_excel(writer,sheet_name='LH')
    data_rh.to_excel(writer,sheet_name='RH')

####################################################################
#-------------- Analysis by likely origin of emission -------------#
####################################################################

data_io_lh = pd.DataFrame({
    'cml' : np.array([cml_lh[i] for i in range(nlh) if jup.inboxio(cml_lh[i],phiio_lh[i])]),
    'phi_io' : np.array([phiio_lh[i] for i in range(nlh) if jup.inboxio(cml_lh[i],phiio_lh[i])]),
    'phi_gan' : np.array([phiga_lh[i] for i in range(nlh) if jup.inboxio(cml_lh[i],phiio_lh[i])]),
    'phi_eu' : np.array([phieu_lh[i] for i in range(nlh) if jup.inboxio(cml_lh[i],phiio_lh[i])]),
    'time' : np.array([t_lh[i] for i in range(nlh) if jup.inboxio(cml_lh[i],phiio_lh[i])]),
    'freq' : np.array([f_lh[i] for i in range(nlh) if jup.inboxio(cml_lh[i],phiio_lh[i])]),
    'intensity' : np.array([i_lh[i] for i in range(nlh) if jup.inboxio(cml_lh[i],phiio_lh[i])]),
    'drift_rate' : np.array([s_lh[i] for i in range(nlh) if jup.inboxio(cml_lh[i],phiio_lh[i])]),
    'sigma' : np.array([sig_lh[i] for i in range(nlh) if jup.inboxio(cml_lh[i],phiio_lh[i])]),
    'chi' : np.array([chi_lh[i] for i in range(nlh) if jup.inboxio(cml_lh[i],phiio_lh[i])]),
    'snr' : np.array([snr_lh[i] for i in range(nlh) if jup.inboxio(cml_lh[i],phiio_lh[i])])
})

data_io_rh = pd.DataFrame({
    'cml' : np.array([cml_rh[i] for i in range(nrh) if jup.inboxio(cml_rh[i],phiio_rh[i])]),
    'phi_io' : np.array([phiio_rh[i] for i in range(nrh) if jup.inboxio(cml_rh[i],phiio_rh[i])]),
    'phi_gan' : np.array([phiga_rh[i] for i in range(nrh) if jup.inboxio(cml_rh[i],phiio_rh[i])]),
    'phi_eu' : np.array([phieu_rh[i] for i in range(nrh) if jup.inboxio(cml_rh[i],phiio_rh[i])]),
    'time' : np.array([t_rh[i] for i in range(nrh) if jup.inboxio(cml_rh[i],phiio_rh[i])]),
    'freq' : np.array([f_rh[i] for i in range(nrh) if jup.inboxio(cml_rh[i],phiio_rh[i])]),
    'intensity' : np.array([i_rh[i] for i in range(nrh) if jup.inboxio(cml_rh[i],phiio_rh[i])]),
    'drift_rate' : np.array([s_rh[i] for i in range(nrh) if jup.inboxio(cml_rh[i],phiio_rh[i])]),
    'sigma' : np.array([sig_rh[i] for i in range(nrh) if jup.inboxio(cml_rh[i],phiio_rh[i])]),
    'chi' : np.array([chi_rh[i] for i in range(nrh) if jup.inboxio(cml_rh[i],phiio_rh[i])]),
    'snr' : np.array([snr_rh[i] for i in range(nrh) if jup.inboxio(cml_rh[i],phiio_rh[i])])
})

data_gan_lh = pd.DataFrame({
    'cml' : np.array([cml_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'phi_io' : np.array([phiio_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'phi_gan' : np.array([phiga_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'phi_eu' : np.array([phieu_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'time' : np.array([t_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'freq' : np.array([f_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'intensity' : np.array([i_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'drift_rate' : np.array([s_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'sigma' : np.array([sig_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'chi' : np.array([chi_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'snr' : np.array([snr_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (jup.inboxgan(cml_lh[i],phiga_lh[i]))])
})

data_gan_rh = pd.DataFrame({
    'cml' : np.array([cml_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'phi_io' : np.array([phiio_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'phi_gan' : np.array([phiga_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'phi_eu' : np.array([phieu_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'time' : np.array([t_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'freq' : np.array([f_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'intensity' : np.array([i_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'drift_rate' : np.array([s_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'sigma' : np.array([sig_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'chi' : np.array([chi_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'snr' : np.array([snr_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (jup.inboxgan(cml_rh[i],phiga_rh[i]))])
})

data_aur_lh = pd.DataFrame({
    'cml' : np.array([cml_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and ( not jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'phi_io' : np.array([phiio_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and ( not jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'phi_gan' : np.array([phiga_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (not jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'phi_eu' : np.array([phieu_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (not jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'time' : np.array([t_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (not jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'freq' : np.array([f_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (not jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'intensity' : np.array([i_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (not jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'drift_rate' : np.array([s_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (not jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'sigma' : np.array([sig_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (not jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'chi' : np.array([chi_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (not jup.inboxgan(cml_lh[i],phiga_lh[i]))]),
    'snr' : np.array([snr_lh[i] for i in range(nlh) if (not jup.inboxio(cml_lh[i],phiio_lh[i])) and (not jup.inboxgan(cml_lh[i],phiga_lh[i]))])
})

data_aur_rh = pd.DataFrame({
    'cml' : np.array([cml_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (not jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'phi_io' : np.array([phiio_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (not jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'phi_gan' : np.array([phiga_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (not jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'phi_eu' : np.array([phieu_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and ( not jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'time' : np.array([t_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (not jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'freq' : np.array([f_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and ( not jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'intensity' : np.array([i_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and ( not jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'drift_rate' : np.array([s_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (not jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'sigma' : np.array([sig_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (not jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'chi' : np.array([chi_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (not jup.inboxgan(cml_rh[i],phiga_rh[i]))]),
    'snr' : np.array([snr_rh[i] for i in range(nrh) if (not jup.inboxio(cml_rh[i],phiio_rh[i])) and (not jup.inboxgan(cml_rh[i],phiga_rh[i]))])
})

####################################################################
#-------------------------- Data Figure 1 -------------------------#
####################################################################

with pd.ExcelWriter('data_figure_1.xlsx') as writer:
    data_io_lh.to_excel(writer,sheet_name='Io_LH')
    data_io_rh.to_excel(writer,sheet_name='Io_RH')
    data_gan_lh.to_excel(writer,sheet_name='Gan_LH')
    data_gan_rh.to_excel(writer,sheet_name='Gan_RH')
    data_aur_lh.to_excel(writer,sheet_name='Aur_LH')
    data_aur_rh.to_excel(writer,sheet_name='Aur_RH')

####################################################################
#--------------------- Analysis by drift-rate ---------------------#
####################################################################

data_io_lh_1 = data_io_lh.loc[(data_io_lh['drift_rate'] >= -35.) & (data_io_lh['drift_rate'] <= -10.),:] ; nilh1 = data_io_lh_1.shape[0]
data_io_lh_2 = data_io_lh.loc[(data_io_lh['drift_rate'] > -10.) & (data_io_lh['drift_rate'] <= 0.),:] ; nilh2 = data_io_lh_2.shape[0]
data_io_lh_3 = data_io_lh.loc[(data_io_lh['drift_rate'] > 0.) & (data_io_lh['drift_rate'] <= 20.),:] ; nilh3 = data_io_lh_3.shape[0]

data_io_rh_1 = data_io_rh.loc[(data_io_rh['drift_rate'] >= -35.) & (data_io_rh['drift_rate'] <= -10.),:] ; nirh1 = data_io_rh_1.shape[0]
data_io_rh_2 = data_io_rh.loc[(data_io_rh['drift_rate'] > -10.) & (data_io_rh['drift_rate'] <= 0.),:] ; nirh2 = data_io_rh_2.shape[0]
data_io_rh_3 = data_io_rh.loc[(data_io_rh['drift_rate'] > 0.) & (data_io_rh['drift_rate'] <= 20.),:] ; nirh3 = data_io_rh_3.shape[0]

data_gan_lh_1 = data_gan_lh.loc[(data_gan_lh['drift_rate'] >= -35.) & (data_gan_lh['drift_rate'] <= -10.),:] ; nglh1 = data_gan_lh_1.shape[0]
data_gan_lh_2 = data_gan_lh.loc[(data_gan_lh['drift_rate'] > -10.) & (data_gan_lh['drift_rate'] <= 0.),:] ; nglh2 = data_gan_lh_2.shape[0]
data_gan_lh_3 = data_gan_lh.loc[(data_gan_lh['drift_rate'] > 0.) & (data_gan_lh['drift_rate'] <= 20.),:] ; nglh3 = data_gan_lh_3.shape[0]

data_gan_rh_1 = data_gan_rh.loc[(data_gan_rh['drift_rate'] >= -35.) & (data_gan_rh['drift_rate'] <= -10.),:] ; ngrh1 = data_gan_rh_1.shape[0]
data_gan_rh_2 = data_gan_rh.loc[(data_gan_rh['drift_rate'] > -10.) & (data_gan_rh['drift_rate'] <= 0.),:] ; ngrh2 = data_gan_rh_2.shape[0]
data_gan_rh_3 = data_gan_rh.loc[(data_gan_rh['drift_rate'] > 0.) & (data_gan_rh['drift_rate'] <= 20.),:] ; ngrh3 = data_gan_rh_3.shape[0]

data_aur_lh_1 = data_aur_lh.loc[(data_aur_lh['drift_rate'] >= -35.) & (data_aur_lh['drift_rate'] <= -10.),:] ; nalh1 = data_aur_lh_1.shape[0]
data_aur_lh_2 = data_aur_lh.loc[(data_aur_lh['drift_rate'] > -10.) & (data_aur_lh['drift_rate'] <= 0.),:] ; nalh2 = data_aur_lh_2.shape[0]
data_aur_lh_3 = data_aur_lh.loc[(data_aur_lh['drift_rate'] > 0.) & (data_aur_lh['drift_rate'] <= 20.),:] ; nalh3 = data_aur_lh_3.shape[0]

data_aur_rh_1 = data_aur_rh.loc[(data_aur_rh['drift_rate'] >= -35.) & (data_aur_rh['drift_rate'] <= -10.),:] ; narh1 = data_aur_rh_1.shape[0]
data_aur_rh_2 = data_aur_rh.loc[(data_aur_rh['drift_rate'] > -10.) & (data_aur_rh['drift_rate'] <= 0.),:] ; narh2 = data_aur_rh_2.shape[0]
data_aur_rh_3 = data_aur_rh.loc[(data_aur_rh['drift_rate'] > 0.) & (data_aur_rh['drift_rate'] <= 20.),:] ; narh3 = data_aur_rh_3.shape[0]


####################################################################
#-------------------------- Data Figure 3 -------------------------#
####################################################################

## Io 

hist_si1_lh,xsi1_lh=np.histogram(data_io_lh_1['drift_rate'],bins=25,range=(-35.,-10.))
hist_si1_rh,xsi1_rh=np.histogram(data_io_rh_1['drift_rate'],bins=25,range=(-35.,-10.))
hist_si2_lh,xsi2_lh=np.histogram(data_io_lh_2['drift_rate'],bins=10,range=(-10.,0))
hist_si2_rh,xsi2_rh=np.histogram(data_io_rh_2['drift_rate'],bins=10,range=(-10.,0))
hist_si3_lh,xsi3_lh=np.histogram(data_io_lh_3['drift_rate'],bins=20,range=(0.,20.))
hist_si3_rh,xsi3_rh=np.histogram(data_io_rh_3['drift_rate'],bins=20,range=(0.,20.))

## Ganymède 

hist_sg1_lh,xsg1_lh=np.histogram(data_gan_lh_1['drift_rate'],bins=25,range=(-35.,-10.))
hist_sg1_rh,xsg1_rh=np.histogram(data_gan_rh_1['drift_rate'],bins=25,range=(-35.,-10.))
hist_sg2_lh,xsg2_lh=np.histogram(data_gan_lh_2['drift_rate'],bins=10,range=(-10.,0))
hist_sg2_rh,xsg2_rh=np.histogram(data_gan_rh_2['drift_rate'],bins=10,range=(-10.,0))
hist_sg3_lh,xsg3_lh=np.histogram(data_gan_lh_3['drift_rate'],bins=20,range=(0.,20.))
hist_sg3_rh,xsg3_rh=np.histogram(data_gan_rh_3['drift_rate'],bins=20,range=(0.,20.))

# Aurores

hist_sa1_lh,xsa1_lh=np.histogram(data_aur_lh_1['drift_rate'],bins=25,range=(-35.,-10.))
hist_sa1_rh,xsa1_rh=np.histogram(data_aur_rh_1['drift_rate'],bins=25,range=(-35.,-10.))
hist_sa2_lh,xsa2_lh=np.histogram(data_aur_lh_2['drift_rate'],bins=10,range=(-10.,0))
hist_sa2_rh,xsa2_rh=np.histogram(data_aur_rh_2['drift_rate'],bins=10,range=(-10.,0))
hist_sa3_lh,xsa3_lh=np.histogram(data_aur_lh_3['drift_rate'],bins=20,range=(0.,20.))
hist_sa3_rh,xsa3_rh=np.histogram(data_aur_rh_3['drift_rate'],bins=20,range=(0.,20.))

dio1_lh = pd.DataFrame({'x' : xsi1_lh[1:], 'y' : hist_si1_lh}) ; dio1_rh = pd.DataFrame({'x' : xsi1_rh[1:], 'y' : hist_si1_rh})
dio2_lh = pd.DataFrame({'x' : xsi2_lh[1:], 'y' : hist_si2_lh}) ; dio2_rh = pd.DataFrame({'x' : xsi2_rh[1:], 'y' : hist_si2_rh})
dio3_lh = pd.DataFrame({'x' : xsi3_lh[1:], 'y' : hist_si3_lh}) ; dio3_rh = pd.DataFrame({'x' : xsi3_rh[1:], 'y' : hist_si3_rh})

dig1_lh = pd.DataFrame({'x' : xsg1_lh[1:], 'y' : hist_sg1_lh}) ; dig1_rh = pd.DataFrame({'x' : xsg1_rh[1:], 'y' : hist_sg1_rh})
dig2_lh = pd.DataFrame({'x' : xsg2_lh[1:], 'y' : hist_sg2_lh}) ; dig2_rh = pd.DataFrame({'x' : xsg2_rh[1:], 'y' : hist_sg2_rh})
dig3_lh = pd.DataFrame({'x' : xsg3_lh[1:], 'y' : hist_sg3_lh}) ; dig3_rh = pd.DataFrame({'x' : xsg3_rh[1:], 'y' : hist_sg3_rh})

dia1_lh = pd.DataFrame({'x' : xsa1_lh[1:], 'y' : hist_sa1_lh}) ; dia1_rh = pd.DataFrame({'x' : xsa1_rh[1:], 'y' : hist_sa1_rh})
dia2_lh = pd.DataFrame({'x' : xsa2_lh[1:], 'y' : hist_sa2_lh}) ; dia2_rh = pd.DataFrame({'x' : xsa2_rh[1:], 'y' : hist_sa2_rh})
dia3_lh = pd.DataFrame({'x' : xsa3_lh[1:], 'y' : hist_sa3_lh}) ; dia3_rh = pd.DataFrame({'x' : xsa3_rh[1:], 'y' : hist_sa3_rh})

with pd.ExcelWriter('data_figure_3.xlsx') as writer:
    dio1_lh.to_excel(writer, sheet_name='Io_lh_-35_s_-10')
    dio2_lh.to_excel(writer, sheet_name='Io_lh_-10_s_0')
    dio3_lh.to_excel(writer, sheet_name='Io_lh_0_s_20')
    dio1_rh.to_excel(writer, sheet_name='Io_rh_-35_s_-10')
    dio2_rh.to_excel(writer, sheet_name='Io_rh_-10_s_0')
    dio3_rh.to_excel(writer, sheet_name='Io_rh_0_s_20')

    dig1_lh.to_excel(writer, sheet_name='Gan_lh_-35_s_-10')
    dig2_lh.to_excel(writer, sheet_name='Gan_lh_-10_s_0')
    dig3_lh.to_excel(writer, sheet_name='Gan_lh_0_s_20')
    dig1_rh.to_excel(writer, sheet_name='Gan_rh_-35_s_-10')
    dig2_rh.to_excel(writer, sheet_name='Gan_rh_-10_s_0')
    dig3_rh.to_excel(writer, sheet_name='Gan_rh_0_s_20')

    dia1_lh.to_excel(writer, sheet_name='Aur_lh_-35_s_-10')
    dia2_lh.to_excel(writer, sheet_name='Aur_lh_-10_s_0')
    dia3_lh.to_excel(writer, sheet_name='Aur_lh_0_s_20')
    dia1_rh.to_excel(writer, sheet_name='Aur_rh_-35_s_-10')
    dia2_rh.to_excel(writer, sheet_name='Aur_rh_-10_s_0')
    dia3_rh.to_excel(writer, sheet_name='Aur_rh_0_s_20')



####################################################################
#------------------------ Data Figure 6 ---------------------------#
####################################################################

RJ = np.float32(69911e3)  # m
L=8. ; Be=7. ; fe=2.8*Be
theta=np.linspace(0,179,179)*0.5 + 1.
ct=np.cos(theta*np.pi/180) ; st=np.sin(theta*np.pi/180)
R=L*(st**2)
f=fe*np.sqrt(1+3*(ct**2))/(R**3)
ct=ct[(R >=0.94) & (R<=1.6)] ; st=st[(R >=0.94) & (R<=1.6)]
f=f[(R >=0.94) & (R<=1.6)] ; R=R[(R >=0.94) & (R<=1.6)]
g=(ct/(st**2))*(3+5*(ct**2))/np.power((1+3*(ct**2)),1.5)

## Io 

gi1_lh=np.array([g[find_value(np.array(data_io_lh_1['freq'])[i],f)] for i in range(nilh1)]) ; gi1_rh=np.array([g[find_value(np.array(data_io_rh_1['freq'])[i],f)] for i in range(nirh1)])
gi2_lh=np.array([g[find_value(np.array(data_io_lh_2['freq'])[i],f)] for i in range(nilh2)]) ; gi2_rh=np.array([g[find_value(np.array(data_io_rh_2['freq'])[i],f)] for i in range(nirh2)])
gi3_lh=np.array([g[find_value(np.array(data_io_lh_3['freq'])[i],f)] for i in range(nilh3)]) ; gi3_rh=np.array([g[find_value(np.array(data_io_rh_3['freq'])[i],f)] for i in range(nirh3)])

vi1_lh = - np.array(data_io_lh_1['drift_rate']) * RJ * L / (3 * np.array(data_io_lh_1['freq']) * gi1_lh) ; vi1_rh = - np.array(data_io_rh_1['drift_rate']) * RJ * L / (3 * np.array(data_io_rh_1['freq']) * gi1_rh)
vi2_lh = - np.array(data_io_lh_2['drift_rate']) * RJ * L / (3*np.array(data_io_lh_2['freq'])*gi2_lh) ; vi2_rh = - np.array(data_io_rh_2['drift_rate']) * RJ * L / (3*np.array(data_io_rh_2['freq'])*gi2_rh)
vi3_lh = np.array(data_io_lh_3['drift_rate']) * RJ * L / (3*np.array(data_io_lh_3['freq'])*gi3_lh) ; vi3_rh = np.array(data_io_rh_3['drift_rate']) * RJ * L / (3*np.array(data_io_rh_3['freq'])*gi3_rh)

Ei1_lh = 256. * np.power(vi1_lh/3e8,2) / (1-np.array(data_io_lh_1['freq'])/40.) ; Ei2_lh = 256. * np.power(vi2_lh/3e8,2) / (1-np.array(data_io_lh_2['freq'])/40.) ; Ei3_lh = 256. * np.power(vi3_lh/3e8,2) / (1-np.array(data_io_lh_3['freq'])/40.)
Ei1_rh = 256. * np.power(vi1_rh/3e8,2) / (1-np.array(data_io_rh_1['freq'])/40.) ; Ei2_rh = 256. * np.power(vi2_rh/3e8,2) / (1-np.array(data_io_rh_2['freq'])/40.) ; Ei3_rh = 256. * np.power(vi3_rh/3e8,2) / (1-np.array(data_io_rh_3['freq'])/40.)

hist_Ei1_lh,xEi1_lh=np.histogram(Ei1_lh,bins=int(np.max(Ei1_lh)-np.min(Ei1_lh)))
hist_Ei1_rh,xEi1_rh=np.histogram(Ei1_rh,bins=int(np.max(Ei1_rh)-np.min(Ei1_rh)))
hist_Ei2_lh,xEi2_lh=np.histogram(Ei2_lh,bins=int((np.max(Ei2_lh)-np.min(Ei2_lh))/0.1))
hist_Ei2_rh,xEi2_rh=np.histogram(Ei2_rh,bins=int((np.max(Ei2_rh)-np.min(Ei2_rh))/0.1))
hist_Ei3_lh,xEi3_lh=np.histogram(Ei3_lh,bins=int((np.max(Ei3_lh)-np.min(Ei3_lh))/0.1))
hist_Ei3_rh,xEi3_rh=np.histogram(Ei3_rh,bins=int((np.max(Ei3_rh)-np.min(Ei3_rh))/0.1))

## Ganymede

gg1_lh=np.array([g[find_value(np.array(data_gan_lh_1['freq'])[i],f)] for i in range(nglh1)]) ; gg1_rh=np.array([g[find_value(np.array(data_gan_rh_1['freq'])[i],f)] for i in range(ngrh1)])
gg2_lh=np.array([g[find_value(np.array(data_gan_lh_2['freq'])[i],f)] for i in range(nglh2)]) ; gg2_rh=np.array([g[find_value(np.array(data_gan_rh_2['freq'])[i],f)] for i in range(ngrh2)])
gg3_lh=np.array([g[find_value(np.array(data_gan_lh_3['freq'])[i],f)] for i in range(nglh3)]) ; gg3_rh=np.array([g[find_value(np.array(data_gan_rh_3['freq'])[i],f)] for i in range(ngrh3)])

vg1_lh = - np.array(data_gan_lh_1['drift_rate']) * RJ * L / (3 * np.array(data_gan_lh_1['freq']) * gg1_lh) ; vg1_rh = - np.array(data_gan_rh_1['drift_rate']) * RJ * L / (3 * np.array(data_gan_rh_1['freq']) * gg1_rh)
vg2_lh = - np.array(data_gan_lh_2['drift_rate']) * RJ * L / (3*np.array(data_gan_lh_2['freq'])*gg2_lh) ; vg2_rh = - np.array(data_gan_rh_2['drift_rate']) * RJ * L / (3*np.array(data_gan_rh_2['freq'])*gg2_rh)
vg3_lh = np.array(data_gan_lh_3['drift_rate']) * RJ * L / (3*np.array(data_gan_lh_3['freq'])*gg3_lh) ; vg3_rh = np.array(data_gan_rh_3['drift_rate']) * RJ * L / (3*np.array(data_gan_rh_3['freq'])*gg3_rh)

Eg1_lh = 256. * np.power(vg1_lh/3e8,2) / (1-np.array(data_gan_lh_1['freq'])/40.) ; Eg2_lh = 256. * np.power(vg2_lh/3e8,2) / (1-np.array(data_gan_lh_2['freq'])/40.) ; Eg3_lh = 256. * np.power(vg3_lh/3e8,2) / (1-np.array(data_gan_lh_3['freq'])/40.)
Eg1_rh = 256. * np.power(vg1_rh/3e8,2) / (1-np.array(data_gan_rh_1['freq'])/40.) ; Eg2_rh = 256. * np.power(vg2_rh/3e8,2) / (1-np.array(data_gan_rh_2['freq'])/40.) ; Eg3_rh = 256. * np.power(vg3_rh/3e8,2) / (1-np.array(data_gan_rh_3['freq'])/40.)

hist_Eg1_lh,xEg1_lh=np.histogram(Eg1_lh,bins=int(np.max(Eg1_lh)-np.min(Eg1_lh)))
hist_Eg1_rh,xEg1_rh=np.histogram(Eg1_rh,bins=int(np.max(Eg1_rh)-np.min(Eg1_rh)))
hist_Eg2_lh,xEg2_lh=np.histogram(Eg2_lh,bins=int((np.max(Eg2_lh)-np.min(Eg2_lh))/0.1))
hist_Eg2_rh,xEg2_rh=np.histogram(Eg2_rh,bins=int((np.max(Eg2_rh)-np.min(Eg2_rh))/0.1))
hist_Eg3_lh,xEg3_lh=np.histogram(Eg3_lh,bins=int((np.max(Eg3_lh)-np.min(Eg3_lh))/0.1))
hist_Eg3_rh,xEg3_rh=np.histogram(Eg3_rh,bins=int((np.max(Eg3_rh)-np.min(Eg3_rh))/0.1))

## Aurora

ga1_lh=np.array([g[find_value(np.array(data_aur_lh_1['freq'])[i],f)] for i in range(nalh1)]) ; ga1_rh=np.array([g[find_value(np.array(data_aur_rh_1['freq'])[i],f)] for i in range(narh1)])
ga2_lh=np.array([g[find_value(np.array(data_aur_lh_2['freq'])[i],f)] for i in range(nalh2)]) ; ga2_rh=np.array([g[find_value(np.array(data_aur_rh_2['freq'])[i],f)] for i in range(narh2)])
ga3_lh=np.array([g[find_value(np.array(data_aur_lh_3['freq'])[i],f)] for i in range(nalh3)]) ; ga3_rh=np.array([g[find_value(np.array(data_aur_rh_3['freq'])[i],f)] for i in range(narh3)])

va1_lh = - np.array(data_aur_lh_1['drift_rate']) * RJ * L / (3 * np.array(data_aur_lh_1['freq']) * ga1_lh) ; va1_rh = - np.array(data_aur_rh_1['drift_rate']) * RJ * L / (3 * np.array(data_aur_rh_1['freq']) * ga1_rh)
va2_lh = - np.array(data_aur_lh_2['drift_rate']) * RJ * L / (3*np.array(data_aur_lh_2['freq'])*ga2_lh) ; va2_rh = - np.array(data_aur_rh_2['drift_rate']) * RJ * L / (3*np.array(data_aur_rh_2['freq'])*ga2_rh)
va3_lh = np.array(data_aur_lh_3['drift_rate']) * RJ * L / (3*np.array(data_aur_lh_3['freq'])*ga3_lh) ; va3_rh = np.array(data_aur_rh_3['drift_rate']) * RJ * L / (3*np.array(data_aur_rh_3['freq'])*ga3_rh)

Ea1_lh = 256. * np.power(va1_lh/3e8,2) / (1-np.array(data_aur_lh_1['freq'])/40.) ; Ea2_lh = 256. * np.power(va2_lh/3e8,2) / (1-np.array(data_aur_lh_2['freq'])/40.) ; Ea3_lh = 256. * np.power(va3_lh/3e8,2) / (1-np.array(data_aur_lh_3['freq'])/40.)
Ea1_rh = 256. * np.power(va1_rh/3e8,2) / (1-np.array(data_aur_rh_1['freq'])/40.) ; Ea2_rh = 256. * np.power(va2_rh/3e8,2) / (1-np.array(data_aur_rh_2['freq'])/40.) ; Ea3_rh = 256. * np.power(va3_rh/3e8,2) / (1-np.array(data_aur_rh_3['freq'])/40.)

hist_Ea1_lh,xEa1_lh=np.histogram(Ea1_lh,bins=int(np.max(Ea1_lh)-np.min(Ea1_lh)))
hist_Ea1_rh,xEa1_rh=np.histogram(Ea1_rh,bins=int(np.max(Ea1_rh)-np.min(Ea1_rh)))
hist_Ea2_lh,xEa2_lh=np.histogram(Ea2_lh,bins=int((np.max(Ea2_lh)-np.min(Ea2_lh))/0.1))
hist_Ea2_rh,xEa2_rh=np.histogram(Ea2_rh,bins=int((np.max(Ea2_rh)-np.min(Ea2_rh))/0.1))
hist_Ea3_lh,xEa3_lh=np.histogram(Ea3_lh,bins=int((np.max(Ea3_lh)-np.min(Ea3_lh))/0.1))
hist_Ea3_rh,xEa3_rh=np.histogram(Ea3_rh,bins=int((np.max(Ea3_rh)-np.min(Ea3_rh))/0.1))

dEo1_lh = pd.DataFrame({'x' : xEi1_lh[1:], 'y' : hist_Ei1_lh}) ; dEo1_rh = pd.DataFrame({'x' : xEi1_rh[1:], 'y' : hist_Ei1_rh})
dEo2_lh = pd.DataFrame({'x' : xEi2_lh[1:], 'y' : hist_Ei2_lh}) ; dEo2_rh = pd.DataFrame({'x' : xEi2_rh[1:], 'y' : hist_Ei2_rh})
dEo3_lh = pd.DataFrame({'x' : xEi3_lh[1:], 'y' : hist_Ei3_lh}) ; dEo3_rh = pd.DataFrame({'x' : xEi3_rh[1:], 'y' : hist_Ei3_rh})

dEg1_lh = pd.DataFrame({'x' : xEg1_lh[1:], 'y' : hist_Eg1_lh}) ; dEg1_rh = pd.DataFrame({'x' : xEg1_rh[1:], 'y' : hist_Eg1_rh})
dEg2_lh = pd.DataFrame({'x' : xEg2_lh[1:], 'y' : hist_Eg2_lh}) ; dEg2_rh = pd.DataFrame({'x' : xEg2_rh[1:], 'y' : hist_Eg2_rh})
dEg3_lh = pd.DataFrame({'x' : xEg3_lh[1:], 'y' : hist_Eg3_lh}) ; dEg3_rh = pd.DataFrame({'x' : xEg3_rh[1:], 'y' : hist_Eg3_rh})

dEa1_lh = pd.DataFrame({'x' : xEa1_lh[1:], 'y' : hist_Ea1_lh}) ; dEa1_rh = pd.DataFrame({'x' : xEa1_rh[1:], 'y' : hist_Ea1_rh})
dEa2_lh = pd.DataFrame({'x' : xEa2_lh[1:], 'y' : hist_Ea2_lh}) ; dEa2_rh = pd.DataFrame({'x' : xEa2_rh[1:], 'y' : hist_Ea2_rh})
dEa3_lh = pd.DataFrame({'x' : xEa3_lh[1:], 'y' : hist_Ea3_lh}) ; dEa3_rh = pd.DataFrame({'x' : xEa3_rh[1:], 'y' : hist_Ea3_rh})

with pd.ExcelWriter('data_figure_6.xlsx') as writer:
    dEo1_lh.to_excel(writer, sheet_name='Io_lh_-35_s_-10')
    dEo2_lh.to_excel(writer, sheet_name='Io_lh_-10_s_0')
    dEo3_lh.to_excel(writer, sheet_name='Io_lh_0_s_20')
    dEo1_rh.to_excel(writer, sheet_name='Io_rh_-35_s_-10')
    dEo2_rh.to_excel(writer, sheet_name='Io_rh_-10_s_0')
    dEo3_rh.to_excel(writer, sheet_name='Io_rh_0_s_20')

    dEg1_lh.to_excel(writer, sheet_name='Gan_lh_-35_s_-10')
    dEg2_lh.to_excel(writer, sheet_name='Gan_lh_-10_s_0')
    dEg3_lh.to_excel(writer, sheet_name='Gan_lh_0_s_20')
    dEg1_rh.to_excel(writer, sheet_name='Gan_rh_-35_s_-10')
    dEg2_rh.to_excel(writer, sheet_name='Gan_rh_-10_s_0')
    dEg3_rh.to_excel(writer, sheet_name='Gan_rh_0_s_20')

    dEa1_lh.to_excel(writer, sheet_name='Aur_lh_-35_s_-10')
    dEa2_lh.to_excel(writer, sheet_name='Aur_lh_-10_s_0')
    dEa3_lh.to_excel(writer, sheet_name='Aur_lh_0_s_20')
    dEa1_rh.to_excel(writer, sheet_name='Aur_rh_-35_s_-10')
    dEa2_rh.to_excel(writer, sheet_name='Aur_rh_-10_s_0')
    dEa3_rh.to_excel(writer, sheet_name='Aur_rh_0_s_20')


####################################################################
#------------------------ Data Figure 8 ---------------------------#
####################################################################

hist_snri1_lh,xsnri1_lh=np.histogram(data_io_lh_1['snr'],bins=20, range=(0,35))
hist_snri1_rh,xsnri1_rh=np.histogram(data_io_rh_1['snr'],bins=20, range=(0,35))
hist_snri2_lh,xsnri2_lh=np.histogram(data_io_lh_2['snr'],bins=20, range=(0,35))
hist_snri2_rh,xsnri2_rh=np.histogram(data_io_rh_2['snr'],bins=20, range=(0,35))
hist_snri3_lh,xsnri3_lh=np.histogram(data_io_lh_3['snr'],bins=20, range=(0,35))
hist_snri3_rh,xsnri3_rh=np.histogram(data_io_rh_3['snr'],bins=30, range=(0,35))

hist_snrg1_lh,xsnrg1_lh=np.histogram(data_gan_lh_1['snr'],bins=20, range=(0,35))
hist_snrg1_rh,xsnrg1_rh=np.histogram(data_gan_rh_1['snr'],bins=20, range=(0,35))
hist_snrg2_lh,xsnrg2_lh=np.histogram(data_gan_lh_2['snr'],bins=20, range=(0,35))
hist_snrg2_rh,xsnrg2_rh=np.histogram(data_gan_rh_2['snr'],bins=20, range=(0,35))
hist_snrg3_lh,xsnrg3_lh=np.histogram(data_gan_lh_3['snr'],bins=20, range=(0,35))
hist_snrg3_rh,xsnrg3_rh=np.histogram(data_gan_rh_3['snr'],bins=20, range=(0,35))

hist_snra1_lh,xsnra1_lh=np.histogram(data_aur_lh_1['snr'],bins=20, range=(0,35))
hist_snra1_rh,xsnra1_rh=np.histogram(data_aur_rh_1['snr'],bins=20, range=(0,35))
hist_snra2_lh,xsnra2_lh=np.histogram(data_aur_lh_2['snr'],bins=20, range=(0,35))
hist_snra2_rh,xsnra2_rh=np.histogram(data_aur_rh_2['snr'],bins=20, range=(0,35))
hist_snra3_lh,xsnra3_lh=np.histogram(data_aur_lh_3['snr'],bins=20, range=(0,35))
hist_snra3_rh,xsnra3_rh=np.histogram(data_aur_rh_3['snr'],bins=20, range=(0,35))

dso1_lh = pd.DataFrame({'x' : xsnri1_lh[:-1], 'y' : hist_snri1_lh+1.}) ; dso1_rh = pd.DataFrame({'x' : xsnri1_rh[:-1], 'y' : hist_snri1_rh+1.})
dso2_lh = pd.DataFrame({'x' : xsnri2_lh[:-1], 'y' : hist_snri2_lh+1.}) ; dso2_rh = pd.DataFrame({'x' : xsnri2_rh[:-1], 'y' : hist_snri2_rh+1.})
dso3_lh = pd.DataFrame({'x' : xsnri3_lh[:-1], 'y' : hist_snri3_lh+1.}) ; dso3_rh = pd.DataFrame({'x' : xsnri3_rh[:-1], 'y' : hist_snri3_rh+1.})

dsg1_lh = pd.DataFrame({'x' : xsnrg1_lh[:-1], 'y' : hist_snrg1_lh}) ; dsg1_rh = pd.DataFrame({'x' : xsnrg1_rh[:-1], 'y' : hist_snrg1_rh})
dsg2_lh = pd.DataFrame({'x' : xsnrg2_lh[:-1], 'y' : hist_snrg2_lh}) ; dsg2_rh = pd.DataFrame({'x' : xsnrg2_rh[:-1], 'y' : hist_snrg2_rh})
dsg3_lh = pd.DataFrame({'x' : xsnrg3_lh[:-1], 'y' : hist_snrg3_lh}) ; dsg3_rh = pd.DataFrame({'x' : xsnrg3_rh[:-1], 'y' : hist_snrg3_rh})

dsa1_lh = pd.DataFrame({'x' : xsnra1_lh[:-1], 'y' : hist_snra1_lh}) ; dsa1_rh = pd.DataFrame({'x' : xsnra1_rh[:-1], 'y' : hist_snra1_rh})
dsa2_lh = pd.DataFrame({'x' : xsnra2_lh[:-1], 'y' : hist_snra2_lh}) ; dsa2_rh = pd.DataFrame({'x' : xsnra2_rh[:-1], 'y' : hist_snra2_rh})
dsa3_lh = pd.DataFrame({'x' : xsnra3_lh[:-1], 'y' : hist_snra3_lh}) ; dsa3_rh = pd.DataFrame({'x' : xsnra3_rh[:-1], 'y' : hist_snra3_rh})

with pd.ExcelWriter('data_figure_8.xlsx') as writer:
    dso1_lh.to_excel(writer, sheet_name='Io_lh_-35_s_-10')
    dso2_lh.to_excel(writer, sheet_name='Io_lh_-10_s_0')
    dso3_lh.to_excel(writer, sheet_name='Io_lh_0_s_20')
    dso1_rh.to_excel(writer, sheet_name='Io_rh_-35_s_-10')
    dso2_rh.to_excel(writer, sheet_name='Io_rh_-10_s_0')
    dso3_rh.to_excel(writer, sheet_name='Io_rh_0_s_20')

    dsg1_lh.to_excel(writer, sheet_name='Gan_lh_-35_s_-10')
    dsg2_lh.to_excel(writer, sheet_name='Gan_lh_-10_s_0')
    dsg3_lh.to_excel(writer, sheet_name='Gan_lh_0_s_20')
    dsg1_rh.to_excel(writer, sheet_name='Gan_rh_-35_s_-10')
    dsg2_rh.to_excel(writer, sheet_name='Gan_rh_-10_s_0')
    dsg3_rh.to_excel(writer, sheet_name='Gan_rh_0_s_20')

    dsa1_lh.to_excel(writer, sheet_name='Aur_lh_-35_s_-10')
    dsa2_lh.to_excel(writer, sheet_name='Aur_lh_-10_s_0')
    dsa3_lh.to_excel(writer, sheet_name='Aur_lh_0_s_20')
    dsa1_rh.to_excel(writer, sheet_name='Aur_rh_-35_s_-10')
    dsa2_rh.to_excel(writer, sheet_name='Aur_rh_-10_s_0')
    dsa3_rh.to_excel(writer, sheet_name='Aur_rh_0_s_20')


####################################################################
#------------------------ Data Figure 10 --------------------------#
####################################################################

sgC1_lh = [np.array(data_gan_lh_1['drift_rate'])[i] for i in range(nglh1) if (jup.inboxganC(np.array(data_gan_lh_1['cml'])[i],np.array(data_gan_lh_1['phi_gan'])[i]))]
sgC2_lh = [np.array(data_gan_lh_2['drift_rate'])[i] for i in range(nglh2) if (jup.inboxganC(np.array(data_gan_lh_2['cml'])[i],np.array(data_gan_lh_2['phi_gan'])[i]))]
sgC3_lh = [np.array(data_gan_lh_3['drift_rate'])[i] for i in range(nglh3) if (jup.inboxganC(np.array(data_gan_lh_3['cml'])[i],np.array(data_gan_lh_3['phi_gan'])[i]))]

sgC1_rh = [np.array(data_gan_rh_1['drift_rate'])[i] for i in range(ngrh1) if (jup.inboxganC(np.array(data_gan_rh_1['cml'])[i],np.array(data_gan_rh_1['phi_gan'])[i]))]
sgC2_rh = [np.array(data_gan_rh_2['drift_rate'])[i] for i in range(ngrh2) if (jup.inboxganC(np.array(data_gan_rh_2['cml'])[i],np.array(data_gan_rh_2['phi_gan'])[i]))]
sgC3_rh = [np.array(data_gan_rh_3['drift_rate'])[i] for i in range(ngrh3) if (jup.inboxganC(np.array(data_gan_rh_3['cml'])[i],np.array(data_gan_rh_3['phi_gan'])[i]))]

hist_sgC1_lh,xsgC1_lh=np.histogram(sgC1_lh,bins=25,range=(-35.,-10.))
hist_sgC1_rh,xsgC1_rh=np.histogram(sgC1_rh,bins=25,range=(-35.,-10.))
hist_sgC2_lh,xsgC2_lh=np.histogram(sgC2_lh,bins=20,range=(-10.,0))
hist_sgC2_rh,xsgC2_rh=np.histogram(sgC2_rh,bins=20,range=(-10.,0))
hist_sgC3_lh,xsgC3_lh=np.histogram(sgC3_lh,bins=20,range=(0.,20.))
hist_sgC3_rh,xsgC3_rh=np.histogram(sgC3_rh,bins=20,range=(0.,20.))

dsgC1_lh = pd.DataFrame({'x' : xsgC1_lh[1:], 'y' : hist_sgC1_lh}) ; dsgC1_rh = pd.DataFrame({'x' : xsgC1_rh[1:], 'y' : hist_sgC1_rh})
dsgC2_lh = pd.DataFrame({'x' : xsgC2_lh[1:], 'y' : hist_sgC2_lh}) ; dsgC2_rh = pd.DataFrame({'x' : xsgC2_rh[1:], 'y' : hist_sgC2_rh})
dsgC3_lh = pd.DataFrame({'x' : xsgC3_lh[1:], 'y' : hist_sgC3_lh}) ; dsgC3_rh = pd.DataFrame({'x' : xsgC3_rh[1:], 'y' : hist_sgC3_rh})

with pd.ExcelWriter('data_figure_10.xlsx') as writer:
    dsgC1_lh.to_excel(writer, sheet_name='GanC_lh_-35_s_-10')
    dsgC2_lh.to_excel(writer, sheet_name='GanC_lh_-10_s_0')
    dsgC3_lh.to_excel(writer, sheet_name='GanC_lh_0_s_20')
    dsgC1_rh.to_excel(writer, sheet_name='GanC_rh_-35_s_-10')
    dsgC2_rh.to_excel(writer, sheet_name='GanC_rh_-10_s_0')
    dsgC3_rh.to_excel(writer, sheet_name='GanC_rh_0_s_20')