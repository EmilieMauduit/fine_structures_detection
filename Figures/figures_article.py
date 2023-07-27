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
#------------------- Figure 1 --------------------#
###################################################

data_fig1 = pd.read_excel('data_figure_1_bis.xlsx',sheet_name=['LH','RH'], index_col=0)
data_lh = data_fig1['LH'] ; data_rh=data_fig1['RH']

print('------ Figure 1 ------')

plt.figure(figsize=(20,9.5))
### CML vs PhiIo
plt.subplot(121)
jup.io(data_lh['cml'],data_lh['phi_io'],data_lh['cml'], data_lh['phi_gan'],data_rh['cml'],data_rh['phi_io'],data_rh['cml'],  data_rh['phi_gan'])

# CML vs PhiGa
plt.subplot(122)
jup.gan(data_lh['cml'], data_lh['phi_gan'],data_lh['cml'],data_lh['phi_io'],data_rh['cml'],  data_rh['phi_gan'],data_rh['cml'],data_rh['phi_io'])


plt.tight_layout()
plt.savefig('Figure_1.pdf', dpi=150)
plt.savefig('Figure_1.eps', dpi=150)



###################################################
#------------------- Figure 2 --------------------#
###################################################

def drifts(x,a,orig):
    x = np.array(x)
    b = orig[1] - (a*orig[0])
    return a*x + b


print('------ Figure 2 bis ------')

Io1=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Io_1.sav')
Io2=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Io_2.sav')
Gan2=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Gan_2.sav')
Gan3=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Gan_3.sav')
Aur2=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Aur_2.sav')
Aur3=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_Aur_3.sav')


print(Io1['fmin'],Io1['fmax'])

plt.figure(figsize=(20,10))
plt.subplot(231)
ax1=plt.gca()
im1=ax1.imshow(jup.scale_spdyn(Io1['xlh1']), origin='lower',extent=[0,(Io1['tmax']-Io1['tmin'])*3600,Io1['fmin'],Io1['fmax']],aspect=(Io1['tmax']-Io1['tmin'])*3600/(Io1['fmax']-Io1['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax1.plot([0.1,0.3],drifts([0.1,0.3],Io1['slope_lh'],[0.1,16.5]), linestyle='dashed', linewidth=3, color='deepskyblue')
ax1.tick_params(axis='both', which='major', labelsize=18)
plt.text(-0.15,17.2, 'a)', color='black',fontsize=20,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-06'.format(Io1['tmin']),fontsize=20)
plt.ylabel('Frequency [MHz]',fontsize=20)
plt.title('Io, <df/dt>={:.3}'.format(Io1['slope_lh']) + ' $MHz.s^{-1}$',fontsize=22)
cb1=plt.colorbar(im1, ax=ax1)
cb1.set_label('dB', fontsize=20)
cb1.ax.tick_params(labelsize=18)

plt.subplot(234)
ax2=plt.gca()
im2=ax2.imshow(jup.scale_spdyn(Io2['xlh1']), origin='lower',extent=[0,(Io2['tmax']-Io2['tmin'])*3600,Io2['fmin'],Io2['fmax']],aspect=(Io2['tmax']-Io2['tmin'])*3600/(Io2['fmax']-Io2['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax2.plot([0.1,0.3],drifts([0.1,0.3],Io2['slope_lh'],[0.1,16.8]), linestyle='dashed', linewidth=3, color='deepskyblue')
ax2.tick_params(axis='both', which='major', labelsize=18)
plt.text(-0.15,17.2, 'b)', color='black',fontsize=20,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-06'.format(Io2['tmin']),fontsize=20)
plt.ylabel('Frequency [MHz]',fontsize=20)
plt.title('Io, <df/dt>={:.3}'.format(Io2['slope_lh']) + ' $MHz.s^{-1}$',fontsize=22)
cb2=plt.colorbar(im2, ax=ax2)
cb2.set_label('dB', fontsize=20)
cb2.ax.tick_params(labelsize=18)

plt.subplot(232)
ax3=plt.gca()
im3=ax3.imshow(jup.scale_spdyn(Gan3['xlh1']), origin='lower',extent=[0,(Gan3['tmax']-Gan3['tmin'])*3600,Gan3['fmin'],Gan3['fmax']],aspect=(Gan3['tmax']-Gan3['tmin'])*3600/(Gan3['fmax']-Gan3['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax3.plot([0.1,0.25],drifts([0.1,0.25],Gan3['slope_lh'],[0.1,16]), linestyle='dashed', linewidth=3, color='deepskyblue')
ax3.tick_params(axis='both', which='major', labelsize=18)
plt.text(-0.2,17.2, 'c)', color='black',fontsize=20,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-17'.format(Gan3['tmin']),fontsize=20)
plt.ylabel('Frequency [MHz]',fontsize=20)
plt.title('Gan, <df/dt>={:.3}'.format(Gan3['slope_lh']) + ' $MHz.s^{-1}$',fontsize=22)
cb3=plt.colorbar(im3, ax=ax3)
cb3.set_label('dB', fontsize=20)
cb3.ax.tick_params(labelsize=18)

plt.subplot(235)
ax4=plt.gca()
im4=ax4.imshow(jup.scale_spdyn(Gan2['xlh1']), origin='lower',extent=[0,(Gan2['tmax']-Gan2['tmin'])*3600,Gan2['fmin'],Gan2['fmax']],aspect=(Gan2['tmax']-Gan2['tmin'])*3600/(Gan2['fmax']-Gan2['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax4.plot([0.5,0.85],drifts([0.5,0.85],Gan2['slope_lh'],[0.5,16]), linestyle='dashed', linewidth=3, color='tab:orange')
ax4.tick_params(axis='both', which='major', labelsize=18)
plt.text(-0.2,17.2, 'd)', color='black',fontsize=20,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-17'.format(Gan2['tmin']),fontsize=20)
plt.ylabel('Frequency [MHz]',fontsize=20)
plt.title('Gan, <df/dt>={:.3}'.format(Gan2['slope_lh']) + ' $MHz.s^{-1}$',fontsize=22)
cb4=plt.colorbar(im4, ax=ax4)
cb4.set_label('dB', fontsize=20)
cb4.ax.tick_params(labelsize=18)

plt.subplot(233)
ax5=plt.gca()
im5=ax5.imshow(jup.scale_spdyn(Aur3['xlh1']), origin='lower',extent=[0,(Aur3['tmax']-Aur3['tmin'])*3600,Aur3['fmin'],Aur3['fmax']],aspect=(Aur3['tmax']-Aur3['tmin'])*3600/(Aur3['fmax']-Aur3['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax5.plot([0.4,0.6],drifts([0.4,0.6],Aur3['slope_lh'],[0.4,13]), linestyle='dashed', linewidth=3, color='deepskyblue')
ax5.tick_params(axis='both', which='major', labelsize=18)
plt.text(-0.2,17.2, 'e)', color='black',fontsize=20,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-15'.format(Aur3['tmin']),fontsize=20)
plt.ylabel('Frequency [MHz]',fontsize=20)
plt.title('Aur, <df/dt>={:.3}'.format(Aur3['slope_lh']) + ' $MHz.s^{-1}$',fontsize=22)
cb5=plt.colorbar(im5, ax=ax5)
cb5.set_label('dB', fontsize=20)
cb5.ax.tick_params(labelsize=18)

plt.subplot(236)
ax6=plt.gca()
im6=ax6.imshow(jup.scale_spdyn(Aur2['xrh1']), origin='lower',extent=[0,(Aur2['tmax']-Aur2['tmin'])*3600,Aur2['fmin'],Aur2['fmax']],aspect=(Aur2['tmax']-Aur2['tmin'])*3600/(Aur2['fmax']-Aur2['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax6.plot([0.1,0.6],drifts([0.1,0.6],Aur2['slope_rh'],[0.1,15]), linestyle='dashed', linewidth=3, color='tab:orange')
ax6.tick_params(axis='both', which='major', labelsize=18)
plt.text(-0.2,17.2, 'f)', color='black',fontsize=20,fontweight='bold')
plt.xlabel('Time [s] from {:.6} h on 2021-04-15'.format(Aur2['tmin']),fontsize=20)
plt.ylabel('Frequency [MHz]',fontsize=20)
plt.title('Aur, <df/dt>={:.3}'.format(Aur2['slope_rh']) + ' $MHz.s^{-1}$',fontsize=22)
cb6=plt.colorbar(im6, ax=ax6)
cb6.set_label('dB', fontsize=20)
cb6.ax.tick_params(labelsize=18)

plt.tight_layout()
plt.savefig('Figure_2.pdf', dpi=150)
plt.savefig('Figure_2.eps', dpi=150)


###################################################
#------------------- Figure 3 --------------------#
###################################################

print('------ Figure 3 ------')

data_fig3 = pd.read_excel('data_figure_3.xlsx', sheet_name=['Io_lh_-35_s_-10','Io_lh_-10_s_0','Io_lh_0_s_20','Io_rh_-35_s_-10','Io_rh_-10_s_0','Io_rh_0_s_20',
        'Gan_lh_-35_s_-10','Gan_lh_-10_s_0','Gan_lh_0_s_20','Gan_rh_-35_s_-10','Gan_rh_-10_s_0','Gan_rh_0_s_20',
        'Aur_lh_-35_s_-10','Aur_lh_-10_s_0','Aur_lh_0_s_20','Aur_rh_-35_s_-10','Aur_rh_-10_s_0','Aur_rh_0_s_20',])


plt.figure(figsize=(20,15))

plt.subplot(321)
ax1=plt.gca()
ax1.plot(data_fig3['Io_lh_-35_s_-10']['x'],data_fig3['Io_lh_-35_s_-10']['y'],drawstyle='steps-mid', color='tab:blue',alpha=1)
ax1.plot(data_fig3['Io_lh_-10_s_0']['x'],data_fig3['Io_lh_-10_s_0']['y'],drawstyle='steps-mid', color='tab:orange',alpha=1)
ax1.plot(data_fig3['Io_lh_0_s_20']['x'],data_fig3['Io_lh_0_s_20']['y'],drawstyle='steps-mid', color='tab:green',alpha=1)
ax1.tick_params(axis='both', which='major', labelsize=20)
plt.text(-35,1555, 'a)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=22)
plt.ylabel('Nbr detections',fontsize=22)
plt.xlim(-35,20)
plt.grid()
plt.title('Io (LH)',fontsize=24)

plt.subplot(322)
ax2=plt.gca()
ax2.plot(data_fig3['Io_rh_-35_s_-10']['x'],data_fig3['Io_rh_-35_s_-10']['y'],drawstyle='steps-mid', color='tab:blue',alpha=1)
ax2.plot(data_fig3['Io_rh_-10_s_0']['x'],data_fig3['Io_rh_-10_s_0']['y'],drawstyle='steps-mid', color='tab:orange',alpha=1)
ax2.plot(data_fig3['Io_rh_0_s_20']['x'],data_fig3['Io_rh_0_s_20']['y'],drawstyle='steps-mid', color='tab:green',alpha=1)
ax2.tick_params(axis='both', which='major', labelsize=20)
plt.text(-35,2650, 'b)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=22)
plt.ylabel('Nbr detections',fontsize=22)
plt.xlim(-35,20)
plt.grid()
plt.title('Io (RH)',fontsize=24)

plt.subplot(323)
ax3=plt.gca()
ax3.plot(data_fig3['Gan_lh_-35_s_-10']['x'],data_fig3['Gan_lh_-35_s_-10']['y'],drawstyle='steps-mid', color='tab:blue',alpha=1)
ax3.plot(data_fig3['Gan_lh_-10_s_0']['x'],data_fig3['Gan_lh_-10_s_0']['y'],drawstyle='steps-mid', color='tab:orange',alpha=1)
ax3.plot(data_fig3['Gan_lh_0_s_20']['x'],data_fig3['Gan_lh_0_s_20']['y'],drawstyle='steps-mid', color='tab:green',alpha=1)
ax3.tick_params(axis='both', which='major', labelsize=20)
plt.text(-35,277, 'c)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=22)
plt.ylabel('Nbr detections',fontsize=22)
plt.xlim(-35,20)
plt.grid()
plt.title('Ganymede (LH)',fontsize=24)

plt.subplot(324)
ax4=plt.gca()
ax4.plot(data_fig3['Gan_rh_-35_s_-10']['x'],data_fig3['Gan_rh_-35_s_-10']['y'],drawstyle='steps-mid', color='tab:blue',alpha=1)
ax4.plot(data_fig3['Gan_rh_-10_s_0']['x'],data_fig3['Gan_rh_-10_s_0']['y'],drawstyle='steps-mid', color='tab:orange',alpha=1)
ax4.plot(data_fig3['Gan_rh_0_s_20']['x'],data_fig3['Gan_rh_0_s_20']['y'],drawstyle='steps-mid', color='tab:green',alpha=1)
ax4.tick_params(axis='both', which='major', labelsize=20)
plt.text(-35,175, 'd)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=22)
plt.ylabel('Nbr detections',fontsize=22)
plt.xlim(-35,20)
plt.grid()
plt.title('Ganymede (RH)',fontsize=24)

plt.subplot(325)
ax5=plt.gca()
ax5.plot(data_fig3['Aur_lh_-35_s_-10']['x'],data_fig3['Aur_lh_-35_s_-10']['y'],drawstyle='steps-mid', color='tab:blue',alpha=1)
ax5.plot(data_fig3['Aur_lh_-10_s_0']['x'],data_fig3['Aur_lh_-10_s_0']['y'],drawstyle='steps-mid', color='tab:orange',alpha=1)
ax5.plot(data_fig3['Aur_lh_0_s_20']['x'],data_fig3['Aur_lh_0_s_20']['y'],drawstyle='steps-mid', color='tab:green',alpha=1)
ax5.tick_params(axis='both', which='major', labelsize=20)
plt.text(-35,325, 'e)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=22)
plt.ylabel('Nbr detections',fontsize=22)
plt.xlim(-35,20)
plt.grid()
plt.title('Main aurora (LH)',fontsize=24)

plt.subplot(326)
ax6=plt.gca()
ax6.plot(data_fig3['Aur_rh_-35_s_-10']['x'],data_fig3['Aur_rh_-35_s_-10']['y'],drawstyle='steps-mid', color='tab:blue',alpha=1)
ax6.plot(data_fig3['Aur_rh_-10_s_0']['x'],data_fig3['Aur_rh_-10_s_0']['y'],drawstyle='steps-mid', color='tab:orange',alpha=1)
ax6.plot(data_fig3['Aur_rh_0_s_20']['x'],data_fig3['Aur_rh_0_s_20']['y'],drawstyle='steps-mid', color='tab:green',alpha=1)
ax6.tick_params(axis='both', which='major', labelsize=20)
plt.text(-35,815, 'f)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('Slopes [MHz/s]',fontsize=22)
plt.ylabel('Nbr detections',fontsize=22)
plt.xlim(-35,20)
plt.grid()
plt.title('Main aurora (RH)',fontsize=24)

plt.tight_layout()
plt.savefig('Figure_3.pdf', dpi=150)
plt.savefig('Figure_3.eps', dpi=150)


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
ax3.plot(data['x'],data['y'], color='orange',linestyle='--', linewidth=1.5, label='$RD_{box \ of \ ones}$')
ax3.plot([-1,181],[0,0], color='black', linestyle='dashed', linewidth=1)
ax3.tick_params(axis='both', which='major', labelsize=16)
plt.text(1,1370, 'e)', color='black',fontsize=16,fontweight='bold')
plt.xlim(0,180)
plt.xlabel("Angles [°]",fontsize=18)
plt.ylabel("Intensity [a.u.]",fontsize=18)
plt.legend(fontsize = 16 )
plt.grid()
plt.title('RD(TF)',fontsize=20)

plt.subplot(236)
ax6=plt.gca()
ax6.plot(Io3['theta_rd'],Io3['rd_rh1o'], 'g--', linewidth=1, label='$RD_{original,corr}$')
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
plt.ylabel("Normalized Intensity ",fontsize=18)
plt.legend(fontsize = 16 )
plt.grid()
plt.title('$RD(TF)_{corr}$,'+' SNR={:.4}'.format(Io3['snr_rh']),fontsize=20)

plt.tight_layout()
plt.savefig('Figure_4.pdf', dpi=150)
plt.savefig('Figure_4.eps', dpi=150)


###################################################
#------------------- Figure 5 --------------------#
###################################################

print('------ Figure 5 ------')

NDet=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_no_detect.sav')

tmin_tf=-((420-1)/2)/(420*2.6e-3) ; tmax_tf=((420-1)/2)/(420*2.6e-3)
fmin_tf=-((420-1)/2)/(420*21.35e-3) ; fmax_tf=((420-1)/2)/(420*21.35e-3)


plt.figure(figsize=(10,20))
plt.subplot(311)
ax1=plt.gca()
im1=ax1.imshow(jup.scale_spdyn(NDet['xlh1']), origin='lower',extent=[0,(NDet['tmax']-NDet['tmin'])*3600,NDet['fmin'],NDet['fmax']],aspect=(NDet['tmax']-NDet['tmin'])*3600/(NDet['fmax']-NDet['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax1.tick_params(axis='both', which='major', labelsize=20)
plt.xlabel('Time [s] from {:.6} h'.format(NDet['tmin']),fontsize=22)
plt.ylabel('Frequency [MHz]',fontsize=22)
plt.title('No signal, <df/dt>={:.4}'.format(NDet['slope_lh']) + ' $MHz.s^{-1}$',fontsize=24)
cb1=plt.colorbar(im1, ax=ax1)
cb1.set_label('dB', fontsize=22)
cb1.ax.tick_params(labelsize=20)


plt.subplot(312)

ax2=plt.gca()
im2=ax2.imshow(np.log10(NDet['tflh1']), origin='lower',extent=[tmin_tf,tmax_tf,fmin_tf,fmax_tf],aspect=(tmax_tf-tmin_tf)/(fmax_tf-fmin_tf),vmin=-3.,cmap='magma',alpha=1)
ax2.tick_params(axis='both', which='major', labelsize=20)
plt.xlabel('Time$^{-1}$ [$s^{-1}$]',fontsize=22)
plt.ylabel('Frequency$^{-1}$ [$MHz^{-1}$]',fontsize=22)
plt.title('TF(SPDYN)',fontsize=24)
cb2=plt.colorbar(im2, ax=ax2)
cb2.set_label('dB', fontsize=22)
cb2.ax.tick_params(labelsize=20)

plt.subplot(313)
ax3=plt.gca()
ax3.plot(NDet['theta_rd'],NDet['rd_lh1o'], 'g--', linewidth=1, label='$RD_{original}$')
ax3.plot([-1,121],[0,0], color='black', linestyle='dashed', linewidth=1)
ax3.plot([60,60],[-0.045,0.08], color='black', linestyle='dashdot', linewidth=1)
ax3.plot(NDet['theta_rd'],NDet['rd_lh1'],'b-' ,linewidth=2,label='$RD_{centered}$')
ax3.plot(NDet['theta_rd'], NDet['fit_lh_all'], 'r--', linewidth=1, label='Gaussian Fit')
ax3.tick_params(axis='both', which='major', labelsize=16)
ax3.legend(loc='upper center',fontsize=20, ncol = 3)
plt.xlim(0,120)
plt.ylim(-0.045,0.08)
plt.xlabel("Angles [°]",fontsize=22)
plt.xticks([0,20,40,60,80,100,120],[15,35,55,'75//105',125,145,165])
plt.ylabel("Normalized Intensity ",fontsize=22)
plt.grid()
plt.title('RD(TF), SNR={:.5}'.format(NDet['snr_lh']),fontsize=24)

plt.tight_layout()
plt.savefig('Figure_5.eps', dpi=150)
plt.savefig('Figure_5.pdf', dpi=150)

###################################################
#------------------- Figure 6 --------------------#
###################################################

print('------ Figure 6 ------')

data_fig6 = pd.read_excel('data_figure_6.xlsx', sheet_name=['Io_lh_-35_s_-10','Io_lh_-10_s_0','Io_lh_0_s_20','Io_rh_-35_s_-10','Io_rh_-10_s_0','Io_rh_0_s_20',
        'Gan_lh_-35_s_-10','Gan_lh_-10_s_0','Gan_lh_0_s_20','Gan_rh_-35_s_-10','Gan_rh_-10_s_0','Gan_rh_0_s_20',
        'Aur_lh_-35_s_-10','Aur_lh_-10_s_0','Aur_lh_0_s_20','Aur_rh_-35_s_-10','Aur_rh_-10_s_0','Aur_rh_0_s_20',])


fig9 , ax  = plt.subplots(3,4,figsize=(20,20))

ax[0,0].plot(data_fig6['Io_lh_-10_s_0']['x'],data_fig6['Io_lh_-10_s_0']['y'],drawstyle='steps-mid',color='tab:orange', alpha=1,label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax[0,0].plot(data_fig6['Io_lh_0_s_20']['x'],data_fig6['Io_lh_0_s_20']['y'],drawstyle='steps-mid',color='tab:green', alpha=1,label='$ s \geq 0$ MHz.s$^{-1}$')
ax[0,0].plot([],[],color='tab:blue',label='$ s \leq -10$ MHz.s$^{-1}$')
ax[0,0].tick_params(axis='both', which='major', labelsize=20)
ax[0,0].set_xlabel('Energy [keV]',fontsize=22)
ax[0,0].set_ylabel('Nbr detections',fontsize=22)
ax[0,0].set_xscale('log')
ax[0,0].set_title('Io (LH)',color='black',fontsize=24)
ax[0,0].grid()

ax[0,1].plot(data_fig6['Io_lh_-35_s_-10']['x'],data_fig6['Io_lh_-35_s_-10']['y'],drawstyle='steps-mid',color='tab:blue', alpha=1)
ax[0,1].tick_params(axis='both', which='major', labelsize=20)
ax[0,1].set_xlabel('Energy [keV]',fontsize=22)
ax[0,1].set_title('Io (LH)',color='black',fontsize=24)
ax[0,1].grid()

ax[0,2].plot(data_fig6['Io_rh_-10_s_0']['x'],data_fig6['Io_rh_-10_s_0']['y'],drawstyle='steps-mid',color='tab:orange', alpha=1)
ax[0,2].plot(data_fig6['Io_rh_0_s_20']['x'],data_fig6['Io_rh_0_s_20']['y'],drawstyle='steps-mid',color='tab:green', alpha=1)
ax[0,2].tick_params(axis='both', which='major', labelsize=20)
ax[0,2].set_xlabel('Energy [keV]',fontsize=22)
ax[0,2].set_xscale('log')
ax[0,2].set_title('Io (RH)',color='black',fontsize=24)
ax[0,2].grid()

ax[0,3].plot(data_fig6['Io_rh_-35_s_-10']['x'],data_fig6['Io_rh_-35_s_-10']['y'],drawstyle='steps-mid',color='tab:blue', alpha=1)
ax[0,3].tick_params(axis='both', which='major', labelsize=20)
ax[0,3].set_xlabel('Energy [keV]',fontsize=22)
ax[0,3].set_title('Io (RH)',color='black',fontsize=24)
ax[0,3].grid()

ax[1,0].plot(data_fig6['Gan_lh_-10_s_0']['x'],data_fig6['Gan_lh_-10_s_0']['y'],drawstyle='steps-mid',color='tab:orange', alpha=1)
ax[1,0].plot(data_fig6['Gan_lh_0_s_20']['x'],data_fig6['Gan_lh_0_s_20']['y'],drawstyle='steps-mid',color='tab:green', alpha=1)
ax[1,0].tick_params(axis='both', which='major', labelsize=20)
ax[1,0].set_xlabel('Energy [keV]',fontsize=22)
ax[1,0].set_ylabel('Nbr detections',fontsize=22)
ax[1,0].set_xscale('log')
ax[1,0].set_title('Ganymede (LH)',color='black',fontsize=24)
ax[1,0].grid()

ax[1,1].plot(data_fig6['Gan_lh_-35_s_-10']['x'],data_fig6['Gan_lh_-35_s_-10']['y'],drawstyle='steps-mid',color='tab:blue', alpha=1)
ax[1,1].tick_params(axis='both', which='major',labelsize=20)
ax[1,1].set_xlabel('Energy [keV]',fontsize=22)
ax[1,1].set_title('Ganymede (LH)',color='black',fontsize=24)
ax[1,1].grid()

ax[1,2].plot(data_fig6['Gan_rh_-10_s_0']['x'],data_fig6['Gan_rh_-10_s_0']['y'],drawstyle='steps-mid',color='tab:orange', alpha=1)
ax[1,2].plot(data_fig6['Gan_rh_0_s_20']['x'],data_fig6['Gan_rh_0_s_20']['y'],drawstyle='steps-mid',color='tab:green', alpha=1)
ax[1,2].tick_params(axis='both', which='major', labelsize=20)
ax[1,2].set_xlabel('Energy [keV]',fontsize=22)
ax[1,2].set_xscale('log')
ax[1,2].set_title('Ganymede (RH)',color='black',fontsize=24)
ax[1,2].grid()

ax[1,3].plot(data_fig6['Gan_rh_-35_s_-10']['x'],data_fig6['Gan_rh_-35_s_-10']['y'],drawstyle='steps-mid',color='tab:blue', alpha=1)
ax[1,3].tick_params(axis='both', which='major',labelsize=20)
ax[1,3].set_xlabel('Energy [keV]',fontsize=22)
ax[1,3].set_title('Ganymede (RH)',color='black',fontsize=24)
ax[1,3].grid()

ax[2,0].plot(data_fig6['Aur_lh_-10_s_0']['x'],data_fig6['Aur_lh_-10_s_0']['y'],drawstyle='steps-mid',color='tab:orange', alpha=1)
ax[2,0].plot(data_fig6['Aur_lh_0_s_20']['x'],data_fig6['Aur_lh_0_s_20']['y'],drawstyle='steps-mid',color='tab:green', alpha=1)
ax[2,0].tick_params(axis='both', which='major', labelsize=20)
ax[2,0].set_xlabel('Energy [keV]',fontsize=22)
ax[2,0].set_ylabel('Nbr detections',fontsize=22)
ax[2,0].set_xscale('log')
ax[2,0].set_title('Main aurora (LH)',color='black',fontsize=24)
ax[2,0].grid()

ax[2,1].plot(data_fig6['Aur_lh_-35_s_-10']['x'],data_fig6['Aur_lh_-35_s_-10']['y'],drawstyle='steps-mid',color='tab:blue', alpha=1)
ax[2,1].tick_params(axis='both', which='major',labelsize=20)
ax[2,1].set_xlabel('Energy [keV]',fontsize=22)
ax[2,1].set_title('Main aurora (LH)',color='black',fontsize=24)
ax[2,1].grid()

ax[2,2].plot(data_fig6['Aur_rh_-10_s_0']['x'],data_fig6['Aur_rh_-10_s_0']['y'],drawstyle='steps-mid',color='tab:orange', alpha=1)
ax[2,2].plot(data_fig6['Aur_rh_0_s_20']['x'],data_fig6['Aur_rh_0_s_20']['y'],drawstyle='steps-mid',color='tab:green', alpha=1)
ax[2,2].tick_params(axis='both', which='major', labelsize=20)
ax[2,2].set_xlabel('Energy [keV]',fontsize=22)
ax[2,2].set_xscale('log')
ax[2,2].set_title('Main aurora (RH)', color='black',fontsize=24)
ax[2,2].grid()

ax[2,3].plot(data_fig6['Aur_rh_-35_s_-10']['x'],data_fig6['Aur_rh_-35_s_-10']['y'],drawstyle='steps-mid',color='tab:blue', alpha=1)
ax[2,3].tick_params(axis='both',which='major',labelsize=20)
ax[2,3].set_xlabel('Energy [keV]',fontsize=22)
ax[2,3].set_title('Main aurora (RH)', color='black',fontsize=24)
ax[2,3].grid()


fig9.legend(loc='lower center', ncol=3, mode='expand',fontsize=22)
fig9.subplots_adjust(top=0.95, hspace=0.25,wspace=0.25,left=0.07,right=0.99, bottom=0.1)
fig9.savefig('Figure_6.pdf', dpi=150)
fig9.savefig('Figure_6.eps', dpi=150)

###################################################
#------------------- Figure 7 --------------------#
###################################################

print('------ Figure 7 ------')

Ppos=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Travail complementaire/results/Figures/Plots_article/Plot_pente_pos.sav')

tmin_tf=-((420-1)/2)/(420*2.6e-3) ; tmax_tf=((420-1)/2)/(420*2.6e-3)
fmin_tf=-((420-1)/2)/(420*21.35e-3) ; fmax_tf=((420-1)/2)/(420*21.35e-3)

plt.figure(figsize=(20,5))
plt.subplot(131)
ax1=plt.gca()
im1=ax1.imshow(jup.scale_spdyn(Ppos['xrh1']), origin='lower',extent=[0,(Ppos['tmax']-Ppos['tmin'])*3600,Ppos['fmin'],Ppos['fmax']],aspect=(Ppos['tmax']-Ppos['tmin'])*3600/(Ppos['fmax']-Ppos['fmin']),vmax=1.5,cmap='gray', alpha=1)
ax1.tick_params(axis='both', which='major', labelsize=20)
plt.xlabel('Time [s] from {:.6} h'.format(Ppos['tmin']),fontsize=22)
plt.ylabel('Frequency [MHz]',fontsize=22)
plt.title('Positive drift\n <df/dt>={:.4}'.format(Ppos['slope_rh']) + ' $MHz.s^{-1}$',fontsize=24)
cb1=plt.colorbar(im1, ax=ax1)
cb1.set_label('dB', fontsize=22)
cb1.ax.tick_params(labelsize=20)

plt.subplot(132)

ax2=plt.gca()
im2=ax2.imshow(np.log10(Ppos['tfrh1']), origin='lower',extent=[tmin_tf,tmax_tf,fmin_tf,fmax_tf],aspect=(tmax_tf-tmin_tf)/(fmax_tf-fmin_tf),vmin=-3.,cmap='magma',alpha=1)
ax2.tick_params(axis='both', which='major', labelsize=20)
plt.xlabel('Time$^{-1}$ [$s^{-1}$]',fontsize=22)
plt.ylabel('Frequency$^{-1}$ [$MHz^{-1}$]',fontsize=22)
plt.title('TF(SPDYN)',fontsize=24)
cb2=plt.colorbar(im2, ax=ax2)
cb2.set_label('dB', fontsize=22)
cb2.ax.tick_params(labelsize=20)

plt.subplot(133)
ax3=plt.gca()
ax3.plot(Ppos['theta_rd'],Ppos['rd_rh1o'], 'g--', linewidth=1, label='$RD_{original}$')
ax3.plot([-1,121],[0,0], color='black', linestyle='dashed', linewidth=1)
ax3.plot([60,60],[-0.04,0.13], color='black', linestyle='dashdot', linewidth=1)
ax3.plot(Ppos['theta_rd'],Ppos['rd_rh1'],'b-' ,linewidth=2,label='$RD_{centered}$')
ax3.plot(Ppos['theta_rd'], Ppos['fit_rh_all'], 'r--', linewidth=1, label='Gaussian Fit')
ax3.tick_params(axis='both', which='major', labelsize=20)
plt.xlim(0,120)
plt.ylim(-0.04,0.13)
plt.xlabel("Angles [°]",fontsize=22)
plt.xticks([0,20,40,60,80,100,120],[15,35,55,'75//105',125,145,165])
plt.ylabel("Intensity ",fontsize=22)
plt.legend(fontsize=15, mode='expand',loc='upper center', ncol=2)
plt.grid()
plt.title('RD(TF), SNR={:.5}'.format(Ppos['snr_rh']),fontsize=24)

plt.tight_layout()
plt.savefig('Figure_7.eps', dpi=150)
plt.savefig('Figure_7.pdf', dpi=150)


###################################################
#------------------- Figure 8 --------------------#
###################################################

print('------ Figure 8 ------')

data_fig8 = pd.read_excel('data_figure_8.xlsx', sheet_name=['Io_lh_-35_s_-10','Io_lh_-10_s_0','Io_lh_0_s_20','Io_rh_-35_s_-10','Io_rh_-10_s_0','Io_rh_0_s_20',
        'Gan_lh_-35_s_-10','Gan_lh_-10_s_0','Gan_lh_0_s_20','Gan_rh_-35_s_-10','Gan_rh_-10_s_0','Gan_rh_0_s_20',
        'Aur_lh_-35_s_-10','Aur_lh_-10_s_0','Aur_lh_0_s_20','Aur_rh_-35_s_-10','Aur_rh_-10_s_0','Aur_rh_0_s_20',])

plt.figure(figsize=(20,15))

plt.subplot(321)
ax1=plt.gca()
ax1.plot(data_fig8['Io_lh_-35_s_-10']['x'],data_fig8['Io_lh_-35_s_-10']['y'],drawstyle='steps-mid', alpha=1, color='tab:blue', label='$ s \leq -10$ MHz.s$^{-1}$')
ax1.plot(data_fig8['Io_lh_-10_s_0']['x'],data_fig8['Io_lh_-10_s_0']['y'],drawstyle='steps-mid', alpha=1, color='tab:orange',label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax1.plot(data_fig8['Io_lh_0_s_20']['x'],data_fig8['Io_lh_0_s_20']['y'],drawstyle='steps-mid', alpha=1, color='tab:green', label='$ s \geq 0$ MHz.s$^{-1}$')
ax1.tick_params(axis='both', which='major', labelsize=20)
plt.text(-2,4600, 'a)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('SNR',fontsize=22)
plt.ylabel('Nbr detections',fontsize=22)
plt.yscale('log')
plt.grid()
plt.legend(fontsize=16)
plt.title('Io (LH)',fontsize=24)

plt.subplot(322)
ax2=plt.gca()
ax2.plot(data_fig8['Io_rh_-35_s_-10']['x'],data_fig8['Io_rh_-35_s_-10']['y'],drawstyle='steps-mid', alpha=1, color='tab:blue', label='$ s \leq -10$ MHz.s$^{-1}$')
ax2.plot(data_fig8['Io_rh_-10_s_0']['x'],data_fig8['Io_rh_-10_s_0']['y'],drawstyle='steps-mid', alpha=1, color='tab:orange',label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax2.plot(data_fig8['Io_rh_0_s_20']['x'],data_fig8['Io_rh_0_s_20']['y'],drawstyle='steps-mid', alpha=1, color='tab:green', label='$ s \geq 0$ MHz.s$^{-1}$')
ax2.tick_params(axis='both', which='major', labelsize=20)
plt.text(-2,5100, 'b)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('SNR',fontsize=22)
plt.ylabel('Nbr detections',fontsize=22)
plt.yscale('log')
plt.grid()
plt.legend(fontsize=16)
plt.title('Io (RH)',fontsize=24)

plt.subplot(323)
ax3=plt.gca()
ax3.plot(data_fig8['Gan_lh_-35_s_-10']['x'],data_fig8['Gan_lh_-35_s_-10']['y'],drawstyle='steps-mid', alpha=1, color='tab:blue', label='$ s \leq -10$ MHz.s$^{-1}$')
ax3.plot(data_fig8['Gan_lh_-10_s_0']['x'],data_fig8['Gan_lh_-10_s_0']['y'],drawstyle='steps-mid', alpha=1, color='tab:orange',label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax3.plot(data_fig8['Gan_lh_0_s_20']['x'],data_fig8['Gan_lh_0_s_20']['y'],drawstyle='steps-mid', alpha=1, color='tab:green', label='$ s \geq 0$ MHz.s$^{-1}$')
ax3.tick_params(axis='both', which='major', labelsize=20)
plt.text(-2,240, 'c)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('SNR',fontsize=22)
plt.ylabel('Nbr detections',fontsize=22)
plt.grid()
plt.legend(fontsize=16)
plt.title('Ganymede (LH)',fontsize=24)

plt.subplot(324)
ax4=plt.gca()
ax4.plot(data_fig8['Gan_rh_-35_s_-10']['x'],data_fig8['Gan_rh_-35_s_-10']['y'],drawstyle='steps-mid', alpha=1, color='tab:blue', label='$ s \leq -10$ MHz.s$^{-1}$')
ax4.plot(data_fig8['Gan_rh_-10_s_0']['x'],data_fig8['Gan_rh_-10_s_0']['y'],drawstyle='steps-mid', alpha=1, color='tab:orange',label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax4.plot(data_fig8['Gan_rh_0_s_20']['x'],data_fig8['Gan_rh_0_s_20']['y'],drawstyle='steps-mid', alpha=1, color='tab:green', label='$ s \geq 0$ MHz.s$^{-1}$')
ax4.tick_params(axis='both', which='major', labelsize=20)
plt.text(-2,110, 'd)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('SNR',fontsize=22)
plt.ylabel('Nbr detections',fontsize=22)
plt.grid()
plt.legend(fontsize=16)
plt.title('Ganymede (RH)',fontsize=24)

plt.subplot(325)
ax5=plt.gca()
ax5.plot(data_fig8['Aur_lh_-35_s_-10']['x'],data_fig8['Aur_lh_-35_s_-10']['y'],drawstyle='steps-mid', alpha=1, color='tab:blue', label='$ s \leq -10$ MHz.s$^{-1}$')
ax5.plot(data_fig8['Aur_lh_-10_s_0']['x'],data_fig8['Aur_lh_-10_s_0']['y'],drawstyle='steps-mid', alpha=1, color='tab:orange',label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax5.plot(data_fig8['Aur_lh_0_s_20']['x'],data_fig8['Aur_lh_0_s_20']['y'],drawstyle='steps-mid', alpha=1, color='tab:green', label='$ s \geq 0$ MHz.s$^{-1}$')
ax5.tick_params(axis='both', which='major', labelsize=20)
plt.text(-2,290, 'e)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('SNR',fontsize=22)
plt.ylabel('Nbr detections',fontsize=22)
plt.grid()
plt.legend(fontsize=16)
plt.title('Main aurora (LH)',fontsize=24)

plt.subplot(326)
ax6=plt.gca()
ax6.plot(data_fig8['Aur_rh_-35_s_-10']['x'],data_fig8['Aur_rh_-35_s_-10']['y'],drawstyle='steps-mid', alpha=1, color='tab:blue', label='$ s \leq -10$ MHz.s$^{-1}$')
ax6.plot(data_fig8['Aur_rh_-10_s_0']['x'],data_fig8['Aur_rh_-10_s_0']['y'],drawstyle='steps-mid', alpha=1, color='tab:orange',label='$ -10 \leq s \leq 0$ MHz.s$^{-1}$')
ax6.plot(data_fig8['Aur_rh_0_s_20']['x'],data_fig8['Aur_rh_0_s_20']['y'],drawstyle='steps-mid', alpha=1, color='tab:green', label='$ s \geq 0$ MHz.s$^{-1}$')
ax6.tick_params(axis='both', which='major', labelsize=20)
plt.text(-2,620, 'f)', color='black',fontsize=24,fontweight='bold')
plt.xlabel('SNR',fontsize=22)
plt.ylabel('Nbr detections',fontsize=22)
plt.grid()
plt.legend(fontsize=16)
plt.title('Main aurora (RH)',fontsize=24)

plt.tight_layout()
plt.savefig('Figure_8.pdf', dpi=150)
plt.savefig('Figure_8.eps', dpi=150)


###################################################
#------------------- Figure 9 --------------------#
###################################################

# Context observations, made by hand.

###################################################
#------------------- Figure 10 -------------------#
###################################################

print('------ Figure 10 ------')

data_fig10 = pd.read_excel('data_figure_10.xlsx', sheet_name=['GanC_lh_-35_s_-10','GanC_lh_-10_s_0','GanC_lh_0_s_20','GanC_rh_-35_s_-10','GanC_rh_-10_s_0','GanC_rh_0_s_20'])

plt.figure(figsize=(15,5))

plt.subplot(121)
ax1=plt.gca()
ax1.plot(data_fig10['GanC_lh_-35_s_-10']['x'],data_fig10['GanC_lh_-35_s_-10']['y'],drawstyle='steps-mid', alpha=1, color='tab:blue')
ax1.plot(data_fig10['GanC_lh_-10_s_0']['x'],data_fig10['GanC_lh_-10_s_0']['y'],drawstyle='steps-mid', alpha=1, color='tab:orange')
ax1.plot(data_fig10['GanC_lh_0_s_20']['x'],data_fig10['GanC_lh_0_s_20']['y'],drawstyle='steps-mid', alpha=1, color='tab:green')
ax1.tick_params(axis='both', which='major', labelsize=16)
plt.xlabel('Slopes [MHz/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.ylim(-3,1.1*np.max(data_fig10['GanC_lh_-10_s_0']['y']))
plt.grid()
plt.title('Ganymede C (LH)',fontsize=20)

plt.subplot(122)
ax1=plt.gca()
ax1.plot(data_fig10['GanC_rh_-35_s_-10']['x'],data_fig10['GanC_rh_-35_s_-10']['y'],drawstyle='steps-mid', alpha=1, color='tab:blue')
ax1.plot(data_fig10['GanC_rh_-10_s_0']['x'],data_fig10['GanC_rh_-10_s_0']['y'],drawstyle='steps-mid', alpha=1, color='tab:orange')
ax1.plot(data_fig10['GanC_rh_0_s_20']['x'],data_fig10['GanC_rh_0_s_20']['y'],drawstyle='steps-mid', alpha=1, color='tab:green')
ax1.tick_params(axis='both', which='major', labelsize=16)
plt.xlabel('Slopes [MHz/s]',fontsize=18)
plt.ylabel('Nbr detections',fontsize=18)
plt.ylim(-3,1.1*np.max(data_fig10['GanC_rh_-10_s_0']['y']))
plt.grid()
plt.title('Ganymede C (RH)',fontsize=20)

plt.tight_layout()
plt.savefig('Figure_10.pdf', dpi=150)

