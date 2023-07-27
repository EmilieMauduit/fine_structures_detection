from operator import is_not
import os
import scipy.io as sio
from scipy.io import readsav
import matplotlib.pyplot as plt
import matplotlib.image as img
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from astropy.time import Time



###### Identification of the type of emissions

## Contours Io

IoAcml=[205.,220,220,240,240,245,245,265,265,270,270,275,275,245,245,215,215,200,200,190,190,185,185,190,190,195,195,200,200,205,205]
IoAphi=[185.,185,190,190,195,195,200,200,205,205,230,230,265,265,260,260,255,255,250,250,245,245,230,230,225,225,205,205,190,190,185]
IoA1cml=[205.,225,225,255,255,265,265,235,235,210,210,200,200,205,205]
IoA1phi=[160.,160,165,165,170,170,195,195,190,190,185,185,165,165,160]
IoA2cml=[315.,335,335,345,345,325,325,300,300,305,305,315,315]
IoA2phi=[220.,220,225,225,240,240,245,245,230,230,225,225,220]
IoBcml=[ 90.,105,105,115,115,130,130,155,155,175,175,185,185,195,195,200,200,180,180,110,110, 95, 95, 90, 90, 80, 80, 75, 75, 90, 90]
IoBphi=[ 55., 55, 70, 70, 75, 75, 80, 80, 85, 85, 90, 90, 95, 95,100,100,115,115,110,110,105,105,100,100, 95, 95, 90, 90, 65, 65, 55]
IoB1cml=[130.,165,165,175,175,180,180,185,185,165,165,145,145,130,130]
IoB1phi=[ 65., 65, 70, 70, 75, 75, 80, 80, 95, 95, 90, 90, 85, 85, 65]
IoCcml=[290.,310,310,320,320,345,345,360,360,315,315,295,295,290,290,275,275,270,270,280,280,290,290]
IoCphi=[215.,215,220,220,225,225,235,235,260,260,255,255,250,250,245,245,240,240,225,225,220,220,215]
IoC0cml=[  0., 45, 45, 20, 20,  0,  0]
IoC0phi=[240.,240,255,255,260,260,240]
IoDcml=[ 20., 55, 55,175,175,190,190,230,230,185,185,115,115, 30, 30, 20, 20]
IoDphi=[ 95., 95,100,100,105,105,110,110,125,125,120,120,115,115,110,110, 95]


def inboxio (x,y):
    #IoA
    if ( ((x >= 184.5) and (x <=190.5) and (y >= 229.5) and (y<= 245.5)) or ((x >= 189.5) and (x <=200.5) and (y >= 224.5) and (y<= 250.5)) or ((x >= 194.5) and (x <=200.5) and (y >= 204.5) and (y<= 225.5)) or ((x >= 199.5) and (x <=215.5) and (y >= 189.5) and (y<= 255.5)) or ((x >= 204.5) and (x <=220.5) and (y >= 184.5) and (y<= 190.5)) or ((x >= 214.5) and (x <=240.5) and (y >= 189.5) and (y<= 260.5)) or ((x >= 239.5) and (x <=245.5) and (y >= 194.5) and (y<= 260.5)) or ((x >= 244.5) and (x <=265.5) and (y >= 199.5) and (y<= 265.5)) or ((x >= 264.5) and (x <=270.5) and (y >= 204.5) and (y<= 265.5)) or ((x >= 269.5) and (x <=275.5) and (y >= 229.5) and (y<= 265.5)) ):
        return (True)
    #IoA1
    elif( ((x >= 234.5) and (x <=265.5) and (y >= 169.5) and (y<= 195.5)) or ((x >= 209.5) and (x <=235.5) and (y >= 169.5) and (y<= 190.5)) or ((x >= 199.5) and (x <=210.5) and (y >= 169.5) and (y<= 185.5)) or ((x >= 199.5) and (x <=255.5) and (y >= 164.5) and (y<= 169.5)) or ((x >= 204.5) and (x <=225.5) and (y >= 159.5) and (y<= 165.5)) ):
        return(True)
    #IoA2
    elif(((x >= 299.5) and (x <=325.5) and (y >= 229.5) and (y<= 245.5)) or ((x >= 304.5) and (x <=325.5) and (y >= 224.5) and (y<= 230.5)) or ((x >= 324.5) and (x <=345.5) and (y >= 224.5) and (y<= 240.5)) or ((x >= 314.5) and (x <=335.5) and (y >= 219.5) and (y<= 225.5)) ):
        return(True)
    #IoB
    elif(((x >= 74.5) and (x <=90.5) and (y >= 64.5) and (y<= 90.5)) or ((x >= 89.5) and (x <=105.5) and (y >= 54.5) and (y<= 70.5)) or ((x >= 79.5) and (x <=90.5) and (y >= 89.5) and (y<= 95.5)) or ((x >= 89.5) and (x <=115.5) and (y >= 69.5) and (y<= 100.5)) or ((x >= 94.5) and (x <=110.5) and (y >= 99.5) and (y<= 105.5)) or ((x >= 109.5) and (x <=130.5) and (y >= 74.5) and (y<= 110.5)) or ((x >= 129.5) and (x <=155.5) and (y >= 79.5) and (y<= 110.5)) or ((x >= 154.5) and (x <=175.5) and (y >= 84.5) and (y<= 110.5)) or ((x >= 174.5) and (x <=185.5) and (y >= 89.5) and (y<= 110.5)) or ((x >= 184.5) and (x <=195.5) and (y >= 94.5) and (y<= 100.5)) or ((x >= 179.5) and (x <=200.5) and (y >= 99.5) and (y<= 115.5)) ):
        return(True)
    #IoB1
    elif(((x >= 129.5) and (x <=165.5) and (y >= 64.5) and (y<= 85.5))or ((x >= 144.5) and (x <=165.5) and (y >= 84.5) and (y<= 90.5)) or ((x >= 164.5) and (x <=175.5) and (y >= 69.5) and (y<= 95.5)) or ((x >= 174.5) and (x <=180.5) and (y >= 74.5) and (y<= 95.5))or ((x >= 179.5) and (x <=185.5) and (y >= 79.5) and (y<= 95.5))):
        return(True)
    #IoC
    elif( ((x >= 314.5) and (x <=360) and (y >= 234.5) and (y<= 260.5)) or ((x >= 294.5) and (x <=345.5) and (y >= 224.5) and (y<= 255.5))or ((x >= 289.5) and (x <=320.5) and (y >= 219.5) and (y<= 250.5)) or ((x >= 289.5) and (x <=310.5) and (y >= 214.5) and (y<= 220.5)) or ((x >= 279.5) and (x <=290.5) and (y >= 219.5) and (y<= 245.5)) or ((x >= 274.5) and (x <=280.5) and (y >= 224.5) and (y<= 245.5)) or ((x >= 269.5) and (x <=275.5) and (y >= 224.5) and (y<= 240.5))):
        return(True)
    #IoC0
    elif( ((x >= 0) and (x <=20.5) and (y >= 239.5) and (y<= 260.5)) or ((x >= 19.5) and (x <=45.5) and (y >= 239.5) and (y<= 255.5))):
        return(True)
    #IoD
    elif( ((x >= 19.5) and (x <=55.5) and (y >= 94.5) and (y<= 110.5)) or ((x >= 29.5) and (x <=175.5) and (y >= 99.5) and (y<= 115.5)) or ((x >= 114.5) and (x <=230.5) and (y >= 109.5) and (y<= 120.5)) or ((x >= 184.5) and (x <=230.5) and (y >= 119.5) and (y<= 125.5))):
        return(True)
    else :
        return (False)

## Contours Ganymède

GaAcml=[285.,340,340,285,285]
GaAphi=[195.,195,240,240,195]
GaBcml=[110.,175,175,110,110]
GaBphi=[ 75., 75,100,100, 75]
GaB1cml=[125.,170,170,125,125]
GaB1phi=[ 25., 25, 75, 75, 25]
GaCcml=[315.,360,360,315,315]
GaCphi=[235.,235,260,260,235]
GaC0cml=[  0., 40, 40, 0,  0]
GaC0phi=[240.,240,260,260,240]
GaDcml=[125.,180,180,125,125]
GaDphi=[190.,190,210,210,190]

#cmap1=copy(copy(plt.cm.nipy_spectral))

def inboxgan(x,y):
    #Gan A
    if ((x <= 340.5) and (x >= 284.5) and (y <= 240.5) and (y >= 194.5)):
        return(True)
    #Gan B 
    elif ((x <= 175.5) and (x >= 109.5) and (y <= 100.5) and (y >= 74.5)) :
        return True
    #Gan B'
    elif ((x <= 170.5) and (x >= 124.5) and (y <= 75.5) and (y >= 24.5)) :
        return True
    #Gan C
    elif (((x <= 360) and (x >= 314.5) and (y <= 260.5) and (y >= 234.5)) or ((x <= 40.5) and (x >= 0) and (y <= 260.5) and (y >= 239.5)))  :
        return True
    #Gan D
    elif ((x <= 180.5) and (x >= 124.5) and (y <= 210.5) and (y >= 189.5)) :
        return True
    else :
        return(False)

def inboxganB(x,y):
    if ((x <= 204.) and (x >= 109.5) and (y <= 100.5) and (y >= 74.5)) :
        return True
    else :
        return False

def inboxganC(x,y) :
    if (((x <= 360) and (x >= 314.5) and (y <= 260.5) and (y >= 234.5)) or ((x <= 40.5) and (x >= 0) and (y <= 260.5) and (y >= 239.5))) :
        return True
    else : 
        return False

## Contours Europe

EurAcml=[200,200,290,290,200] ; EurAphi=[230,260,260,230,230]
EurC1cml = [280,280,360,360,280] ; EurC1phi = [ 240,268,268,240,240]
EurC2cml = [0,0,20,20,0] ; EurC2phi = [ 240,268,268,240,240]
EurDcml = [165,165,290,290,165] ; EurDphi = [120,145,145,120,120]

def inboxeuropa(x,y):
    #Eur A
    if ((x >= 200.) and (x <= 290.) and (y >= 230.) and (y <= 260.)):
        return True
    #Eur C
    elif (((x >= 280.) and (x <= 360.)) or ((x >= 0.) and (x <= 20.))) and ((y >= 240.) and (y <= 268.)):
        return True
    #Eur D
    elif ((x >= 165.) and (x <= 290.) and (y >= 120.) and (y <= 145.)):
        return True
    else :
        return False
### Sorting emissions

def sort_emissions_phio(x,y, xga, yga):
    dim=np.shape(x)
    n=dim[0]
    x_io=[]
    y_io=[]
    x_ga=[]
    y_ga=[]
    x_eu=[]
    y_eu=[]

    for i in range(n):

        if (inboxio(x[i],y[i])==True) :
            x_io.append(x[i])
            y_io.append(y[i])
        else :
            if (inboxgan(xga[i],yga[i])==True) :
                x_ga.append(x[i])
                y_ga.append(y[i])
            else :
                x_eu.append(x[i])
                y_eu.append(y[i])
    return(x_io,y_io,x_ga,y_ga,x_eu,y_eu)

def sort_emissions_phiga(x,y,xio,yio):
    dim=np.shape(x)
    n=dim[0]
    x_io=[]
    y_io=[]
    x_ga=[]
    y_ga=[]
    x_eu=[]
    y_eu=[]

    for i in range(n):

        if (inboxio(xio[i],yio[i])==True) :
            x_io.append(x[i])
            y_io.append(y[i])
        else :
            if (inboxgan(x[i],y[i])==True) :
                x_ga.append(x[i])
                y_ga.append(y[i])
            else :
                x_eu.append(x[i])
                y_eu.append(y[i])
    return(x_io,y_io,x_ga,y_ga,x_eu,y_eu)

def sort_emissions_phieu(x,y,xio,yio,xga,yga):
    dim=np.shape(x)
    n=dim[0]
    x_io=[] ; y_io=[]
    x_ga=[] ; y_ga=[]
    x_eu=[] ; y_eu=[]
    x_au=[] ; y_au =[]

    for i in range(n):

        if (inboxio(xio[i],yio[i])==True) :
            x_io.append(x[i])
            y_io.append(y[i])
        else :
            if (inboxgan(xga[i],yga[i])==True) :
                x_ga.append(x[i])
                y_ga.append(y[i])
            else :
                if (inboxeuropa(x[i],y[i]) == True) :
                    x_eu.append(x[i])
                    y_eu.append(y[i])
                else :
                    x_au.append(x[i])
                    y_au.append(y[i])
    return(x_io,y_io,x_ga,y_ga,x_eu,y_eu, x_au,y_au)



def select_dates(x,y,date,times):
    date_jd=Time(date).jd
    times_jd=Time(times,format='jd')
    x_out=[]
    y_out=[]
    for i in range(len(times_jd.value)):
        if (date_jd <= times_jd.value[i] <= date_jd+1.0):
            x_out.append(x[i])
            y_out.append(y[i])
    return(x_out,y_out)

def select_slope(x,y,slopes,smax,smin):
    x_out=[]
    y_out=[]
    for i in range(len(slopes)):
        if smin <= slopes[i] <= smax :
            x_out.append(x[i])
            y_out.append(y[i])
    return(x_out,y_out)

### Scaling

def scale_spdyn(x):
    dim=np.shape(x)
    y=x.copy()
    for i in range (dim[0]):
        for j in range(dim[1]):
            if (y[i][j] > 1.5):
                y[i][j] = 1.5
            elif (y[i][j] < 1.0):
                y[i][j] = 1.0
    return(y)

### Probability maps for the plots ###


data1=readsav(r'/Users/emauduit/Documents/Stage Jupiter 2021/Stage/Programmes/Traitement massif/probas_cartes.sav')

carte_io=data1['probaio']
carte_gan=data1['probagan']

max_io=np.quantile(carte_io,0.99)
max_gan=np.quantile(carte_gan,0.95)


## Io - CML : plots io phase coordinates with respect to cml coordinates onto Io emissions probability map

def io(xlh,ylh, xgalh, ygalh,xrh,yrh,xgarh,ygarh,times_lh=None,times_rh=None, date=None,slope_lh=None,slope_rh=None,slope_max=None,slope_min=None):
    ax=plt.gca()
    im=ax.imshow(carte_io, origin='lower',extent=[0,360,0,360], vmax=max_io,cmap='gray', alpha=0.8)
    ax.tick_params(axis='both', which='major', labelsize=20)
    plt.text(1,5, 'a)', color='white',fontsize=20,fontweight='bold')
    plt.xlabel('CML (°)',fontsize=22)
    plt.ylabel('Io phase (°)',fontsize=22)
    #plt.title(legends)

    if times_lh is not None and times_rh is not None and date is not None :
        xlh,ylh=select_dates(xlh,ylh,date=date,times=times_lh)
        xrh,yrh=select_dates(xrh,yrh,date=date,times=times_rh)
        xgalh,ygalh=select_dates(xgalh,ygalh,date=date,times=times_lh)
        xgarh,ygarh=select_dates(xgarh,ygarh,date=date,times=times_rh)
    if slope_lh is not None and slope_rh is not None and slope_max is not None and slope_min is not None:
        xlh,ylh=select_slope(xlh,ylh,slope_lh,slope_max,slope_min)
        xrh,yrh=select_slope(xrh,yrh,slope_rh,slope_max,slope_min)
        xgalh,ygalh=select_slope(xgalh,ygalh,slope_lh,slope_max,slope_min)
        xgarh,ygarh=select_slope(xgarh,ygarh,slope_rh,slope_max,slope_min)

    x_iolh,y_iolh,x_galh,y_galh,x_eulh,y_eulh=sort_emissions_phio(xlh, ylh, xgalh, ygalh)
    x_iorh,y_iorh,x_garh,y_garh,x_eurh,y_eurh=sort_emissions_phio(xrh, yrh, xgarh, ygarh)

    print('IO : LH : ',len(x_iolh), ', RH :', len(x_iorh))
    print('GAN : LH : ',len(x_galh), ', RH :', len(x_garh))
    print('AUR : LH : ',len(x_eulh), ', RH :', len(x_eurh))


    plt.plot(x_iolh, y_iolh, "x",markersize=12,markeredgecolor='royalblue',markeredgewidth=1,markerfacecolor='none', label='Io - LH')
    plt.plot(x_galh, y_galh,"x",markersize=12, markeredgecolor='yellowgreen',markeredgewidth=1,markerfacecolor='none', label='Gan - LH')
    plt.plot(x_eulh, y_eulh, "x",markersize=12,markeredgecolor='lightpink',markeredgewidth=1, markerfacecolor='none',label='Non-Io, Non-Gan - LH')
    plt.plot(x_iorh, y_iorh,"+",markersize=12,markeredgecolor='royalblue',markeredgewidth=1,markerfacecolor='none', label='Io - RH')
    plt.plot(x_garh, y_garh,"+",markersize=12, markeredgecolor='yellowgreen', markeredgewidth=1,markerfacecolor='none',label='Gan - RH')
    plt.plot(x_eurh, y_eurh,"+",markersize=12,markeredgecolor='lightpink',markeredgewidth=1,markerfacecolor='none', label='Non-Io, Non-Gan - RH')
    plt.plot(IoAcml,IoAphi, '-', color='white')
    plt.plot(IoA1cml,IoA1phi, '--', color='white')
    plt.plot(IoA2cml,IoA2phi, '--', color='white')
    plt.plot(IoBcml,IoBphi, '-', color='white')
    plt.plot(IoB1cml,IoB1phi, '--', color='white')
    plt.plot(IoCcml,IoCphi, '-', color='white')
    plt.plot(IoC0cml,IoC0phi, '--', color='white')
    plt.plot(IoDcml,IoDphi, '-', color='white')
    plt.text(225,275,'A',color='white', fontsize=16,fontweight='demibold')
    plt.text(170,170,"A'",color='white', fontsize=16,fontweight='demibold')
    plt.text(315,195,'A"',color='white', fontsize=16,fontweight='demibold')
    plt.text(50,60,'B',color='white', fontsize=16,fontweight='demibold')
    plt.text(185,60,"B'",color='white', fontsize=16,fontweight='demibold')
    plt.text(310,270,'C',color='white', fontsize=16,fontweight='demibold')
    plt.text(5,270,'C',color='white', fontsize=16,fontweight='demibold')
    plt.text(60,125,'D',color='white', fontsize=16,fontweight='demibold')
    plt.xlim(0,360)
    plt.ylim(0,360)
    plt.legend(bbox_to_anchor=(0.,0.91,2.37, 0.2),loc='upper left',markerscale=1.3, mode='expand',ncol=6, fontsize=18)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cb=plt.colorbar(im, cax=cax)
    cb.set_label('%', fontsize=20)
    cb.ax.tick_params(labelsize=18)
    return()


### Gan-CML : plots Ganymede phase coordinates with respect to cml coordinates onto Ganymede emissions probability map in different colors whereas it is Io or non-Io emissions

def gan(xlh,ylh,xiolh,yiolh,xrh,yrh,xiorh,yiorh,times_lh=None,times_rh=None,date=None,slope_lh=None,slope_rh=None,slope_max=None,slope_min=None):
    ax=plt.gca()
    im=ax.imshow(carte_gan, origin='lower',extent=[0,360,0,360],vmax=max_gan,cmap='gray',alpha=0.8)
    ax.tick_params(axis='both', which='major', labelsize=20)
    plt.text(1,5, 'b)', color='white',fontsize=20,fontweight='bold')
    plt.xlabel('CML (°)', fontsize=22)
    plt.ylabel('Ganymede phase (°)', fontsize=22)

    if times_lh is not None and times_rh is not None and date is not None :
        xiolh,yiolh=select_dates(xiolh,yiolh,date=date,times=times_lh)
        xiorh,yiorh=select_dates(xiorh,yiorh,date=date,times=times_rh)
        xlh,ylh=select_dates(xlh,ylh,date=date,times=times_lh)
        xrh,yrh=select_dates(xrh,yrh,date=date,times=times_rh)

    if slope_lh is not None and slope_rh is not None and slope_max is not None and slope_min is not None:
        xlh,ylh=select_slope(xlh,ylh,slope_lh,slope_max,slope_min)
        xrh,yrh=select_slope(xrh,yrh,slope_rh,slope_max,slope_min)
        xiolh,yiolh=select_slope(xiolh,yiolh,slope_lh,slope_max,slope_min)
        xiorh,yiorh=select_slope(xiorh,yiorh,slope_rh,slope_max,slope_min)


    x_iolh,y_iolh,x_galh,y_galh,x_eulh,y_eulh=sort_emissions_phiga(xlh, ylh, xiolh, yiolh)
    x_iorh,y_iorh,x_garh,y_garh,x_eurh,y_eurh=sort_emissions_phiga(xrh, yrh, xiorh, yiorh)

    print('IO : LH : ',len(x_iolh), ', RH :', len(x_iorh))
    print('GAN : LH : ',len(x_galh), ', RH :', len(x_garh))
    print('AUR : LH : ',len(x_eulh), ', RH :', len(x_eurh))

    plt.plot(x_iolh, y_iolh, "x",markersize=12,markeredgecolor='royalblue',markeredgewidth=1,markerfacecolor='none', label='Io - LH')
    plt.plot(x_galh, y_galh,"x",markersize=12, markeredgecolor='yellowgreen',markeredgewidth=1,markerfacecolor='none', label='Gan - LH')
    plt.plot(x_eulh, y_eulh, "x",markersize=12,markeredgecolor='lightpink',markeredgewidth=1, markerfacecolor='none',label='Non-Io, Non-Gan, LH')
    plt.plot(x_iorh, y_iorh,"+",markersize=12,markeredgecolor='royalblue',markeredgewidth=1,markerfacecolor='none', label='Io - RH')
    plt.plot(x_garh, y_garh,"+",markersize=12, markeredgecolor='yellowgreen', markeredgewidth=1,markerfacecolor='none',label='Gan - RH')
    plt.plot(x_eurh, y_eurh,"+",markersize=12,markeredgecolor='lightpink',markeredgewidth=1,markerfacecolor='none', label='Non-Io, Non-Gan, RH')
    plt.plot(GaAcml, GaAphi,'-', color='white')
    plt.plot(GaBcml, GaBphi,'-', color='white')
    plt.plot(GaB1cml, GaB1phi,'--', color='white')
    plt.plot(GaCcml, GaCphi,'-', color='white')
    plt.plot(GaC0cml, GaC0phi,'--', color='white')
    plt.plot(GaDcml, GaDphi,'-', color='white')
    plt.text(335,175,'A',color='white', fontsize=16,fontweight='demibold')
    plt.text(120,105,'B',color='white', fontsize=16,fontweight='demibold')
    plt.text(180,50,"B'",color='white', fontsize=16,fontweight='demibold')
    plt.text(345,270,'C',color='white', fontsize=16,fontweight='demibold')
    plt.text(10,270,'C',color='white', fontsize=16,fontweight='demibold')
    plt.text(100,190,'D',color='white', fontsize=16,fontweight='demibold')
    plt.xlim(0,360)
    plt.ylim(0,360)
    #plt.legend()
    #plt.tight_layout()
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cb=plt.colorbar(im, cax=cax)
    cb.set_label('%', fontsize=22)
    cb.ax.tick_params(labelsize=18)
    return()

## Europa- CML : plots Europa phase coordinates with respect to cml coordinates onto non-Io emissions probability map in different colors whereas it is Io or Gan or non-Io/non-Gan emissions

def europa(xlh,ylh,xiolh,yiolh,xgalh,ygalh,xrh,yrh,xiorh,yiorh,xgarh,ygarh,times_lh=None,times_rh=None,date=None,slope_lh=None,slope_rh=None,slope_max=None,slope_min=None):
    ax=plt.gca()
    im=ax.imshow(carte_gan, origin='lower',extent=[0,360,0,360],vmax=max_gan,cmap='gray',alpha=0.8)
    ax.tick_params(axis='both', which='major', labelsize=14)
    plt.xlabel('CML (°)', fontsize=18)
    plt.ylabel('Europa phase (°)', fontsize=18)

    if times_lh is not None and times_rh is not None and date is not None :
        xiolh,yiolh=select_dates(xiolh,yiolh,date=date,times=times_lh)
        xiorh,yiorh=select_dates(xiorh,yiorh,date=date,times=times_rh)
        xgalh,ygalh=select_dates(xgalh,ygalh,date=date,times=times_lh)
        xgarh,ygarh=select_dates(xgarh,ygarh,date=date,times=times_rh)
        xlh,ylh=select_dates(xlh,ylh,date=date,times=times_lh)
        xrh,yrh=select_dates(xrh,yrh,date=date,times=times_rh)
    
    if slope_lh is not None and slope_rh is not None and slope_max is not None and slope_min is not None:
        xlh,ylh=select_slope(xlh,ylh,slope_lh,slope_max,slope_min)
        xrh,yrh=select_slope(xrh,yrh,slope_rh,slope_max,slope_min)
        xiolh,yiolh=select_slope(xiolh,yiolh,slope_lh,slope_max,slope_min)
        xiorh,yiorh=select_slope(xiorh,yiorh,slope_rh,slope_max,slope_min)
        xgalh,ygalh=select_slope(xgalh,ygalh,slope_lh,slope_max,slope_min)
        xgarh,ygarh=select_slope(xgarh,ygarh,slope_rh,slope_max,slope_min)

    x_iolh,y_iolh,x_galh,y_galh,x_eulh,y_eulh, x_aulh,y_aulh=sort_emissions_phieu(xlh, ylh, xiolh, yiolh,xgalh,ygalh)
    x_iorh,y_iorh,x_garh,y_garh,x_eurh,y_eurh, x_aurh,y_aurh=sort_emissions_phieu(xrh, yrh, xiorh, yiorh,xgarh,ygarh)

    print('IO : LH : ',len(x_iolh), ', RH :', len(x_iorh))
    print('GAN : LH : ',len(x_galh), ', RH :', len(x_garh))
    print('AUR : LH : ',len(x_eulh), ', RH :', len(x_eurh))

    plt.plot(x_iolh, y_iolh, "x",markersize=10,markeredgecolor='royalblue',markeredgewidth=0.5,markerfacecolor='none', label='Io - LH')
    plt.plot(x_galh, y_galh,"x",markersize=10, markeredgecolor='yellowgreen',markeredgewidth=0.5,markerfacecolor='none', label='Gan - LH')
    plt.plot(x_eulh, y_eulh, "x",markersize=10,markeredgecolor='lightpink',markeredgewidth=0.5, markerfacecolor='none',label='Eur - LH') #'firebrick'
    plt.plot(x_aulh, y_aulh, "x",markersize=10,markeredgecolor='lightpink',markeredgewidth=0.5, markerfacecolor='none',label='Non-Io, Non-Gan, LH')
    plt.plot(x_iorh, y_iorh,"+",markersize=10,markeredgecolor='royalblue',markeredgewidth=0.5,markerfacecolor='none', label='Io - RH')
    plt.plot(x_garh, y_garh,"+",markersize=10, markeredgecolor='yellowgreen', markeredgewidth=0.5,markerfacecolor='none',label='Gan - RH')
    plt.plot(x_eurh, y_eurh,"+",markersize=10,markeredgecolor='lightpink',markeredgewidth=0.5,markerfacecolor='none', label='Eur - RH')
    plt.plot(x_aurh, y_aurh,"+",markersize=10,markeredgecolor='lightpink',markeredgewidth=0.5,markerfacecolor='none', label='Non-Io, Non-Gan, RH')
    plt.plot(EurAcml, EurAphi,'-', color='white')
    plt.plot(EurC1cml, EurC1phi,'-', color='white')
    plt.plot(EurC2cml, EurC2phi,'-', color='white')
    plt.plot(EurDcml, EurDphi,'--', color='white')
    plt.xlim(0,360)
    plt.ylim(0,360)
    #plt.legend(bbox_to_anchor=(0.,0.91,1.0, 0.2),loc='upper left',markerscale=1.3, mode='expand',ncol=4, fontsize=14)
    #plt.tight_layout()
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cb=plt.colorbar(im, cax=cax)
    cb.set_label('%', fontsize=18)
    cb.ax.tick_params(labelsize=14)

    return()


#### Callisto - CML : plots Callisto phase coordinates with respect to cml coordinates onto non-Io emissions probability map in different colors whereas it is Io or Gan or non-Io/non-Gan emissions

def callisto(x,y,title, legends, markers):
    plt.imshow(carte_gan, origin='lower',extent=[0,360,0,360],vmax=max_gan,cmap='jet')
    plt.xlabel('CML (°)')
    plt.ylabel('Calisto phase (°)')
    for i in range (0,len(x)):
        plt.plot(x[i], y[i], markers[i], label=legends[i],color='black')
    plt.xlim(0,360)
    plt.ylim(0,360)
    cb=plt.colorbar()
    cb.set_label('%', fontsize='large')
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()
    plt.title(title)
    return()

#### Amalthea - CML : plots Amalthea phase coordinates with respect to cml coordinates onto non-Io emissions probability map in different colors whereas it is Io or Gan or non-Io/non-Gan emissions

def amalthea(x,y,title, legends, markers):
    plt.imshow(carte_gan, origin='lower',extent=[0,360,0,360],vmax=max_gan,cmap='jet')
    plt.xlabel('CML (°)')
    plt.ylabel('Amaltha phase (°)')
    for i in range (0,len(x)):
        plt.plot(x[i], y[i], markers[i], label=legends[i],color='black')
    plt.xlim(0,360)
    plt.ylim(0,360)
    cb=plt.colorbar()
    cb.set_label('%', fontsize='large')
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()
    plt.title(title)
    return()






