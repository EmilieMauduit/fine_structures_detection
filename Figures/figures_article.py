import os
import scipy.io as sio
from scipy.io import readsav
from array import array
import matplotlib.pyplot as plt
import matplotlib.image as img
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import jupiter_sf as jup



###################################################
#------------------- Tools--------------------#

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
#------------------- Figure 1 --------------------#
###################################################

print('------ Figure 1 ------')

year=str(input('Year ?'))
month=str(input('Month ?'))

data=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/interpol_time_fit_all_'+month+'_'+year+'.sav')

cmlsf_lh=data['cmlsf_lh']
cmlsf_rh=data['cmlsf_rh']

phiosf_lh=data['phiosf_lh']
phiosf_rh=data['phiosf_rh']

phigasf_lh=data['phigasf_lh']
phigasf_rh=data['phigasf_rh']

phieusf_lh=data['phieusf_lh']
phieusf_rh=data['phieusf_rh']

phicasf_lh=data['phicasf_lh']
phicasf_rh=data['phicasf_rh']

phiamsf_lh=data['phiamsf_lh']
phiamsf_rh=data['phiamsf_rh']

jd90=2447892.5000000005

t90sf_lh=data['t90sf_lh']
t90sf_rh=data['t90sf_rh']
f90sf_lh=data['f90sf_lh']
f90sf_rh=data['f90sf_rh']

i90sf_lh=data['i90sf_lh']
i90sf_rh=data['i90sf_rh']
err_i90sf_lh=data['err_i90sf_lh']
err_i90sf_rh=data['err_i90sf_rh']

s90sf_lh=data['s90sf_lh']
s90sf_rh=data['s90sf_rh']
err_s90sf_lh=data['err_s90sf_lh']
err_s90sf_rh=data['err_s90sf_rh']

sig90sf_lh=2*np.sqrt(2*np.log10(2))*data['sig90sf_lh']
sig90sf_rh=2*np.sqrt(2*np.log10(2))*data['sig90sf_rh']
err_sig90sf_lh=2*np.sqrt(2*np.log10(2))*data['err_sig90sf_lh']
err_sig90sf_rh=2*np.sqrt(2*np.log10(2))*data['err_sig90sf_rh']

chi90sf_lh=data['chi90sf_lh']
chi90sf_rh=data['chi90sf_rh']
snr90sf_lh=data['snr90sf_lh']
snr90sf_rh=data['snr90sf_rh']
err_moy90sf_lh=data['err_moy90sf_lh']
err_moy90sf_rh=data['err_moy90sf_rh']

dim_lh=np.shape(cmlsf_lh)
dim_rh=np.shape(cmlsf_rh)

nlh=dim_lh[0]
nrh=dim_rh[0]

cml=[cmlsf_lh,cmlsf_rh]
phio=[phiosf_lh,phiosf_rh]
phiga=[phigasf_lh,phigasf_rh]
phieu=[phieusf_lh,phieusf_rh]
phica=[phicasf_lh, phicasf_rh]
phiam=[phiamsf_lh, phiamsf_rh]

cml_lh=[] ; cml_rh=[]
phiio_lh=[] ; phiio_rh=[]
phiga_lh=[] ; phiga_rh=[]
phieu_lh=[] ; phieu_rh=[]
t_lh=[] ; t_rh=[] ; f_lh=[] ; f_rh=[]
i_lh=[] ; i_rh=[] ; err_i_lh=[] ; err_i_rh=[]
s_lh=[] ; s_rh=[] ; err_s_lh=[] ; err_s_rh=[]
sig_lh=[] ; sig_rh=[] ; err_sig_lh=[] ; err_sig_rh=[]
chi_lh=[] ; chi_rh=[]
snr_lh=[] ; snr_rh=[]

for i in range(nlh):
    if (snr90sf_lh[i] >= 6.):
        cml_lh.append(cmlsf_lh[i])
        phiio_lh.append(phiosf_lh[i])
        phiga_lh.append(phigasf_lh[i])
        phieu_lh.append(phieusf_lh[i])
        t_lh.append(t90sf_lh[i])
        f_lh.append(f90sf_lh[i])
        i_lh.append(i90sf_lh[i])
        s_lh.append(s90sf_lh[i])
        sig_lh.append(sig90sf_lh[i])
        chi_lh.append(chi90sf_lh[i])
        snr_lh.append(snr90sf_lh[i])

for i in range(nrh):
    if (snr90sf_rh[i] >= 6.):
        cml_rh.append(cmlsf_rh[i])
        phiio_rh.append(phiosf_rh[i])
        phiga_rh.append(phigasf_rh[i])
        phieu_rh.append(phieusf_rh[i])
        t_rh.append(t90sf_rh[i])
        f_rh.append(f90sf_rh[i])
        i_rh.append(i90sf_rh[i])
        s_rh.append(s90sf_rh[i])
        sig_rh.append(sig90sf_rh[i])
        chi_rh.append(chi90sf_rh[i])
        snr_rh.append(snr90sf_rh[i])

nlh=len(cml_lh) ; nrh=len(cml_rh)

markers=['^','x','+']

plt.figure(figsize=(20,9.5))
### CML vs PhiIo

#plt.suptitle('Fine structures occurencies (fit +/- 30) - '+month+'/'+year+' - NDA/JunoN', fontsize='x-large')
plt.subplot(121)
jup.io(cml_lh,phiio_lh,cml_lh, phiga_lh,cml_rh,phiio_rh,cml_rh, phiga_rh,'LH', markers)
# slope_lh=s90sf_lh,slope_rh=s90sf_rh,slope_max=-10.0,slope_min=-30.)

# CML vs PhiGa
plt.subplot(122)
jup.gan(cml_lh, phiga_lh,cml_lh,phiio_lh,cml_rh, phiga_rh,cml_rh,phiio_rh,'LH', markers )
#jup.europa(cml_lh,phieu_lh,cml_lh,phiio_lh,cml_lh,phiga_lh,cml_rh,phieu_rh,cml_rh,phiio_rh,cml_rh,phiga_rh)
# slope_lh=s90sf_lh,slope_rh=s90sf_rh,slope_max=-10.0,slope_min=-30.)

plt.tight_layout()
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_1.pdf', dpi=150)
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_1.eps', dpi=150)

###################################################
#------------------- Figure 2 --------------------#
###################################################

print('------ Figure 2 ------')

Io1=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Io_1.sav')
Io2=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Io_2.sav')
Gan2=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Gan_2.sav')
Gan3=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Gan_3.sav')
Aur2=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Aur_2.sav')
Aur3=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Aur_3.sav')

plt.figure(figsize=(25,20))
plt.subplot(321)
ax1=plt.gca()
im1=ax1.imshow(jup.scale_spdyn(Io1['xlh1']), origin='lower',extent=[0,(Io1['tmax']-Io1['tmin'])*3600,Io1['fmin'],Io1['fmax']],aspect=(Io1['tmax']-Io1['tmin'])*3600/(Io1['fmax']-Io1['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax1.tick_params(axis='both', which='major', labelsize=16)
plt.text(0.,17.1, 'a)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-06'.format(Io1['tmin']),fontsize=18)
plt.ylabel('Frequency [MHz]',fontsize=18)
plt.title('Io, <df/dt>={:.4}'.format(Io1['slope_lh']) + ' $MHz.s^{-1}$',fontsize=20)
cb1=plt.colorbar(im1, ax=ax1)
cb1.set_label('dB', fontsize=18)
cb1.ax.tick_params(labelsize=16)

plt.subplot(322)
ax2=plt.gca()
im2=ax2.imshow(jup.scale_spdyn(Io2['xlh1']), origin='lower',extent=[0,(Io2['tmax']-Io2['tmin'])*3600,Io2['fmin'],Io2['fmax']],aspect=(Io2['tmax']-Io2['tmin'])*3600/(Io2['fmax']-Io2['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax2.tick_params(axis='both', which='major', labelsize=16)
plt.text(0.,17.1, 'b)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-06'.format(Io2['tmin']),fontsize=18)
plt.ylabel('Frequency [MHz]',fontsize=18)
plt.title('Io, <df/dt>={:.4}'.format(Io2['slope_lh']) + ' $MHz.s^{-1}$',fontsize=20)
cb2=plt.colorbar(im2, ax=ax2)
cb2.set_label('dB', fontsize=18)
cb2.ax.tick_params(labelsize=16)

plt.subplot(323)
ax3=plt.gca()
im3=ax3.imshow(jup.scale_spdyn(Gan3['xlh1']), origin='lower',extent=[0,(Gan3['tmax']-Gan3['tmin'])*3600,Gan3['fmin'],Gan3['fmax']],aspect=(Gan3['tmax']-Gan3['tmin'])*3600/(Gan3['fmax']-Gan3['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax3.tick_params(axis='both', which='major', labelsize=16)
plt.text(0.,17.1, 'c)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-17'.format(Gan3['tmin']),fontsize=18)
plt.ylabel('Frequency [MHz]',fontsize=18)
plt.title('Gan, <df/dt>={:.4}'.format(Gan3['slope_lh']) + ' $MHz.s^{-1}$',fontsize=20)
cb3=plt.colorbar(im3, ax=ax3)
cb3.set_label('dB', fontsize=18)
cb3.ax.tick_params(labelsize=16)

plt.subplot(324)
ax4=plt.gca()
im4=ax4.imshow(jup.scale_spdyn(Gan2['xlh1']), origin='lower',extent=[0,(Gan2['tmax']-Gan2['tmin'])*3600,Gan2['fmin'],Gan2['fmax']],aspect=(Gan2['tmax']-Gan2['tmin'])*3600/(Gan2['fmax']-Gan2['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax4.tick_params(axis='both', which='major', labelsize=16)
plt.text(0.,17.1, 'd)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-17'.format(Gan2['tmin']),fontsize=18)
plt.ylabel('Frequency [MHz]',fontsize=18)
plt.title('Gan, <df/dt>={:.4}'.format(Gan2['slope_lh']) + ' $MHz.s^{-1}$',fontsize=20)
cb4=plt.colorbar(im4, ax=ax4)
cb4.set_label('dB', fontsize=18)
cb4.ax.tick_params(labelsize=16)

plt.subplot(325)
ax5=plt.gca()
im5=ax5.imshow(jup.scale_spdyn(Aur3['xlh1']), origin='lower',extent=[0,(Aur3['tmax']-Aur3['tmin'])*3600,Aur3['fmin'],Aur3['fmax']],aspect=(Aur3['tmax']-Aur3['tmin'])*3600/(Aur3['fmax']-Aur3['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax5.tick_params(axis='both', which='major', labelsize=16)
plt.text(0.,17.1, 'e)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-15'.format(Aur3['tmin']),fontsize=18)
plt.ylabel('Frequency [MHz]',fontsize=18)
plt.title('Aur, <df/dt>={:.4}'.format(Aur3['slope_lh']) + ' $MHz.s^{-1}$',fontsize=20)
cb5=plt.colorbar(im5, ax=ax5)
cb5.set_label('dB', fontsize=18)
cb5.ax.tick_params(labelsize=16)

plt.subplot(326)
ax6=plt.gca()
im6=ax6.imshow(jup.scale_spdyn(Aur2['xrh1']), origin='lower',extent=[0,(Aur2['tmax']-Aur2['tmin'])*3600,Aur2['fmin'],Aur2['fmax']],aspect=(Aur2['tmax']-Aur2['tmin'])*3600/(Aur2['fmax']-Aur2['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax6.tick_params(axis='both', which='major', labelsize=16)
plt.text(0.,17.1, 'f)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-15'.format(Aur2['tmin']),fontsize=18)
plt.ylabel('Frequency [MHz]',fontsize=18)
plt.title('Aur, <df/dt>={:.4}'.format(Aur2['slope_rh']) + ' $MHz.s^{-1}$',fontsize=20)
cb6=plt.colorbar(im6, ax=ax6)
cb6.set_label('dB', fontsize=18)
cb6.ax.tick_params(labelsize=16)

plt.tight_layout()
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_2.pdf', dpi=150)
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_2.eps', dpi=150)



###################################################
#----------------- Figure 2 bis ------------------#
###################################################

print('------ Figure 2 bis ------')

Io1=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Io_1.sav')
Io2=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Io_2.sav')
Gan2=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Gan_2.sav')
Gan3=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Gan_3.sav')
Aur2=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Aur_2.sav')
Aur3=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Aur_3.sav')

plt.figure(figsize=(20,10))
plt.subplot(231)
ax1=plt.gca()
im1=ax1.imshow(jup.scale_spdyn(Io1['xlh1']), origin='lower',extent=[0,(Io1['tmax']-Io1['tmin'])*3600,Io1['fmin'],Io1['fmax']],aspect=(Io1['tmax']-Io1['tmin'])*3600/(Io1['fmax']-Io1['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax1.tick_params(axis='both', which='major', labelsize=16)
plt.text(-0.1,17.15, 'a)', color='black',fontsize=20,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-06'.format(Io1['tmin']),fontsize=18)
plt.ylabel('Frequency [MHz]',fontsize=18)
plt.title('Io, <df/dt>={:.3}'.format(Io1['slope_lh']) + ' $MHz.s^{-1}$',fontsize=20)
cb1=plt.colorbar(im1, ax=ax1)
cb1.set_label('dB', fontsize=18)
cb1.ax.tick_params(labelsize=16)

plt.subplot(234)
ax2=plt.gca()
im2=ax2.imshow(jup.scale_spdyn(Io2['xlh1']), origin='lower',extent=[0,(Io2['tmax']-Io2['tmin'])*3600,Io2['fmin'],Io2['fmax']],aspect=(Io2['tmax']-Io2['tmin'])*3600/(Io2['fmax']-Io2['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax2.tick_params(axis='both', which='major', labelsize=16)
plt.text(-0.1,17.15, 'b)', color='black',fontsize=20,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-06'.format(Io2['tmin']),fontsize=18)
plt.ylabel('Frequency [MHz]',fontsize=18)
plt.title('Io, <df/dt>={:.3}'.format(Io2['slope_lh']) + ' $MHz.s^{-1}$',fontsize=20)
cb2=plt.colorbar(im2, ax=ax2)
cb2.set_label('dB', fontsize=18)
cb2.ax.tick_params(labelsize=16)

plt.subplot(232)
ax3=plt.gca()
im3=ax3.imshow(jup.scale_spdyn(Gan3['xlh1']), origin='lower',extent=[0,(Gan3['tmax']-Gan3['tmin'])*3600,Gan3['fmin'],Gan3['fmax']],aspect=(Gan3['tmax']-Gan3['tmin'])*3600/(Gan3['fmax']-Gan3['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax3.tick_params(axis='both', which='major', labelsize=16)
plt.text(-0.15,17.15, 'c)', color='black',fontsize=20,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-17'.format(Gan3['tmin']),fontsize=18)
plt.ylabel('Frequency [MHz]',fontsize=18)
plt.title('Gan, <df/dt>={:.3}'.format(Gan3['slope_lh']) + ' $MHz.s^{-1}$',fontsize=20)
cb3=plt.colorbar(im3, ax=ax3)
cb3.set_label('dB', fontsize=18)
cb3.ax.tick_params(labelsize=16)

plt.subplot(235)
ax4=plt.gca()
im4=ax4.imshow(jup.scale_spdyn(Gan2['xlh1']), origin='lower',extent=[0,(Gan2['tmax']-Gan2['tmin'])*3600,Gan2['fmin'],Gan2['fmax']],aspect=(Gan2['tmax']-Gan2['tmin'])*3600/(Gan2['fmax']-Gan2['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax4.tick_params(axis='both', which='major', labelsize=16)
plt.text(-0.15,17.15, 'd)', color='black',fontsize=20,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-17'.format(Gan2['tmin']),fontsize=18)
plt.ylabel('Frequency [MHz]',fontsize=18)
plt.title('Gan, <df/dt>={:.3}'.format(Gan2['slope_lh']) + ' $MHz.s^{-1}$',fontsize=20)
cb4=plt.colorbar(im4, ax=ax4)
cb4.set_label('dB', fontsize=18)
cb4.ax.tick_params(labelsize=16)

plt.subplot(233)
ax5=plt.gca()
im5=ax5.imshow(jup.scale_spdyn(Aur3['xlh1']), origin='lower',extent=[0,(Aur3['tmax']-Aur3['tmin'])*3600,Aur3['fmin'],Aur3['fmax']],aspect=(Aur3['tmax']-Aur3['tmin'])*3600/(Aur3['fmax']-Aur3['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax5.tick_params(axis='both', which='major', labelsize=16)
plt.text(-0.15,17.15, 'e)', color='black',fontsize=20,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-15'.format(Aur3['tmin']),fontsize=18)
plt.ylabel('Frequency [MHz]',fontsize=18)
plt.title('Aur, <df/dt>={:.3}'.format(Aur3['slope_lh']) + ' $MHz.s^{-1}$',fontsize=20)
cb5=plt.colorbar(im5, ax=ax5)
cb5.set_label('dB', fontsize=18)
cb5.ax.tick_params(labelsize=16)

plt.subplot(236)
ax6=plt.gca()
im6=ax6.imshow(jup.scale_spdyn(Aur2['xrh1']), origin='lower',extent=[0,(Aur2['tmax']-Aur2['tmin'])*3600,Aur2['fmin'],Aur2['fmax']],aspect=(Aur2['tmax']-Aur2['tmin'])*3600/(Aur2['fmax']-Aur2['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax6.tick_params(axis='both', which='major', labelsize=16)
plt.text(-0.15,17.15, 'f)', color='black',fontsize=20,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-15'.format(Aur2['tmin']),fontsize=18)
plt.ylabel('Frequency [MHz]',fontsize=18)
plt.title('Aur, <df/dt>={:.3}'.format(Aur2['slope_rh']) + ' $MHz.s^{-1}$',fontsize=20)
cb6=plt.colorbar(im6, ax=ax6)
cb6.set_label('dB', fontsize=18)
cb6.ax.tick_params(labelsize=16)

plt.tight_layout()
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_2_bis.pdf', dpi=150)
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_2_bis.eps', dpi=150)


###################################################
#------------------- Figure 3 --------------------#
###################################################

print('------ Figure 3 ------')

ti1_lh=[] ; ti2_lh=[] ; ti3_lh=[]
si1_lh=[] ; si2_lh=[] ; si3_lh=[]
Ii1_lh=[] ; Ii2_lh=[] ; Ii3_lh=[]
snri1_lh=[] ; snri2_lh=[] ; snri3_lh=[]

print('LH nombre detections total =', len(cml_lh))
print('RH nombre detections total =', len(cml_rh))
spos_lh=0
for i in range (nlh):
    if (jup.inboxio(cml_lh[i], phiio_lh[i])==True):
        spos_lh+=1
        if ((-35 <= s_lh[i]) and (s_lh[i] <= -10)):
            ti1_lh.append(t_lh[i])
            si1_lh.append(s_lh[i])
            Ii1_lh.append(i_lh[i])
            snri1_lh.append(snr_lh[i])
        elif ((s_lh[i] > -10.) and(s_lh[i] <= 0)):
            ti2_lh.append(t_lh[i])
            si2_lh.append(s_lh[i])
            Ii2_lh.append(i_lh[i])
            snri2_lh.append(snr_lh[i])
        elif ((s_lh[i] > 0.) and(s_lh[i] <= 20)) : 
            ti3_lh.append(t_lh[i])
            si3_lh.append(s_lh[i])
            Ii3_lh.append(i_lh[i])
            snri3_lh.append(snr_lh[i])

perc_sipos_lh = len(si3_lh)/spos_lh
                
ti1_rh=[] ; ti2_rh=[] ; ti3_rh=[]        
si1_rh=[] ; si2_rh=[] ; si3_rh=[]
Ii1_rh=[] ; Ii2_rh=[] ; Ii3_rh=[]
snri1_rh=[] ; snri2_rh=[] ; snri3_rh=[]

spos_rh=0

for i in range(nrh):
    if (jup.inboxio(cml_rh[i], phiio_rh[i])==True):
        spos_rh+=1
        if ((-35 <= s_rh[i]) and (s_rh[i] <= -10)):
            ti1_rh.append(t_rh[i])
            si1_rh.append(s_rh[i])
            Ii1_rh.append(i_rh[i])
            snri1_rh.append(snr_rh[i])
        elif ((s_rh[i] > -10.) and(s_rh[i] <= 0)):
            ti2_rh.append(t_rh[i])
            si2_rh.append(s_rh[i])
            Ii2_rh.append(i_rh[i])
            snri2_rh.append(snr_rh[i])
        elif ((s_rh[i] > 0.) and(s_rh[i] <= 20)) : 
            ti3_rh.append(t_rh[i])
            si3_rh.append(s_rh[i])
            Ii3_rh.append(i_rh[i])
            snri3_rh.append(snr_rh[i])
            
perc_sipos_rh = len(si3_rh)/spos_rh
            
hist_Ii1_lh,xii1_lh=np.histogram(Ii1_lh,bins=500, range=(0,4))
hist_Ii1_rh,xii1_rh=np.histogram(Ii1_rh,bins=500, range=(0,4))
hist_Ii2_lh,xii2_lh=np.histogram(Ii2_lh,bins=500, range=(0,4))
hist_Ii2_rh,xii2_rh=np.histogram(Ii2_rh,bins=500, range=(0,4))
hist_Ii3_lh,xii3_lh=np.histogram(Ii3_lh,bins=500, range=(0,4))
hist_Ii3_rh,xii3_rh=np.histogram(Ii3_rh,bins=500, range=(0,4))

hist_si1_lh,xsi1_lh=np.histogram(si1_lh,bins=25,range=(-35.,-10.))
hist_si1_rh,xsi1_rh=np.histogram(si1_rh,bins=25,range=(-35.,-10.))
hist_si2_lh,xsi2_lh=np.histogram(si2_lh,bins=10,range=(-10.,0))
hist_si2_rh,xsi2_rh=np.histogram(si2_rh,bins=10,range=(-10.,0))
hist_si3_lh,xsi3_lh=np.histogram(si3_lh,bins=20,range=(0.,20.))
hist_si3_rh,xsi3_rh=np.histogram(si3_rh,bins=20,range=(0.,20.))


## Ganymède 

tg1_lh=[] ; tg2_lh=[] ; tg3_lh=[] 
sg1_lh=[] ; sg2_lh=[] ; sg3_lh=[] 
Ig1_lh=[] ; Ig2_lh=[] ; Ig3_lh=[] 
snrg1_lh=[] ; snrg2_lh=[] ; snrg3_lh=[] 


spos_lh=0
for i in range (nlh):
    if ((jup.inboxio(cml_lh[i], phiio_lh[i])==False) and (jup.inboxgan(cml_lh[i], phiga_lh[i])==True)):
        spos_lh+=1
        if ((-35 <= s_lh[i]) and (s_lh[i] <= -10)):
            tg1_lh.append(t_lh[i])
            sg1_lh.append(s_lh[i])
            Ig1_lh.append(i_lh[i])
            snrg1_lh.append(snr_lh[i])
        elif ((s_lh[i] > -10.0) and(s_lh[i] <= 0)):
            tg2_lh.append(t_lh[i])
            sg2_lh.append(s_lh[i])
            Ig2_lh.append(i_lh[i])
            snrg2_lh.append(snr_lh[i])
        elif ((s_lh[i] > 0.) and(s_lh[i] <= 20)) : 
            tg3_lh.append(t_lh[i])
            sg3_lh.append(s_lh[i])
            Ig3_lh.append(i_lh[i])
            snrg3_lh.append(snr_lh[i])

perc_sgpos_lh = len(sg3_lh)/spos_lh

tg1_rh=[] ; tg2_rh=[]; tg3_rh=[]     
sg1_rh=[] ; sg2_rh=[]; sg3_rh=[] 
Ig1_rh=[] ; Ig2_rh=[] ; Ig3_rh=[] 
snrg1_rh=[] ; snrg2_rh=[] ; snrg3_rh=[] 

spos_rh=0
for i in range(nrh):
    if ((jup.inboxio(cml_rh[i], phiio_rh[i])==False) and (jup.inboxgan(cml_rh[i], phiga_rh[i])==True)):
        spos_rh+=1
        if ((-35 <= s_rh[i]) and (s_rh[i] <= -10)):
            tg1_rh.append(t_rh[i])
            sg1_rh.append(s_rh[i])
            Ig1_rh.append(i_rh[i])
            snrg1_rh.append(snr_rh[i])
        elif ((s_rh[i] > -10.) and(s_rh[i] <= 0)):
            tg2_rh.append(t_rh[i])
            sg2_rh.append(s_rh[i])
            Ig2_rh.append(i_rh[i])
            snrg2_rh.append(snr_rh[i])
        elif ((s_rh[i] > 0.) and(s_rh[i] <= 20)) : 
            tg3_rh.append(t_rh[i])
            sg3_rh.append(s_rh[i])
            Ig3_rh.append(i_rh[i])
            snrg3_rh.append(snr_rh[i])
            
perc_sgpos_rh = len(sg3_rh)/spos_rh

hist_Ig1_lh,xig1_lh=np.histogram(Ig1_lh,bins=500, range=(0,4))
hist_Ig1_rh,xig1_rh=np.histogram(Ig1_rh,bins=500, range=(0,4))
hist_Ig2_lh,xig2_lh=np.histogram(Ig2_lh,bins=500, range=(0,4))
hist_Ig2_rh,xig2_rh=np.histogram(Ig2_rh,bins=500, range=(0,4))
hist_Ig3_lh,xig3_lh=np.histogram(Ig3_lh,bins=500, range=(0,4))
hist_Ig3_rh,xig3_rh=np.histogram(Ig3_rh,bins=500, range=(0,4))


hist_sg1_lh,xsg1_lh=np.histogram(sg1_lh,bins=25,range=(-35.,-10.))
hist_sg1_rh,xsg1_rh=np.histogram(sg1_rh,bins=25,range=(-35.,-10.))
hist_sg2_lh,xsg2_lh=np.histogram(sg2_lh,bins=10,range=(-10.,0))
hist_sg2_rh,xsg2_rh=np.histogram(sg2_rh,bins=10,range=(-10.,0))
hist_sg3_lh,xsg3_lh=np.histogram(sg3_lh,bins=20,range=(0.,20.))
hist_sg3_rh,xsg3_rh=np.histogram(sg3_rh,bins=20,range=(0.,20.))


## Aurores


ta1_lh=[] ; ta2_lh=[] ; ta3_lh=[] 
sa1_lh=[] ; sa2_lh=[] ; sa3_lh=[] 
Ia1_lh=[] ; Ia2_lh=[] ; Ia3_lh=[] 
snra1_lh=[] ; snra2_lh=[] ; snra3_lh=[] 

spos_lh=0

for i in range (nlh):
    if ((jup.inboxio(cml_lh[i], phiio_lh[i])==False) and (jup.inboxgan(cml_lh[i], phiga_lh[i])==False)):
        spos_lh+=1
        if ((-35 <= s_lh[i]) and (s_lh[i] <= -10)):
            ta1_lh.append(t_lh[i])
            sa1_lh.append(s_lh[i])
            Ia1_lh.append(i_lh[i])
            snra1_lh.append(snr_lh[i])
        elif ((s_lh[i] > -10.) and(s_lh[i] <= -0)):
            ta2_lh.append(t_lh[i])
            sa2_lh.append(s_lh[i])
            Ia2_lh.append(i_lh[i])
            snra2_lh.append(snr_lh[i])
        elif ((s_lh[i] > 0.) and(s_lh[i] <= 20)) : 
            ta3_lh.append(t_lh[i])
            sa3_lh.append(s_lh[i])
            Ia3_lh.append(i_lh[i])
            snra3_lh.append(snr_lh[i])

perc_sapos_lh = len(sa3_lh)/spos_lh      

ta1_rh=[] ; ta2_rh=[]; ta3_rh=[]       
sa1_rh=[] ; sa2_rh=[]; sa3_rh=[] 
Ia1_rh=[] ; Ia2_rh=[] ; Ia3_rh=[] 
snra1_rh=[] ; snra2_rh=[] ; snra3_rh=[]

spos_rh=0

for i in range(nrh):
    if ((jup.inboxio(cml_rh[i], phiio_rh[i])==False) and (jup.inboxgan(cml_rh[i], phiga_rh[i])==False)):
        spos_rh+=1
        if ((-35 <= s_rh[i]) and (s_rh[i] <= -10)):
            ta1_rh.append(t_rh[i])
            sa1_rh.append(s_rh[i])
            Ia1_rh.append(i_rh[i])
            snra1_rh.append(snr_rh[i])
        elif ((s_rh[i] > -10.) and(s_rh[i] <= 0)):
            ta2_rh.append(t_rh[i])
            sa2_rh.append(s_rh[i])
            Ia2_rh.append(i_rh[i])
            snra2_rh.append(snr_rh[i])
        elif ((s_rh[i] > 0.) and(s_rh[i] <= 20)) : 
            ta3_rh.append(t_rh[i])
            sa3_rh.append(s_rh[i])
            Ia3_rh.append(i_rh[i])
            snra3_rh.append(snr_rh[i])

perc_sapos_rh = len(sa3_rh)/spos_rh 


hist_Ia1_lh,xia1_lh=np.histogram(Ia1_lh,bins=500, range=(0,4))
hist_Ia1_rh,xia1_rh=np.histogram(Ia1_rh,bins=500, range=(0,4))
hist_Ia2_lh,xia2_lh=np.histogram(Ia2_lh,bins=500, range=(0,4))
hist_Ia2_rh,xia2_rh=np.histogram(Ia2_rh,bins=500, range=(0,4))
hist_Ia3_lh,xia3_lh=np.histogram(Ia3_lh,bins=500, range=(0,4))
hist_Ia3_rh,xia3_rh=np.histogram(Ia3_rh,bins=500, range=(0,4))


hist_sa1_lh,xsa1_lh=np.histogram(sa1_lh,bins=25,range=(-35.,-10.))
hist_sa1_rh,xsa1_rh=np.histogram(sa1_rh,bins=25,range=(-35.,-10.))
hist_sa2_lh,xsa2_lh=np.histogram(sa2_lh,bins=10,range=(-10.,0))
hist_sa2_rh,xsa2_rh=np.histogram(sa2_rh,bins=10,range=(-10.,0))
hist_sa3_lh,xsa3_lh=np.histogram(sa3_lh,bins=20,range=(0.,20.))
hist_sa3_rh,xsa3_rh=np.histogram(sa3_rh,bins=20,range=(0.,20.))

print('LH nombre detections total =', len(cml_lh))
print('RH nombre detections total =', len(cml_rh))

print('LH Io bleu N=', len(si1_lh))
print('RH Io bleu N=', len(si1_rh))
print('LH Io orange N=', len(si2_lh))
print('RH Io orange N=', len(si2_rh))
print('LH Io vert N=', len(si3_lh))
print('RH Io vert N=', len(si3_rh))

print('LH Gan bleu N=', len(sg1_lh))
print('RH Gan bleu N=', len(sg1_rh))
print('LH Gan orange N=', len(sg2_lh))
print('RH Gan orange N=', len(sg2_rh))
print('LH Gan vert N=', len(sg3_lh))
print('RH Gan vert N=', len(sg3_rh))

print('LH Aur bleu N=', len(sa1_lh))
print('RH Aur bleu N=', len(sa1_rh))
print('LH Aur orange N=', len(sa2_lh))
print('RH Aur orange N=', len(sa2_rh))
print('LH Aur vert N=', len(sa3_lh))
print('RH Aur vert N=', len(sa3_rh))

plt.figure(figsize=(20,15))

plt.subplot(321)
ax1=plt.gca()
ax1.plot(xsi1_lh[1:],hist_si1_lh,drawstyle='steps-mid', alpha=1)
ax1.plot(xsi2_lh[1:],hist_si2_lh,drawstyle='steps-mid', alpha=1)
ax1.plot(xsi3_lh[1:],hist_si3_lh,drawstyle='steps-mid', alpha=1)
ax1.tick_params(axis='both', which='major', labelsize=16)
plt.text(-35,1555, 'a)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.xlim(-35,20)
plt.grid()
plt.title('Io (LH)',fontsize=20)

plt.subplot(322)
ax2=plt.gca()
ax2.plot(xsi1_rh[1:],hist_si1_rh,drawstyle='steps-mid', alpha=1)
ax2.plot(xsi2_rh[1:],hist_si2_rh,drawstyle='steps-mid', alpha=1)
ax2.plot(xsi3_rh[1:],hist_si3_rh,drawstyle='steps-mid', alpha=1)
ax2.tick_params(axis='both', which='major', labelsize=16)
plt.text(-35,2650, 'b)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.xlim(-35,20)
plt.grid()
plt.title('Io (RH)',fontsize=20)

plt.subplot(323)
ax3=plt.gca()
ax3.plot(xsg1_lh[1:],hist_sg1_lh,drawstyle='steps-mid', alpha=1)
ax3.plot(xsg2_lh[1:],hist_sg2_lh,drawstyle='steps-mid', alpha=1)
ax3.plot(xsg3_lh[1:],hist_sg3_lh,drawstyle='steps-mid', alpha=1)
ax3.tick_params(axis='both', which='major', labelsize=16)
plt.text(-35,275, 'c)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.xlim(-35,20)
plt.grid()
plt.title('Ganymede (LH)',fontsize=20)

plt.subplot(324)
ax4=plt.gca()
ax4.plot(xsg1_rh[1:],hist_sg1_rh,drawstyle='steps-mid', alpha=1)
ax4.plot(xsg2_rh[1:],hist_sg2_rh,drawstyle='steps-mid', alpha=1)
ax4.plot(xsg3_rh[1:],hist_sg3_rh,drawstyle='steps-mid', alpha=1)
ax4.tick_params(axis='both', which='major', labelsize=16)
plt.text(-35,175, 'd)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.xlim(-35,20)
plt.grid()
plt.title('Ganymede (RH)',fontsize=20)

plt.subplot(325)
ax5=plt.gca()
ax5.plot(xsa1_lh[1:],hist_sa1_lh,drawstyle='steps-mid', alpha=1)
ax5.plot(xsa2_lh[1:],hist_sa2_lh,drawstyle='steps-mid', alpha=1)
ax5.plot(xsa3_lh[1:],hist_sa3_lh,drawstyle='steps-mid', alpha=1)
ax5.tick_params(axis='both', which='major', labelsize=16)
plt.text(-35,320, 'e)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.xlim(-35,20)
plt.grid()
plt.title('Main aurora (LH)',fontsize=20)

plt.subplot(326)
ax6=plt.gca()
ax6.plot(xsa1_rh[1:],hist_sa1_rh,drawstyle='steps-mid', alpha=1)
ax6.plot(xsa2_rh[1:],hist_sa2_rh,drawstyle='steps-mid', alpha=1)
ax6.plot(xsa3_rh[1:],hist_sa3_rh,drawstyle='steps-mid', alpha=1)
ax6.tick_params(axis='both', which='major', labelsize=16)
plt.text(-35,815, 'f)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.xlim(-35,20)
plt.grid()
plt.title('Main aurora (RH)',fontsize=20)

plt.tight_layout()
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_3.pdf', dpi=150)
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_3.eps', dpi=150)


###################################################
#------------------- Figure 4 --------------------#
###################################################

print('------ Figure 4 ------')

Io3=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Io_traitement_3.sav')
data=readsav(r'rdbox.sav')
tmin_tf=-((420-1)/2)/(420*2.6e-3) ; tmax_tf=((420-1)/2)/(420*2.6e-3)
fmin_tf=-((420-1)/2)/(420*21.35e-3) ; fmax_tf=((420-1)/2)/(420*21.35e-3)

plt.figure(figsize=(20,10))
plt.subplot(231)
ax1=plt.gca()
im1=ax1.imshow(np.log10(Io3['rhs']), origin='lower',extent=[0,(Io3['tmax']-Io3['tmin'])*3600,Io3['fmin'],Io3['fmax']],aspect=(Io3['tmax']-Io3['tmin'])*3600/(Io3['fmax']-Io3['fmin']),cmap='gray', alpha=1)
ax1.tick_params(axis='both', which='major', labelsize=16)
plt.text(0.01,17.2, 'a)', color='black',fontsize=16,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h'.format(Io3['tmin']),fontsize=18)
plt.ylabel('Frequency [MHz]',fontsize=18)
plt.title('SPDYN',fontsize=20)
cb1=plt.colorbar(im1, ax=ax1)
cb1.set_label('dB', fontsize=18)
cb1.ax.tick_params(labelsize=16)

plt.subplot(234)
ax4=plt.gca()
im4=ax4.imshow(jup.scale_spdyn(Io3['xrh1']), origin='lower',extent=[0,(Io3['tmax']-Io3['tmin'])*3600,Io3['fmin'],Io3['fmax']],aspect=(Io3['tmax']-Io3['tmin'])*3600/(Io3['fmax']-Io3['fmin']),cmap='gray', alpha=1)
ax4.tick_params(axis='both', which='major', labelsize=16)
plt.text(-0.1,17.2, 'b)', color='black',fontsize=16,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h'.format(Io3['tmin']),fontsize=18)
plt.ylabel('Frequency [MHz]',fontsize=18)
plt.title('$SPDYN_{corr}$,'+' s={:.3}'.format(Io3['slope_rh']) + ' $MHz.s^{-1}$',fontsize=20)
cb4=plt.colorbar(im4, ax=ax4)
cb4.set_label('dB', fontsize=18)
cb4.ax.tick_params(labelsize=16)


plt.subplot(232)

ax2=plt.gca()
im2=ax2.imshow(np.log10(Io3['tfrh1o']), origin='lower',extent=[tmin_tf,tmax_tf,fmin_tf,fmax_tf],aspect=(tmax_tf-tmin_tf)/(fmax_tf-fmin_tf),cmap='magma',alpha=1)
ax2.tick_params(axis='both', which='major', labelsize=16)
plt.text(-190,24.4, 'c)', color='black',fontsize=16,fontweight='bold')
plt.xlabel('Time$^{-1}$ [$s^{-1}$]',fontsize=18)
plt.ylabel('Frequency$^{-1}$ [$MHz^{-1}$]',fontsize=18)
plt.title('TF(SPDYN)',fontsize=20)
cb2=plt.colorbar(im2, ax=ax2)
cb2.set_label('dB', fontsize=18)
cb2.ax.tick_params(labelsize=16)

plt.subplot(235)

ax5=plt.gca()
im5=ax5.imshow(np.log10(Io3['tfrh1']), origin='lower',extent=[tmin_tf,tmax_tf,fmin_tf,fmax_tf],aspect=(tmax_tf-tmin_tf)/(fmax_tf-fmin_tf), vmin=-3.,cmap='magma',alpha=1)
ax5.tick_params(axis='both', which='major', labelsize=16)
plt.text(-190,24.4, 'd)', color='black',fontsize=16,fontweight='bold')
plt.xlabel('Time$^{-1}$ [$s^{-1}$]',fontsize=18)
plt.ylabel('Frequency$^{-1}$ [$MHz^{-1}$]',fontsize=18)
plt.title('$TF(SPDYN)_{corr}$',fontsize=20)
cb5=plt.colorbar(im5, ax=ax5)
cb5.set_label('dB', fontsize=18)
cb5.ax.tick_params(labelsize=16)

plt.subplot(233)
ax3=plt.gca()
ax3.plot(np.linspace(0,180,264),Io3['rd_rh1_o'], 'g-', linewidth=1, label='$RD_{original}$')
ax3.plot(data['x'],data['y'], color='orange',linestyle='--', linewidth=1.5, label='$RD_{box of ones}$')
ax3.plot([-1,181],[0,0], color='black', linestyle='dashed', linewidth=1)
ax3.tick_params(axis='both', which='major', labelsize=16)
plt.text(1,1370, 'e)', color='black',fontsize=16,fontweight='bold')
plt.xlim(0,180)
plt.xlabel("Angles [°]",fontsize=18)
plt.ylabel("Intensity ",fontsize=18)
plt.legend()
plt.grid()
plt.title('RD(TF)',fontsize=20)

plt.subplot(236)
ax6=plt.gca()
ax6.plot(Io3['theta_rd'],Io3['rd_rh1o'], 'g--', linewidth=1, label='$RD_{original,corrected}$')
ax6.plot([-1,121],[0,0], color='black', linestyle='dashed', linewidth=1)
ax6.plot([60,60],[-0.3,1.1], color='black', linestyle='dashdot', linewidth=1)
ax6.plot(Io3['theta_rd'],Io3['rd_rh1'],'b-' ,linewidth=2,label='$RD_{centered}$')
ax6.plot(Io3['theta_rd'], Io3['fit_rh_all'], 'r--', linewidth=1, label='Gaussian Fit')
ax6.tick_params(axis='both', which='major', labelsize=16)
plt.text(0.1,1.12, 'f)', color='black',fontsize=16,fontweight='bold')
plt.xlim(0,120)
plt.ylim(-0.3,1.1)
plt.xlabel("Angles [°]",fontsize=18)
plt.xticks([0,20,40,60,80,100,120],[15,35,55,'75//105',125,145,165])
plt.ylabel("Intensity ",fontsize=18)
plt.legend()
plt.grid()
plt.title('$RD(TF)_{corr}$,'+' SNR={:.4}'.format(Io3['snr_rh']),fontsize=20)

plt.tight_layout()
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_4.pdf', dpi=150)
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_4.eps', dpi=150)


###################################################
#------------------- Figure 5 --------------------#
###################################################

print('------ Figure 5 ------')

NDet=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_no_detect.sav')

tmin_tf=-((420-1)/2)/(420*2.6e-3) ; tmax_tf=((420-1)/2)/(420*2.6e-3)
fmin_tf=-((420-1)/2)/(420*21.35e-3) ; fmax_tf=((420-1)/2)/(420*21.35e-3)


plt.figure(figsize=(20,5))
plt.subplot(131)
ax1=plt.gca()
im1=ax1.imshow(jup.scale_spdyn(NDet['xlh1']), origin='lower',extent=[0,(NDet['tmax']-NDet['tmin'])*3600,NDet['fmin'],NDet['fmax']],aspect=(NDet['tmax']-NDet['tmin'])*3600/(NDet['fmax']-NDet['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax1.tick_params(axis='both', which='major', labelsize=16)
plt.xlabel('Time [s] from {:.6} h'.format(NDet['tmin']),fontsize=18)
plt.ylabel('Frequency [MHz]',fontsize=18)
plt.title('No signal, <df/dt>={:.4}'.format(NDet['slope_lh']) + ' $MHz.s^{-1}$',fontsize=20)
cb1=plt.colorbar(im1, ax=ax1)
cb1.set_label('dB', fontsize=18)
cb1.ax.tick_params(labelsize=16)


plt.subplot(132)

ax2=plt.gca()
im2=ax2.imshow(np.log10(NDet['tflh1']), origin='lower',extent=[tmin_tf,tmax_tf,fmin_tf,fmax_tf],aspect=(tmax_tf-tmin_tf)/(fmax_tf-fmin_tf),vmin=-3.,cmap='magma',alpha=1)
ax2.tick_params(axis='both', which='major', labelsize=16)
plt.xlabel('Time$^{-1}$ [$s^{-1}$]',fontsize=18)
plt.ylabel('Frequency$^{-1}$ [$MHz^{-1}$]',fontsize=18)
plt.title('TF(SPDYN)',fontsize=20)
cb2=plt.colorbar(im2, ax=ax2)
cb2.set_label('dB', fontsize=18)
cb2.ax.tick_params(labelsize=16)

plt.subplot(133)
ax3=plt.gca()
ax3.plot(NDet['theta_rd'],NDet['rd_lh1o'], 'g--', linewidth=1, label='$RD_{original}$')
ax3.plot([-1,121],[0,0], color='black', linestyle='dashed', linewidth=1)
ax3.plot([60,60],[-0.045,0.06], color='black', linestyle='dashdot', linewidth=1)
ax3.plot(NDet['theta_rd'],NDet['rd_lh1'],'b-' ,linewidth=2,label='$RD_{centered}$')
ax3.plot(NDet['theta_rd'], NDet['fit_lh_all'], 'r--', linewidth=1, label='Gaussian Fit')
ax3.tick_params(axis='both', which='major', labelsize=16)
plt.xlim(0,120)
plt.ylim(-0.045,0.06)
plt.xlabel("Angles [°]",fontsize=18)
plt.xticks([0,20,40,60,80,100,120],[15,35,55,'75//105',125,145,165])
plt.ylabel("Intensity ",fontsize=18)
plt.legend()
plt.grid()
plt.title('RD(TF), SNR={:.5}'.format(NDet['snr_lh']),fontsize=20)

plt.tight_layout()
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_5.eps', dpi=150)
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_5.pdf', dpi=150)


###################################################
#------------------- Figure 6 --------------------#
###################################################

print('------ Figure 6 ------')

Ppos=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_pente_pos.sav')

tmin_tf=-((420-1)/2)/(420*2.6e-3) ; tmax_tf=((420-1)/2)/(420*2.6e-3)
fmin_tf=-((420-1)/2)/(420*21.35e-3) ; fmax_tf=((420-1)/2)/(420*21.35e-3)

plt.figure(figsize=(20,5))
plt.subplot(131)
ax1=plt.gca()
im1=ax1.imshow(jup.scale_spdyn(Ppos['xrh1']), origin='lower',extent=[0,(Ppos['tmax']-Ppos['tmin'])*3600,Ppos['fmin'],Ppos['fmax']],aspect=(Ppos['tmax']-Ppos['tmin'])*3600/(Ppos['fmax']-Ppos['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax1.tick_params(axis='both', which='major', labelsize=16)
plt.xlabel('Time [s] from {:.6} h'.format(Ppos['tmin']),fontsize=18)
plt.ylabel('Frequency [MHz]',fontsize=18)
plt.title('Positive drift, <df/dt>={:.4}'.format(Ppos['slope_rh']) + ' $MHz.s^{-1}$',fontsize=20)
cb1=plt.colorbar(im1, ax=ax1)
cb1.set_label('dB', fontsize=18)
cb1.ax.tick_params(labelsize=16)

plt.subplot(132)

ax2=plt.gca()
im2=ax2.imshow(np.log10(Ppos['tfrh1']), origin='lower',extent=[tmin_tf,tmax_tf,fmin_tf,fmax_tf],aspect=(tmax_tf-tmin_tf)/(fmax_tf-fmin_tf),vmin=-3.,cmap='magma',alpha=1)
ax2.tick_params(axis='both', which='major', labelsize=16)
plt.xlabel('Time$^{-1}$ [$s^{-1}$]',fontsize=18)
plt.ylabel('Frequency$^{-1}$ [$MHz^{-1}$]',fontsize=18)
plt.title('TF(SPDYN)',fontsize=20)
cb2=plt.colorbar(im2, ax=ax2)
cb2.set_label('dB', fontsize=18)
cb2.ax.tick_params(labelsize=16)

plt.subplot(133)
ax3=plt.gca()
ax3.plot(Ppos['theta_rd'],Ppos['rd_rh1o'], 'g--', linewidth=1, label='$RD_{original}$')
ax3.plot([-1,121],[0,0], color='black', linestyle='dashed', linewidth=1)
ax3.plot([60,60],[-0.04,0.11], color='black', linestyle='dashdot', linewidth=1)
ax3.plot(Ppos['theta_rd'],Ppos['rd_rh1'],'b-' ,linewidth=2,label='$RD_{centered}$')
ax3.plot(Ppos['theta_rd'], Ppos['fit_rh_all'], 'r--', linewidth=1, label='Gaussian Fit')
ax3.tick_params(axis='both', which='major', labelsize=16)
plt.xlim(0,120)
plt.ylim(-0.04,0.11)
plt.xlabel("Angles [°]",fontsize=18)
plt.xticks([0,20,40,60,80,100,120],[15,35,55,'75//105',125,145,165])
plt.ylabel("Intensity ",fontsize=18)
plt.legend()
plt.grid()
plt.title('RD(TF), SNR={:.5}'.format(Ppos['snr_rh']),fontsize=20)

plt.tight_layout()
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_6.eps', dpi=150)
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_6.pdf', dpi=150)


###################################################
#------------------- Figure 7 --------------------#
###################################################

print('------ Figure 7 ------')

hist_snri1_lh,xsnri1_lh=np.histogram(snri1_lh,bins=int(np.max(snri1_lh)-np.min(snri1_lh)))
hist_snri1_rh,xsnri1_rh=np.histogram(snri1_rh,bins=int(np.max(snri1_rh)-np.min(snri1_rh)))
hist_snri2_lh,xsnri2_lh=np.histogram(snri2_lh,bins=int(np.max(snri2_lh)-np.min(snri2_lh)))
hist_snri2_rh,xsnri2_rh=np.histogram(snri2_rh,bins=int(np.max(snri2_lh)-np.min(snri2_lh)))
hist_snri3_lh,xsnri3_lh=np.histogram(snri3_lh,bins=int(np.max(snri2_lh)-np.min(snri2_lh)))
hist_snri3_rh,xsnri3_rh=np.histogram(snri3_rh,bins=int(np.max(snri2_lh)-np.min(snri2_lh)))

hist_snrg1_lh,xsnrg1_lh=np.histogram(snrg1_lh,bins=int(np.max(snrg1_lh)-np.min(snrg1_lh)))
hist_snrg1_rh,xsnrg1_rh=np.histogram(snrg1_rh,bins=int(np.max(snrg1_rh)-np.min(snrg1_rh)))
hist_snrg2_lh,xsnrg2_lh=np.histogram(snrg2_lh,bins=int(np.max(snrg2_lh)-np.min(snrg2_lh)))
hist_snrg2_rh,xsnrg2_rh=np.histogram(snrg2_rh,bins=int(np.max(snrg2_rh)-np.min(snrg2_rh)))
hist_snrg3_lh,xsnrg3_lh=np.histogram(snrg3_lh,bins=int(np.max(snrg2_lh)-np.min(snrg2_lh)))
hist_snrg3_rh,xsnrg3_rh=np.histogram(snrg3_rh,bins=int(np.max(snrg2_rh)-np.min(snrg2_rh)))

hist_snra1_lh,xsnra1_lh=np.histogram(snra1_lh,bins=int(np.max(snra1_lh)-np.min(snra1_lh)))
hist_snra1_rh,xsnra1_rh=np.histogram(snra1_rh,bins=int(np.max(snra1_rh)-np.min(snra1_rh)))
hist_snra2_lh,xsnra2_lh=np.histogram(snra2_lh,bins=int(np.max(snra2_lh)-np.min(snra2_lh)))
hist_snra2_rh,xsnra2_rh=np.histogram(snra2_rh,bins=int(np.max(snra2_rh)-np.min(snra2_rh)))
hist_snra3_lh,xsnra3_lh=np.histogram(snra3_lh,bins=int(np.max(snra2_lh)-np.min(snra2_lh)))
hist_snra3_rh,xsnra3_rh=np.histogram(snra3_rh,bins=int(np.max(snra2_rh)-np.min(snra2_rh)))


plt.figure(figsize=(20,15))

plt.subplot(321)
ax1=plt.gca()
ax1.plot(xsnri1_lh[0:-1],hist_snri1_lh+1.,drawstyle='steps-mid', alpha=1, label='$ s \leq -10$ MHz.s$^{-1}$')
ax1.plot(xsnri2_lh[0:-1],hist_snri2_lh+1.,drawstyle='steps-mid', alpha=1,label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax1.plot(xsnri3_lh[0:-1],hist_snri3_lh+1.,drawstyle='steps-mid', alpha=1,label='$ s \geq 0$ MHz.s$^{-1}$')
ax1.tick_params(axis='both', which='major', labelsize=16)
plt.text(5,2900, 'a)', color='black',fontsize=20,fontweight='bold')
plt.xlim(5,40)
plt.xlabel('SNR',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.yscale('log')
plt.grid()
plt.legend()
plt.title('Io (LH)',fontsize=20)

plt.subplot(322)
ax2=plt.gca()
ax2.plot(xsnri1_rh[0:-1],hist_snri1_rh+1.,drawstyle='steps-mid', alpha=1,label='$ s \leq -10$ MHz.s$^{-1}$')
ax2.plot(xsnri2_rh[0:-1],hist_snri2_rh+1.,drawstyle='steps-mid', alpha=1,label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax2.plot(xsnri3_rh[0:-1],hist_snri3_rh+1.,drawstyle='steps-mid', alpha=1,label='$ s \geq 0$ MHz.s$^{-1}$')
ax2.tick_params(axis='both', which='major', labelsize=16)
plt.text(5,3100, 'b)', color='black',fontsize=20,fontweight='bold')
plt.xlim(5,40)
plt.xlabel('SNR',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.yscale('log')
plt.grid()
plt.legend()
plt.title('Io (RH)',fontsize=20)

plt.subplot(323)
ax3=plt.gca()
ax3.plot(xsnrg1_lh[0:-1],hist_snrg1_lh,drawstyle='steps-mid', alpha=1,label='$ s \leq -10$ MHz.s$^{-1}$')
ax3.plot(xsnrg2_lh[0:-1],hist_snrg2_lh,drawstyle='steps-mid', alpha=1,label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax3.plot(xsnrg3_lh[0:-1],hist_snrg3_lh,drawstyle='steps-mid', alpha=1,label='$ s \geq 0$ MHz.s$^{-1}$')
ax3.tick_params(axis='both', which='major', labelsize=16)
plt.text(5,245, 'c)', color='black',fontsize=20,fontweight='bold')
plt.xlabel('SNR',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.xlim(5,40)
#plt.yscale('log')
plt.grid()
plt.legend()
plt.title('Ganymede (LH)',fontsize=20)

plt.subplot(324)
ax4=plt.gca()
ax4.plot(xsnrg1_rh[0:-1],hist_snrg1_rh,drawstyle='steps-mid', alpha=1,label='$ s \leq -10$ MHz.s$^{-1}$')
ax4.plot(xsnrg2_rh[0:-1],hist_snrg2_rh,drawstyle='steps-mid', alpha=1,label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax4.plot(xsnrg3_rh[0:-1],hist_snrg3_rh,drawstyle='steps-mid', alpha=1,label='$ s \geq 0$ MHz.s$^{-1}$')
ax4.tick_params(axis='both', which='major', labelsize=16)
plt.text(5,110, 'd)', color='black',fontsize=20,fontweight='bold')
plt.xlabel('SNR',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.xlim(5,40)
#plt.yscale('log')
plt.grid()
plt.legend()
plt.title('Ganymede (RH)',fontsize=20)

plt.subplot(325)
ax5=plt.gca()
ax5.plot(xsnra1_lh[0:-1],hist_snra1_lh,drawstyle='steps-mid', alpha=1,label='$ s \leq -10$ MHz.s$^{-1}$')
ax5.plot(xsnra2_lh[0:-1],hist_snra2_lh,drawstyle='steps-mid', alpha=1,label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax5.plot(xsnra3_lh[0:-1],hist_snra3_lh,drawstyle='steps-mid', alpha=1,label='$ s \geq 0$ MHz.s$^{-1}$')
ax5.tick_params(axis='both', which='major', labelsize=16)
plt.text(5,290, 'e)', color='black',fontsize=20,fontweight='bold')
plt.xlim(5,40)
plt.xlabel('SNR',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
#plt.yscale('log')
plt.grid()
plt.legend()
plt.title('Main aurora (LH)',fontsize=20)

plt.subplot(326)
ax6=plt.gca()
ax6.plot(xsnra1_rh[0:-1],hist_snra1_rh,drawstyle='steps-mid', alpha=1,label='$ s \leq -10$ MHz.s$^{-1}$')
ax6.plot(xsnra2_rh[0:-1],hist_snra2_rh,drawstyle='steps-mid', alpha=1,label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax6.plot(xsnra3_rh[0:-1],hist_snra3_rh,drawstyle='steps-mid', alpha=1,label='$ s \geq 0$ MHz.s$^{-1}$')
ax6.tick_params(axis='both', which='major', labelsize=16)
plt.text(5,620, 'f)', color='black',fontsize=20,fontweight='bold')
plt.xlabel('SNR',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.xlim(5,40)
#plt.yscale('log')
plt.grid()
plt.legend()
plt.title('Main aurora (RH)',fontsize=20)

plt.tight_layout()
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_7.pdf', dpi=150)
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_7.eps', dpi=150)


###################################################
#------------------- Figure 8 --------------------#
###################################################

# Context observations, made by hand.


###################################################
#------------------- Figure 9 --------------------#
###################################################

print('------ Figure 9 ------')

ti1_lh=[] ; ti2_lh=[] ; ti3_lh=[]
fi1_lh=[] ; fi2_lh=[] ; fi3_lh=[]
si1_lh=[] ; si2_lh=[] ; si3_lh=[]
Ii1_lh=[] ; Ii2_lh=[] ; Ii3_lh=[]
snri1_lh=[] ; snri2_lh=[] ; snri3_lh=[]

RJ = np.float32(69911e3)  # m
L=8. ; Be=7. ; fe=2.8*Be
theta=np.linspace(0,179,179)*0.5 + 1.
ct=np.cos(theta*np.pi/180) ; st=np.sin(theta*np.pi/180)
R=L*(st**2)
f=fe*np.sqrt(1+3*(ct**2))/(R**3)
ct=ct[(R >=0.94) & (R<=1.6)] ; st=st[(R >=0.94) & (R<=1.6)]
f=f[(R >=0.94) & (R<=1.6)] ; R=R[(R >=0.94) & (R<=1.6)]
g=(ct/(st**2))*(3+5*(ct**2))/np.power((1+3*(ct**2)),1.5)

print(len(g),len(f))

print('LH nombre detections total =', len(cml_lh))
print('RH nombre detections total =', len(cml_rh))
spos_lh=0
for i in range (nlh):
    if (jup.inboxio(cml_lh[i], phiio_lh[i])==True):
        spos_lh+=1
        if ((-35 <= s_lh[i]) and (s_lh[i] <= -10)):
            ti1_lh.append(t_lh[i])
            fi1_lh.append(f_lh[i])
            si1_lh.append(s_lh[i])
            Ii1_lh.append(i_lh[i])
            snri1_lh.append(snr_lh[i])
        elif ((s_lh[i] > -10.) and(s_lh[i] <= 0)):
            ti2_lh.append(t_lh[i])
            fi2_lh.append(f_lh[i])
            si2_lh.append(s_lh[i])
            Ii2_lh.append(i_lh[i])
            snri2_lh.append(snr_lh[i])
        elif ((s_lh[i] > 0.) and(s_lh[i] <= 20)) :
            ti3_lh.append(t_lh[i])
            fi3_lh.append(f_lh[i])
            si3_lh.append(s_lh[i])
            Ii3_lh.append(i_lh[i])
            snri3_lh.append(snr_lh[i])

perc_sipos_lh = len(si3_lh)/spos_lh
                
ti1_rh=[] ; ti2_rh=[] ; ti3_rh=[]    
fi1_rh=[] ; fi2_rh=[] ; fi3_rh=[]     
si1_rh=[] ; si2_rh=[] ; si3_rh=[]
Ii1_rh=[] ; Ii2_rh=[] ; Ii3_rh=[]
snri1_rh=[] ; snri2_rh=[] ; snri3_rh=[]

spos_rh=0

for i in range(nrh):
    if (jup.inboxio(cml_rh[i], phiio_rh[i])==True):
        spos_rh+=1
        if ((-35 <= s_rh[i]) and (s_rh[i] <= -10)):
            ti1_rh.append(t_rh[i])
            fi1_rh.append(f_rh[i])
            si1_rh.append(s_rh[i])
            Ii1_rh.append(i_rh[i])
            snri1_rh.append(snr_rh[i])
        elif ((s_rh[i] > -10.) and(s_rh[i] <= 0)):
            ti2_rh.append(t_rh[i])
            fi2_rh.append(f_rh[i])
            si2_rh.append(s_rh[i])
            Ii2_rh.append(i_rh[i])
            snri2_rh.append(snr_rh[i])
        elif ((s_rh[i] > 0.) and(s_rh[i] <= 20)):
            ti3_rh.append(t_rh[i])
            fi3_rh.append(f_rh[i])
            si3_rh.append(s_rh[i])
            Ii3_rh.append(i_rh[i])
            snri3_rh.append(snr_rh[i])
            
perc_sipos_rh = len(si3_rh)/spos_rh

fi1_lh =np.array(fi1_lh) ; fi2_lh =np.array(fi2_lh) ; fi3_lh =np.array(fi3_lh) 
fi1_rh =np.array(fi1_rh) ; fi2_rh =np.array(fi2_rh) ; fi3_rh =np.array(fi3_rh) 
si1_lh =np.array(si1_lh) ; si2_lh =np.array(si2_lh) ; si3_lh =np.array(si3_lh) 
si1_rh =np.array(si1_rh) ; si2_rh =np.array(si2_rh) ; si3_rh =np.array(si3_rh) 

gi1_lh=np.array([g[find_value(fi1_lh[i],f)] for i in range(len(fi1_lh))]) ; gi1_rh=np.array([g[find_value(fi1_rh[i],f)] for i in range(len(fi1_rh))])
gi2_lh=np.array([g[find_value(fi2_lh[i],f)] for i in range(len(fi2_lh))]) ; gi2_rh=np.array([g[find_value(fi2_rh[i],f)] for i in range(len(fi2_rh))])
gi3_lh=np.array([g[find_value(fi3_lh[i],f)] for i in range(len(fi3_lh))]) ; gi3_rh=np.array([g[find_value(fi3_rh[i],f)] for i in range(len(fi3_rh))])

vi1_lh = - si1_lh * RJ * L / (3 * fi1_lh * gi1_lh) ; vi2_lh = - si2_lh * RJ * L / (3*fi2_lh*gi2_lh) ; vi3_lh = si3_lh * RJ * L / (3*fi3_lh*gi3_lh)
vi1_rh = - si1_rh * RJ * L / (3 * fi1_rh * gi1_rh) ; vi2_rh = - si2_rh * RJ * L / (3*fi2_rh*gi2_rh) ; vi3_rh = si3_rh * RJ * L / (3*fi3_rh*gi3_rh)

Ei1_lh = 256. * np.power(vi1_lh/3e8,2) / (1-fi1_lh/40.) ; Ei2_lh = 256. * np.power(vi2_lh/3e8,2) / (1-fi2_lh/40.) ; Ei3_lh = 256. * np.power(vi3_lh/3e8,2) / (1-fi3_lh/40.)
Ei1_rh = 256. * np.power(vi1_rh/3e8,2) / (1-fi1_rh/40.) ; Ei2_rh = 256. * np.power(vi2_rh/3e8,2) / (1-fi2_rh/40.) ; Ei3_rh = 256. * np.power(vi3_rh/3e8,2) / (1-fi3_rh/40.)


hist_vi1_lh,xvi1_lh=np.histogram(np.abs(vi1_lh),bins=20)
hist_vi1_rh,xvi1_rh=np.histogram(np.abs(vi1_rh),bins=20)
hist_vi2_lh,xvi2_lh=np.histogram(np.abs(vi2_lh),bins=20)
hist_vi2_rh,xvi2_rh=np.histogram(np.abs(vi2_rh),bins=20)
hist_vi3_lh,xvi3_lh=np.histogram(np.abs(vi3_lh),bins=20)
hist_vi3_rh,xvi3_rh=np.histogram(np.abs(vi3_rh),bins=20)

print(np.min(Ei1_lh),np.max(Ei1_lh))

hist_Ei1_lh,xEi1_lh=np.histogram(Ei1_lh,bins=int(np.max(Ei1_lh)-np.min(Ei1_lh)))
hist_Ei1_rh,xEi1_rh=np.histogram(Ei1_rh,bins=int(np.max(Ei1_rh)-np.min(Ei1_rh)))
hist_Ei2_lh,xEi2_lh=np.histogram(Ei2_lh,bins=int((np.max(Ei2_lh)-np.min(Ei2_lh))/0.1))
hist_Ei2_rh,xEi2_rh=np.histogram(Ei2_rh,bins=int((np.max(Ei2_rh)-np.min(Ei2_rh))/0.1))
hist_Ei3_lh,xEi3_lh=np.histogram(Ei3_lh,bins=int((np.max(Ei3_lh)-np.min(Ei3_lh))/0.1))
hist_Ei3_rh,xEi3_rh=np.histogram(Ei3_rh,bins=int((np.max(Ei3_rh)-np.min(Ei3_rh))/0.1))

## Ganymède 

tg1_lh=[] ; tg2_lh=[] ; tg3_lh=[] 
fg1_lh=[] ; fg2_lh=[] ; fg3_lh=[] 
sg1_lh=[] ; sg2_lh=[] ; sg3_lh=[] 
Ig1_lh=[] ; Ig2_lh=[] ; Ig3_lh=[] 
snrg1_lh=[] ; snrg2_lh=[] ; snrg3_lh=[] 


spos_lh=0
for i in range (nlh):
    if ((jup.inboxio(cml_lh[i], phiio_lh[i])==False) and (jup.inboxgan(cml_lh[i], phiga_lh[i])==True)):
        spos_lh+=1
        if ((-35 <= s_lh[i]) and (s_lh[i] <= -10)):
            tg1_lh.append(t_lh[i])
            fg1_lh.append(f_lh[i])
            sg1_lh.append(s_lh[i])
            Ig1_lh.append(i_lh[i])
            snrg1_lh.append(snr_lh[i])
        elif ((s_lh[i] > -10.0) and(s_lh[i] <= 0)):
            tg2_lh.append(t_lh[i])
            fg2_lh.append(f_lh[i])
            sg2_lh.append(s_lh[i])
            Ig2_lh.append(i_lh[i])
            snrg2_lh.append(snr_lh[i])
        elif ((s_lh[i] > 0.) and(s_lh[i] <= 20)) : 
            tg3_lh.append(t_lh[i])
            fg3_lh.append(f_lh[i])
            sg3_lh.append(s_lh[i])
            Ig3_lh.append(i_lh[i])
            snrg3_lh.append(snr_lh[i])

perc_sgpos_lh = len(sg3_lh)/spos_lh

tg1_rh=[] ; tg2_rh=[]; tg3_rh=[]     
fg1_rh=[] ; fg2_rh=[]; fg3_rh=[]  
sg1_rh=[] ; sg2_rh=[]; sg3_rh=[] 
Ig1_rh=[] ; Ig2_rh=[] ; Ig3_rh=[] 
snrg1_rh=[] ; snrg2_rh=[] ; snrg3_rh=[] 

spos_rh=0
for i in range(nrh):
    if ((jup.inboxio(cml_rh[i], phiio_rh[i])==False) and (jup.inboxgan(cml_rh[i], phiga_rh[i])==True)):
        spos_rh+=1
        if ((-35 <= s_rh[i]) and (s_rh[i] <= -10)):
            tg1_rh.append(t_rh[i])
            fg1_rh.append(f_rh[i])
            sg1_rh.append(s_rh[i])
            Ig1_rh.append(i_rh[i])
            snrg1_rh.append(snr_rh[i])
        elif ((s_rh[i] > -10.) and(s_rh[i] <= 0)):
            tg2_rh.append(t_rh[i])
            fg2_rh.append(f_rh[i])
            sg2_rh.append(s_rh[i])
            Ig2_rh.append(i_rh[i])
            snrg2_rh.append(snr_rh[i])
        elif ((s_rh[i] > 0.) and(s_rh[i] <= 20)) :
            tg3_rh.append(t_rh[i])
            fg3_rh.append(f_rh[i])
            sg3_rh.append(s_rh[i])
            Ig3_rh.append(i_rh[i])
            snrg3_rh.append(snr_rh[i])
            
perc_sgpos_rh = len(sg3_rh)/spos_rh

fg1_lh =np.array(fg1_lh) ; fg2_lh =np.array(fg2_lh) ; fg3_lh =np.array(fg3_lh) 
fg1_rh =np.array(fg1_rh) ; fg2_rh =np.array(fg2_rh) ; fg3_rh =np.array(fg3_rh) 
sg1_lh =np.array(sg1_lh) ; sg2_lh =np.array(sg2_lh) ; sg3_lh =np.array(sg3_lh) 
sg1_rh =np.array(sg1_rh) ; sg2_rh =np.array(sg2_rh) ; sg3_rh =np.array(sg3_rh) 

gg1_lh=np.array([g[find_value(fg1_lh[i],f)] for i in range(len(fg1_lh))]) ; gg1_rh=np.array([g[find_value(fg1_rh[i],f)] for i in range(len(fg1_rh))])
gg2_lh=np.array([g[find_value(fg2_lh[i],f)] for i in range(len(fg2_lh))]) ; gg2_rh=np.array([g[find_value(fg2_rh[i],f)] for i in range(len(fg2_rh))])
gg3_lh=np.array([g[find_value(fg3_lh[i],f)] for i in range(len(fg3_lh))]) ; gg3_rh=np.array([g[find_value(fg3_rh[i],f)] for i in range(len(fg3_rh))])

vg1_lh = - sg1_lh * RJ * L / (3 * fg1_lh * gg1_lh) ; vg2_lh = - sg2_lh * RJ * L / (3*fg2_lh*gg2_lh) ; vg3_lh = sg3_lh * RJ * L / (3*fg3_lh*gg3_lh)
vg1_rh = - sg1_rh * RJ * L / (3 * fg1_rh * gg1_rh) ; vg2_rh = - sg2_rh * RJ * L / (3*fg2_rh*gg2_rh) ; vg3_rh = sg3_rh * RJ * L / (3*fg3_rh*gg3_rh)

Eg1_lh = 256. * np.power(vg1_lh/3e8,2) / (1-fg1_lh/40.) ; Eg2_lh = 256. * np.power(vg2_lh/3e8,2) / (1-fg2_lh/40.) ; Eg3_lh = 256. * np.power(vg3_lh/3e8,2) / (1-fg3_lh/40.)
Eg1_rh = 256. * np.power(vg1_rh/3e8,2) / (1-fg1_rh/40.) ; Eg2_rh = 256. * np.power(vg2_rh/3e8,2) / (1-fg2_rh/40.) ; Eg3_rh = 256. * np.power(vg3_rh/3e8,2) / (1-fg3_rh/40.)


hist_vg1_lh,xvg1_lh=np.histogram(np.abs(vg1_lh),bins=20)
hist_vg1_rh,xvg1_rh=np.histogram(np.abs(vg1_rh),bins=20)
hist_vg2_lh,xvg2_lh=np.histogram(np.abs(vg2_lh),bins=20)
hist_vg2_rh,xvg2_rh=np.histogram(np.abs(vg2_rh),bins=20)
hist_vg3_lh,xvg3_lh=np.histogram(np.abs(vg3_lh),bins=20)
hist_vg3_rh,xvg3_rh=np.histogram(np.abs(vg3_rh),bins=20)

hist_Eg1_lh,xEg1_lh=np.histogram(Eg1_lh,bins=int(np.max(Eg1_lh)-np.min(Eg1_lh)))
hist_Eg1_rh,xEg1_rh=np.histogram(Eg1_rh,bins=int(np.max(Eg1_rh)-np.min(Eg1_rh)))
hist_Eg2_lh,xEg2_lh=np.histogram(Eg2_lh,bins=int((np.max(Eg2_lh)-np.min(Eg2_lh))/0.1))
hist_Eg2_rh,xEg2_rh=np.histogram(Eg2_rh,bins=int((np.max(Eg2_rh)-np.min(Eg2_rh))/0.1))
hist_Eg3_lh,xEg3_lh=np.histogram(Eg3_lh,bins=int((np.max(Eg3_lh)-np.min(Eg3_lh))/0.1))
hist_Eg3_rh,xEg3_rh=np.histogram(Eg3_rh,bins=int((np.max(Eg3_rh)-np.min(Eg3_rh))/0.1))

## Aurores


ta1_lh=[] ; ta2_lh=[] ; ta3_lh=[] 
fa1_lh=[] ; fa2_lh=[] ; fa3_lh=[] 
sa1_lh=[] ; sa2_lh=[] ; sa3_lh=[] 
Ia1_lh=[] ; Ia2_lh=[] ; Ia3_lh=[] 
snra1_lh=[] ; snra2_lh=[] ; snra3_lh=[] 

spos_lh=0

for i in range (nlh):
    if ((jup.inboxio(cml_lh[i], phiio_lh[i])==False) and (jup.inboxgan(cml_lh[i], phiga_lh[i])==False)):
        spos_lh+=1
        if ((-35 <= s_lh[i]) and (s_lh[i] <= -10)):
            ta1_lh.append(t_lh[i])
            fa1_lh.append(f_lh[i])
            sa1_lh.append(s_lh[i])
            Ia1_lh.append(i_lh[i])
            snra1_lh.append(snr_lh[i])
        elif ((s_lh[i] > -10.) and(s_lh[i] <= -0)):
            ta2_lh.append(t_lh[i])
            fa2_lh.append(f_lh[i])
            sa2_lh.append(s_lh[i])
            Ia2_lh.append(i_lh[i])
            snra2_lh.append(snr_lh[i])
        elif ((s_lh[i] > 0.) and(s_lh[i] <= 20)) :
            ta3_lh.append(t_lh[i])
            fa3_lh.append(f_lh[i])
            sa3_lh.append(s_lh[i])
            Ia3_lh.append(i_lh[i])
            snra3_lh.append(snr_lh[i])

perc_sapos_lh = len(sa3_lh)/spos_lh      

ta1_rh=[] ; ta2_rh=[]; ta3_rh=[]
fa1_rh=[] ; fa2_rh=[]; fa3_rh=[]       
sa1_rh=[] ; sa2_rh=[]; sa3_rh=[] 
Ia1_rh=[] ; Ia2_rh=[] ; Ia3_rh=[] 
snra1_rh=[] ; snra2_rh=[] ; snra3_rh=[]

spos_rh=0

for i in range(nrh):
    if ((jup.inboxio(cml_rh[i], phiio_rh[i])==False) and (jup.inboxgan(cml_rh[i], phiga_rh[i])==False)):
        spos_rh+=1
        if ((-35 <= s_rh[i]) and (s_rh[i] <= -10)):
            ta1_rh.append(t_rh[i])
            fa1_rh.append(f_rh[i])
            sa1_rh.append(s_rh[i])
            Ia1_rh.append(i_rh[i])
            snra1_rh.append(snr_rh[i])
        elif ((s_rh[i] > -10.) and(s_rh[i] <= 0)):
            ta2_rh.append(t_rh[i])
            fa2_rh.append(f_rh[i])
            sa2_rh.append(s_rh[i])
            Ia2_rh.append(i_rh[i])
            snra2_rh.append(snr_rh[i])
        elif ((s_rh[i] > 0.) and(s_rh[i] <= 20)) :
            ta3_rh.append(t_rh[i])
            fa3_rh.append(f_rh[i])
            sa3_rh.append(s_rh[i])
            Ia3_rh.append(i_rh[i])
            snra3_rh.append(snr_rh[i])

perc_sapos_rh = len(sa3_rh)/spos_rh 

fa1_lh =np.array(fa1_lh) ; fa2_lh =np.array(fa2_lh) ; fa3_lh =np.array(fa3_lh) 
fa1_rh =np.array(fa1_rh) ; fa2_rh =np.array(fa2_rh) ; fa3_rh =np.array(fa3_rh) 
sa1_lh =np.array(sa1_lh) ; sa2_lh =np.array(sa2_lh) ; sa3_lh =np.array(sa3_lh) 
sa1_rh =np.array(sa1_rh) ; sa2_rh =np.array(sa2_rh) ; sa3_rh =np.array(sa3_rh) 

ga1_lh=np.array([g[find_value(fa1_lh[i],f)] for i in range(len(fa1_lh))]) ; ga1_rh=np.array([g[find_value(fa1_rh[i],f)] for i in range(len(fa1_rh))])
ga2_lh=np.array([g[find_value(fa2_lh[i],f)] for i in range(len(fa2_lh))]) ; ga2_rh=np.array([g[find_value(fa2_rh[i],f)] for i in range(len(fa2_rh))])
ga3_lh=np.array([g[find_value(fa3_lh[i],f)] for i in range(len(fa3_lh))]) ; ga3_rh=np.array([g[find_value(fa3_rh[i],f)] for i in range(len(fa3_rh))])

va1_lh = - sa1_lh * RJ * L / (3 * fa1_lh * ga1_lh) ; va2_lh = - sa2_lh * RJ * L / (3 * fa2_lh * ga2_lh) ; va3_lh = sa3_lh * RJ * L / (3*fa3_lh*ga3_lh)
va1_rh = - sa1_rh * RJ * L / (3 * fa1_rh * ga1_rh) ; va2_rh = - sa2_rh * RJ * L / (3 * fa2_rh * ga2_rh) ; va3_rh = sa3_rh * RJ * L / (3*fa3_rh*ga3_rh)

Ea1_lh = 256. * np.power(va1_lh/3e8,2) / (1-fa1_lh/40.) ; Ea2_lh = 256. * np.power(va2_lh/3e8,2) / (1-fa2_lh/40.) ; Ea3_lh = 256. * np.power(va3_lh/3e8,2) / (1-fa3_lh/40.)
Ea1_rh = 256. * np.power(va1_rh/3e8,2) / (1-fa1_rh/40.) ; Ea2_rh = 256. * np.power(va2_rh/3e8,2) / (1-fa2_rh/40.) ; Ea3_rh = 256. * np.power(va3_rh/3e8,2) / (1-fa3_rh/40.)


hist_va1_lh,xva1_lh=np.histogram(np.abs(va1_lh),bins=20)
hist_va1_rh,xva1_rh=np.histogram(np.abs(va1_rh),bins=20)
hist_va2_lh,xva2_lh=np.histogram(np.abs(va2_lh),bins=20)
hist_va2_rh,xva2_rh=np.histogram(np.abs(va2_rh),bins=20)
hist_va3_lh,xva3_lh=np.histogram(np.abs(va3_lh),bins=20)
hist_va3_rh,xva3_rh=np.histogram(np.abs(va3_rh),bins=20)

hist_Ea1_lh,xEa1_lh=np.histogram(Ea1_lh,bins=int(np.max(Ea1_lh)-np.min(Ea1_lh)))
hist_Ea1_rh,xEa1_rh=np.histogram(Ea1_rh,bins=int(np.max(Ea1_rh)-np.min(Ea1_rh)))
hist_Ea2_lh,xEa2_lh=np.histogram(Ea2_lh,bins=int((np.max(Ea2_lh)-np.min(Ea2_lh))/0.1))
hist_Ea2_rh,xEa2_rh=np.histogram(Ea2_rh,bins=int((np.max(Ea2_rh)-np.min(Ea2_rh))/0.1))
hist_Ea3_lh,xEa3_lh=np.histogram(Ea3_lh,bins=int((np.max(Ea3_lh)-np.min(Ea3_lh))/0.1))
hist_Ea3_rh,xEa3_rh=np.histogram(Ea3_rh,bins=int((np.max(Ea3_rh)-np.min(Ea3_rh))/0.1))


plt.figure(figsize=(20,15))

plt.subplot(321)
ax1=plt.gca()
ax1.plot(xvi1_lh[1:]*1e-3,hist_vi1_lh,drawstyle='steps-mid', alpha=1)
ax1.plot(xvi2_lh[1:]*1e-3,hist_vi2_lh,drawstyle='steps-mid', alpha=1)
ax1.plot(xvi3_lh[1:]*1e-3,hist_vi3_lh,drawstyle='steps-mid', alpha=1)
ax1.tick_params(axis='both', which='major', labelsize=16)
#plt.text(-1,2100, 'a)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('$v_{//}$ [km/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.grid()
plt.title('Io (LH)',fontsize=20)

plt.subplot(322)
ax2=plt.gca()
ax2.plot(xvi1_rh[1:]*1e-3,hist_vi1_rh,drawstyle='steps-mid', alpha=1)
ax2.plot(xvi2_rh[1:]*1e-3,hist_vi2_rh,drawstyle='steps-mid', alpha=1)
ax2.plot(xvi3_rh[1:]*1e-3,hist_vi3_rh,drawstyle='steps-mid', alpha=1)
ax2.tick_params(axis='both', which='major', labelsize=16)
#plt.text(-1,2100, 'b)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('$v_{//}$ [km/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.grid()
plt.title('Io (RH)',fontsize=20)

plt.subplot(323)
ax3=plt.gca()
ax3.plot(xvg1_lh[1:]*1e-3,hist_vg1_lh,drawstyle='steps-mid', alpha=1)
ax3.plot(xvg2_lh[1:]*1e-3,hist_vg2_lh,drawstyle='steps-mid', alpha=1)
ax3.plot(xvg3_lh[1:]*1e-3,hist_vg3_lh,drawstyle='steps-mid', alpha=1)
ax3.tick_params(axis='both', which='major', labelsize=16)
#plt.text(-1,260, 'c)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('$v_{//}$ [km/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.yscale('log')
plt.grid()
plt.title('Ganymede (LH)',fontsize=20)

plt.subplot(324)
ax4=plt.gca()
ax4.plot(xvg1_rh[1:]*1e-3,hist_vg1_rh,drawstyle='steps-mid', alpha=1)
ax4.plot(xvg2_rh[1:]*1e-3,hist_vg2_rh,drawstyle='steps-mid', alpha=1)
ax4.plot(xvg3_rh[1:]*1e-3,hist_vg3_rh,drawstyle='steps-mid', alpha=1)
ax4.tick_params(axis='both', which='major', labelsize=16)
#plt.text(-1,220, 'd)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('$v_{//}$ [km/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.yscale('log')
plt.grid()
plt.title('Ganymede (RH)',fontsize=20)

plt.subplot(325)
ax5=plt.gca()
ax5.plot(xva1_lh[1:]*1e-3,hist_va1_lh,drawstyle='steps-mid', alpha=1)
ax5.plot(xva2_lh[1:]*1e-3,hist_va2_lh,drawstyle='steps-mid', alpha=1)
ax5.plot(xva3_lh[1:]*1e-3,hist_va3_lh,drawstyle='steps-mid', alpha=1)
ax5.tick_params(axis='both', which='major', labelsize=16)
#plt.text(-1,400, 'e)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('$v_{//}$ [km/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.yscale('log')
plt.grid()
plt.title('Main aurora (LH)',fontsize=20)

plt.subplot(326)
ax6=plt.gca()
ax6.plot(xva1_rh[1:]*1e-3,hist_va1_rh,drawstyle='steps-mid', alpha=1)
ax6.plot(xva2_rh[1:]*1e-3,hist_va2_rh,drawstyle='steps-mid', alpha=1)
ax6.plot(xva3_rh[1:]*1e-3,hist_va3_rh,drawstyle='steps-mid', alpha=1)
ax6.tick_params(axis='both', which='major', labelsize=16)
#plt.text(-1,750, 'f)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('$v_{//}$ [km/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.yscale('log')
plt.grid()
plt.title('Main aurora (RH)',fontsize=20)

plt.tight_layout()
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_9_Vpar.pdf', dpi=150)
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_9_Vpar.eps', dpi=150)

fig9 , ax  = plt.subplots(3,4,figsize=(20,15))

ax[0,0].plot(xEi2_lh[1:],hist_Ei2_lh,drawstyle='steps-mid',color='tab:orange', alpha=1,label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax[0,0].plot(xEi3_lh[1:],hist_Ei3_lh,drawstyle='steps-mid',color='tab:green', alpha=1,label='$ s \geq 0$ MHz.s$^{-1}$')
ax[0,0].tick_params(axis='both', which='major', labelsize=16)
#plt.text(-1,260, 'c)', color='black',fontsize=24,fontweight='bold')
ax[0,0].set_xlabel('Energy [keV]',fontsize=18)
ax[0,0].set_ylabel('Nbr detections',fontsize=18)
ax[0,0].set_xscale('log')
#ax[0,0].set_xlim(0.05,6)
ax[0,0].set_title('Io (LH)',color='black',fontsize=20)
ax[0,0].grid()
ax[0,0].legend()

ax[0,1].plot(xEi1_lh[1:],hist_Ei1_lh,drawstyle='steps-mid',color='tab:blue', alpha=1, label='$ s \leq -10$ MHz.s$^{-1}$')
ax[0,1].tick_params(axis='both', which='major', labelsize=16)
#plt.text(-1,260, 'c)', color='black',fontsize=24,fontweight='bold')
ax[0,1].set_xlabel('Energy [keV]',fontsize=18)
ax[0,1].set_ylabel('Nbr detections',fontsize=18)
ax[0,1].set_title('Io (LH)',color='black',fontsize=20)
ax[0,1].grid()
ax[0,1].legend()


ax[0,2].plot(xEi2_rh[1:],hist_Ei2_rh,drawstyle='steps-mid',color='tab:orange', alpha=1,label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax[0,2].plot(xEi3_rh[1:],hist_Ei3_rh,drawstyle='steps-mid',color='tab:green', alpha=1,label='$ s \geq 0$ MHz.s$^{-1}$')
ax[0,2].tick_params(axis='both', which='major', labelsize=16)
ax[0,2].set_xlabel('Energy [keV]',fontsize=18)
ax[0,2].set_ylabel('Nbr detections',fontsize=18)
ax[0,2].set_xscale('log')
#ax[0,2].set_xlim(0.05,6)
ax[0,2].set_title('Io (RH)',color='black',fontsize=20)
ax[0,2].grid()
ax[0,2].legend()

ax[0,3].plot(xEi1_rh[1:],hist_Ei1_rh,drawstyle='steps-mid',color='tab:blue', alpha=1, label='$ s \leq -10$ MHz.s$^{-1}$')
ax[0,3].tick_params(axis='both', which='major', labelsize=16)
#plt.text(-1,260, 'c)', color='black',fontsize=24,fontweight='bold')
ax[0,3].set_xlabel('Energy [keV]',fontsize=18)
ax[0,3].set_ylabel('Nbr detections',fontsize=18)
ax[0,3].set_title('Io (RH)',color='black',fontsize=20)
ax[0,3].grid()
ax[0,3].legend()



ax[1,0].plot(xEg2_lh[1:],hist_Eg2_lh,drawstyle='steps-mid',color='tab:orange', alpha=1,label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax[1,0].plot(xEg3_lh[1:],hist_Eg3_lh,drawstyle='steps-mid',color='tab:green', alpha=1,label='$ s \geq 0$ MHz.s$^{-1}$')
ax[1,0].tick_params(axis='both', which='major', labelsize=16)
ax[1,0].set_xlabel('Energy [keV]',fontsize=18)
ax[1,0].set_ylabel('Nbr detections',fontsize=18)
ax[1,0].set_xscale('log')
#ax[1,0].set_xlim(0.05,6)
ax[1,0].set_title('Ganymede (LH)',color='black',fontsize=20)
ax[1,0].legend()
ax[1,0].grid()


ax[1,1].plot(xEg1_lh[1:],hist_Eg1_lh,drawstyle='steps-mid',color='tab:blue', alpha=1, label='$ s \leq -10$ MHz.s$^{-1}$')
ax[1,1].tick_params(axis='both', which='major',labelsize=16)
#plt.text(-1,260, 'c)', color='black',fontsize=24,fontweight='bold')
ax[1,1].set_xlabel('Energy [keV]',fontsize=18)
ax[1,1].set_ylabel('Nbr detections',fontsize=18)
ax[1,1].set_title('Ganymede (LH)',color='black',fontsize=20)
ax[1,1].grid()
ax[1,1].legend()


ax[1,2].plot(xEg2_rh[1:],hist_Eg2_rh,drawstyle='steps-mid',color='tab:orange', alpha=1,label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax[1,2].plot(xEg3_rh[1:],hist_Eg3_rh,drawstyle='steps-mid',color='tab:green', alpha=1,label='$ s \geq 0$ MHz.s$^{-1}$')
ax[1,2].tick_params(axis='both', which='major', labelsize=16)
ax[1,2].set_xlabel('Energy [keV]',fontsize=18)
ax[1,2].set_ylabel('Nbr detections',fontsize=18)
ax[1,2].set_xscale('log')
#ax[1,2].set_xlim(0.05,6)
ax[1,2].set_title('Ganymede (RH)',color='black',fontsize=20)
ax[1,2].grid()
ax[1,2].legend()

ax[1,3].plot(xEg1_rh[1:],hist_Eg1_rh,drawstyle='steps-mid',color='tab:blue', alpha=1, label='$ s \leq -10$ MHz.s$^{-1}$')
ax[1,3].tick_params(axis='both', which='major',labelsize=16)
#plt.text(-1,260, 'c)', color='black',fontsize=24,fontweight='bold')
ax[1,3].set_xlabel('Energy [keV]',fontsize=18)
ax[1,3].set_ylabel('Nbr detections',fontsize=18)
ax[1,3].set_title('Ganymede (RH)',color='black',fontsize=20)
ax[1,3].grid()
ax[1,3].legend()


ax[2,0].plot(xEa2_lh[1:],hist_Ea2_lh,drawstyle='steps-mid',color='tab:orange', alpha=1,label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax[2,0].plot(xEa3_lh[1:],hist_Ea3_lh,drawstyle='steps-mid',color='tab:green', alpha=1,label='$ s \geq 0$ MHz.s$^{-1}$')
ax[2,0].tick_params(axis='both', which='major', labelsize=16)
#plt.text(-1,260, 'c)', color='black',fontsize=24,fontweight='bold')
ax[2,0].set_xlabel('Energy [keV]',fontsize=18)
ax[2,0].set_ylabel('Nbr detections',fontsize=18)
ax[2,0].set_xscale('log')
#ax[2,0].set_xlim(0.05,6)
ax[2,0].set_title('Main aurora (LH)',color='black',fontsize=20)
ax[2,0].grid()
ax[2,0].legend()

ax[2,1].plot(xEa1_lh[1:],hist_Ea1_lh,drawstyle='steps-mid',color='tab:blue', alpha=1, label='$ s \leq -10$ MHz.s$^{-1}$')
ax[2,1].tick_params(axis='both', which='major',labelsize=16)
#plt.text(-1,260, 'c)', color='black',fontsize=24,fontweight='bold')
ax[2,1].set_xlabel('Energy [keV]',fontsize=18)
ax[2,1].set_ylabel('Nbr detections',fontsize=18)
ax[2,1].set_title('Main aurora (LH)',color='black',fontsize=20)
ax[2,1].grid()
ax[2,1].legend()



ax[2,2].plot(xEa2_rh[1:],hist_Ea2_rh,drawstyle='steps-mid',color='tab:orange', alpha=1,label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax[2,2].plot(xEa3_rh[1:],hist_Ea3_rh,drawstyle='steps-mid',color='tab:green', alpha=1,label='$ s \geq 0$ MHz.s$^{-1}$')
ax[2,2].tick_params(axis='both', which='major', labelsize=16)
#plt.text(-1,260, 'c)', color='black',fontsize=24,fontweight='bold')
ax[2,2].set_xlabel('Energy [keV]',fontsize=18)
ax[2,2].set_ylabel('Nbr detections',fontsize=18)
ax[2,2].set_xscale('log')
#ax[2,2].set_xlim(0.05,6)
ax[2,2].set_title('Main aurora (RH)', color='black',fontsize=20)
ax[2,2].grid()
ax[2,2].legend()


ax[2,3].plot(xEa1_rh[1:],hist_Ea1_rh,drawstyle='steps-mid',color='tab:blue', alpha=1, label='$ s \leq -10$ MHz.s$^{-1}$')
ax[2,3].tick_params(axis='both',which='major',labelsize=16)
#plt.text(-1,260, 'c)', color='black',fontsize=24,fontweight='bold')
ax[2,3].set_xlabel('Energy [keV]',fontsize=18)
ax[2,3].set_ylabel('Nbr detections',fontsize=18)
ax[2,3].set_title('Main aurora (RH)', color='black',fontsize=20)
ax[2,3].grid()
ax[2,3].legend()

fig9.tight_layout()
fig9.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_9_E.pdf', dpi=150)
fig9.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_9_E.eps', dpi=150)


###################################################
#------------------- Figure 10 -------------------#
###################################################

print('------ Figure 10 ------')

plt.figure(figsize=(20,5))

plt.subplot(121)
ax1=plt.gca()
ax1.plot(xsi1_lh[0:-1],hist_si1_lh,drawstyle='steps-mid', alpha=1)
ax1.plot(xsi2_lh[0:-1],hist_si2_lh,drawstyle='steps-mid', alpha=1)
ax1.plot(xsi3_lh[0:-1],hist_si3_lh,drawstyle='steps-mid', alpha=1)
ax1.tick_params(axis='both', which='major', labelsize=16)
plt.text(-37,3100, 'a)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.yscale('log')
plt.grid()
plt.title('Io (LH)',fontsize=20)

plt.subplot(122)
ax2=plt.gca()
ax2.plot(xsi1_rh[0:-1],hist_si1_rh,drawstyle='steps-mid', alpha=1)
ax2.plot(xsi2_rh[0:-1],hist_si2_rh,drawstyle='steps-mid', alpha=1)
ax2.plot(xsi3_rh[0:-1],hist_si3_rh,drawstyle='steps-mid', alpha=1)
ax2.tick_params(axis='both', which='major', labelsize=16)
plt.text(-37,6000, 'b)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.yscale('log')
plt.grid()
plt.title('Io (RH)',fontsize=20)

plt.tight_layout()
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_10.pdf', dpi=150)
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_10.eps', dpi=150)



###################################################
#------------------- Figure 11 -------------------#
###################################################

#Distribution de la polar et des pentes pour les points Gan B et Gan C
print('------ Figure 11 ------')

NgB_lh=0 ; NgC_lh=0 ; NgAD_lh=0
sgB_lh=[] ; sgC_lh=[] 

for i in range (nlh):
    if ((jup.inboxio(cml_lh[i], phiio_lh[i])==False) and  (jup.inboxgan(cml_lh[i], phiga_lh[i])==True)):
        if (jup.inboxganB(cml_lh[i], phiga_lh[i])==True):
            NgB_lh += 1
            sgB_lh.append(s_lh[i])
        elif (jup.inboxganC(cml_lh[i], phiga_lh[i])==True):
            NgC_lh +=1
            sgC_lh.append(s_lh[i])
        else :
            NgAD_lh += 1

sgB1_lh = [sgB_lh[i] for i in range(len(sgB_lh)) if (-35. <= sgB_lh[i] < -10.)]
sgB2_lh = [sgB_lh[i] for i in range(len(sgB_lh)) if (-10. <= sgB_lh[i] < 0.)]
sgB3_lh = [sgB_lh[i] for i in range(len(sgB_lh)) if (0. <= sgB_lh[i] <= 20.)]

sgC1_lh = [sgC_lh[i] for i in range(len(sgC_lh)) if (-35. <= sgC_lh[i] < -10.)]
sgC2_lh = [sgC_lh[i] for i in range(len(sgC_lh)) if (-10. <= sgC_lh[i] < 0.)]
sgC3_lh = [sgC_lh[i] for i in range(len(sgC_lh)) if (0. <= sgC_lh[i] <= 20.)]

NgB_rh=0 ; NgC_rh=0  ; NgAD_rh=0
sgB_rh=[] ; sgC_rh=[] 

for i in range (nrh):
    if ((jup.inboxio(cml_rh[i], phiio_rh[i])==False) and  (jup.inboxgan(cml_rh[i], phiga_rh[i])==True)) :
        if (jup.inboxganB(cml_rh[i], phiga_rh[i])==True):
            NgB_rh += 1
            sgB_rh.append(s_rh[i])
        elif (jup.inboxganC(cml_rh[i], phiga_rh[i])==True):
            NgC_rh +=1
            sgC_rh.append(s_rh[i])
        else :
            NgAD_rh += 1

sgB1_rh = [sgB_rh[i] for i in range(len(sgB_rh)) if (-35. <= sgB_rh[i] < -10.)]
sgB2_rh = [sgB_rh[i] for i in range(len(sgB_rh)) if (-10. <= sgB_rh[i] < 0.)]
sgB3_rh = [sgB_rh[i] for i in range(len(sgB_rh)) if (0. <= sgB_rh[i] <= 20.)]

sgC1_rh = [sgC_rh[i] for i in range(len(sgC_rh)) if (-35. <= sgC_rh[i] < -10.)]
sgC2_rh = [sgC_rh[i] for i in range(len(sgC_rh)) if (-10. <= sgC_rh[i] < 0.)]
sgC3_rh = [sgC_rh[i] for i in range(len(sgC_rh)) if (0. <= sgC_rh[i] <= 20.)]


hist_sgB1_lh,xsgB1_lh=np.histogram(sgB1_lh,bins=25,range=(-35.,-10.))
hist_sgB1_rh,xsgB1_rh=np.histogram(sgB1_rh,bins=25,range=(-35.,-10.))
hist_sgB2_lh,xsgB2_lh=np.histogram(sgB2_lh,bins=20,range=(-10.,0))
hist_sgB2_rh,xsgB2_rh=np.histogram(sgB2_rh,bins=20,range=(-10.,0))
hist_sgB3_lh,xsgB3_lh=np.histogram(sgB3_lh,bins=20,range=(0.,20.))
hist_sgB3_rh,xsgB3_rh=np.histogram(sgB3_rh,bins=20,range=(0.,20.))

hist_sgC1_lh,xsgC1_lh=np.histogram(sgC1_lh,bins=25,range=(-35.,-10.))
hist_sgC1_rh,xsgC1_rh=np.histogram(sgC1_rh,bins=25,range=(-35.,-10.))
hist_sgC2_lh,xsgC2_lh=np.histogram(sgC2_lh,bins=20,range=(-10.,0))
hist_sgC2_rh,xsgC2_rh=np.histogram(sgC2_rh,bins=20,range=(-10.,0))
hist_sgC3_lh,xsgC3_lh=np.histogram(sgC3_lh,bins=20,range=(0.,20.))
hist_sgC3_rh,xsgC3_rh=np.histogram(sgC3_rh,bins=20,range=(0.,20.))

print(NgB_lh,NgB_rh,NgC_lh,NgC_rh, NgAD_lh,NgAD_rh)

plt.figure(figsize=(20,10))

plt.subplot(221)
ax1=plt.gca()
ax1.plot(xsgB1_lh[0:-1],hist_sgB1_lh,drawstyle='steps-mid', alpha=1)
ax1.plot(xsgB2_lh[0:-1],hist_sgB2_lh,drawstyle='steps-mid', alpha=1)
ax1.plot(xsgB3_lh[0:-1],hist_sgB3_lh,drawstyle='steps-mid', alpha=1)
ax1.tick_params(axis='both', which='major', labelsize=16)
#plt.text(-37,3100, 'a)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.ylim(-3,1.1*np.max(hist_sgB1_rh))
plt.grid()
plt.title('Ganymede B (LH)',fontsize=20)

plt.subplot(222)
ax2=plt.gca()
ax2.plot(xsgB1_rh[0:-1],hist_sgB1_rh,drawstyle='steps-mid', alpha=1)
ax2.plot(xsgB2_rh[0:-1],hist_sgB2_rh,drawstyle='steps-mid', alpha=1)
ax2.plot(xsgB3_rh[0:-1],hist_sgB3_rh,drawstyle='steps-mid', alpha=1)
ax2.tick_params(axis='both', which='major', labelsize=16)
#plt.text(-37,6000, 'b)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.ylim(-3,1.1*np.max(hist_sgB1_rh))
plt.grid()
plt.title('Ganymede B (RH)',fontsize=20)

plt.subplot(223)
ax1=plt.gca()
ax1.plot(xsgC1_lh[0:-1],hist_sgC1_lh,drawstyle='steps-mid', alpha=1)
ax1.plot(xsgC2_lh[0:-1],hist_sgC2_lh,drawstyle='steps-mid', alpha=1)
ax1.plot(xsgC3_lh[0:-1],hist_sgC3_lh,drawstyle='steps-mid', alpha=1)
ax1.tick_params(axis='both', which='major', labelsize=16)
#plt.text(-37,3100, 'a)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.ylim(-3,1.1*np.max(hist_sgC2_lh))
plt.grid()
plt.title('Ganymede C (LH)',fontsize=20)

plt.subplot(224)
ax1=plt.gca()
ax1.plot(xsgC1_rh[0:-1],hist_sgC1_rh,drawstyle='steps-mid', alpha=1)
ax1.plot(xsgC2_rh[0:-1],hist_sgC2_rh,drawstyle='steps-mid', alpha=1)
ax1.plot(xsgC3_rh[0:-1],hist_sgC3_rh,drawstyle='steps-mid', alpha=1)
ax1.tick_params(axis='both', which='major', labelsize=16)
#plt.text(-37,3100, 'a)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.ylim(-3,1.1*np.max(hist_sgC2_lh))
plt.grid()
plt.title('Ganymede C (RH)',fontsize=20)

plt.tight_layout()
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_11a.pdf', dpi=150)


plt.figure(figsize=(10,10))
plt.bar([0.8,1.8],[NgB_lh*100./(NgB_lh+NgB_rh),NgC_lh*100/(NgC_lh+NgC_rh)], 0.4, color ='blue', label='LH')
plt.bar([1.2,2.2],[NgB_rh*100./(NgB_lh+NgB_rh),NgC_rh*100/(NgC_lh+NgC_rh)],0.4, color='orange', label='RH')
plt.xticks([1.0,2.0],['Ganymede B', 'Ganymede C'])
plt.ylabel('Percentage of detections [%]')
plt.title('Polarization distribution')
plt.grid()
plt.legend()
plt.savefig('/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/Article/Figures/Figure_11b.pdf', dpi=150)