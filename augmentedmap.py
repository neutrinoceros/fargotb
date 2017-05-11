#!/usr/bin/python
#-*-coding:utf-8-*-
# --------------------------
# Author : Clément Robert
# written may 2017
# --------------------------

from lib_parsing import * # built-in module that comes with the toolbox
import matplotlib.pyplot as plt
import argparse

#issues
#     * background should be azimuthally cropped for the colormap to have correct scaling
#     * xticks are uniformative in case of azimcropping
#     * bug : ./augmentedmap.py ../data/in/phase0.par 20 -c 10 -tc yields wrong yticks

#enhancements 
#     * we could add the option of using cartesian coordinates
#     * logscaling is not taken into account yet
#     * yticks could be better

# Defintions **********************************************************

def Hill_radius(r_p,q_p) :
    return r_p*(q_p/3)**(1./3)

def findRadialLimits(r_p,q_p,rads,croper=5.) :
    R_H = Hill_radius(r_p,q_p)
    nr = len(rads)
    jmin,jmax = 0,nr-1
    while rads[jmin] < r_p-croper*R_H :
        jmin +=1
    while rads[jmax-2] > r_p+croper*R_H :
        jmax -=1
    return jmin,jmax

def findAzimLimits(r_p,q_p,thetas,croper=5.) :
    R_H = Hill_radius(r_p,q_p)
    ns = len(thetas)
    imin,imax = 0,ns-1
    while r_p*thetas[imin] < -croper*R_H :
        imin +=1
    while r_p*thetas[imax-1] > croper*R_H :
        imax -=1
    return imin,imax

def crop_field(field,jmin,jmax) :
    cfield = field[jmin:jmax,:]
    return cfield

def rotate(field,thetas,theta_p) :
    ns = len(thetas)
    i_p = 0
    while thetas[i_p] < theta_p :
        i_p += 1

    cesure  = ns/2 - i_p
    ffield1 = np.concatenate((field[:,-cesure:ns-1],field[:,0:i_p]),axis=1)
    ffield2 = field[:,i_p:-cesure]
    ffield  = np.concatenate((ffield1,ffield2),axis=1)
    return ffield

def circle(x0,y0,r,theta) :
    return x0+r*np.cos(theta), y0+r*np.sin(theta)


# PARSING *************************************************************

parser = argparse.ArgumentParser()
# mandatories --------------------------------------------------------
parser.add_argument("config")
parser.add_argument("NOUT", type=int)
# switches -----------------------------------------------------------
parser.add_argument('-tc','--thetacrop',   action= 'store_true',
                    help="crop the figure in the azimuthal direction")
parser.add_argument('-s', '--hillsphere',  action= 'store_true',
                    help="traces 0.3*R_H and R_H levels")
parser.add_argument('-sl','--streamlines', action= 'store_true',
                    help="add streamlines (NOT IMPLEMENTED YET)")
# keywords arguments -------------------------------------------------
parser.add_argument('-bg','--background',dest='bg_key',
                    help="define background field using keys (label, density, FLI ...)",
                    choices=['l','d','f'], default = 'd')
parser.add_argument('-c' ,'--crop',      dest='crop_limit', type=float,
                    help="zoom around the planet",
                    default = 1000)
parser.add_argument('-o' ,'--output',
                    help="define picture output file name",
                    default = "")

# conversion ---------------------------------------------------------
args = parser.parse_args()
if args.thetacrop :
    azim_crop_limit = args.crop_limit
else :
    azim_crop_limit = 1000

if args.bg_key == "f" :
    print "Sorry, FLI postprocessing is not implemented yet, come back later !"
    exit(-1)

# fetching of numerical configuration --------------------------------
OUTDIR  = parseString(args.config, 'OutputDir'       )
SPACING = parseString(args.config, 'RadialSpacing'   )
NRAD    = parseValue (args.config, 'nrad'            )
NSEC    = parseValue (args.config, 'nsec'            )
RMIN    = parseValue (args.config, 'rmin',      float)
RMAX    = parseValue (args.config, 'rmax',      float)
ninterm = parseValue (args.config, 'ninterm'         )
DT      = parseValue (args.config, 'DT',        float)

# minimal postprocessing ---------------------------------------------
DR      = (RMAX-RMIN)/NRAD
dtheta  = 2.*np.pi/NSEC

base_theta    = np.linspace(0.,2*np.pi,NSEC)
rotated_theta = np.linspace(-np.pi,np.pi,NSEC)

# get planetary info -------------------------------------------------
lastline = np.loadtxt(OUTDIR+"planet0.dat")[-1]
q_p = lastline[5]
x_p = lastline[1]
y_p = lastline[2]

r_p     = np.sqrt(x_p**2+y_p**2)
theta_p = 0.0#by definition


# define plotting objects (fig, ax), choosing aspect carefully to have 
# same scale in both directions 
# this will be easy to spot when we plot hill "sphere"
fig = plt.figure()
ax = fig.add_subplot(111,aspect='auto')

bg_field, bgfile = get2Dfield(args.bg_key,NRAD,NSEC,OUTDIR,args.NOUT)
bg_used_radii    = getrad(RMIN,RMAX,NRAD,DR,args.bg_key,SPACING)


# plot background *****************************************************
# define background field, vt, vr
# useful options should be density, label, FLI

Jmin,Jmax          = findRadialLimits(r_p,q_p,bg_used_radii,args.crop_limit)
bg_field           = rotate(bg_field,base_theta,theta_p)
bg_field_crop      = bg_field[Jmin:Jmax,:]
bg_used_radii_crop = bg_used_radii[Jmin:Jmax]

# These two lines need to be run after rotation...
i_p = 0
while base_theta[i_p] < theta_p :
    i_p += 1
j_p = 0
while bg_used_radii_crop[j_p] < r_p :
    j_p += 1

bg_used_theta = rotated_theta #alias

# finding limits of the plot
Imin,Imax = findAzimLimits(r_p,q_p,bg_used_theta,azim_crop_limit)


# PLOTTING ************************************************************
# background and associated colorbar ---------------------------------
im = ax.imshow(bg_field_crop,cmap='viridis',aspect="auto",
               interpolation='none')
cb = fig.colorbar(im)
cb.set_label(AxLabels[args.bg_key])

# ticks --------------------------------------------------------------
ax.set_xticks([0,NSEC/4,NSEC/2,3*NSEC/4,NSEC])
ax.set_xticklabels([r"$-\pi$",r"$-\pi/2$",r"$0$",r"$\pi/2$",r"$\pi$"])

ytickslab = ax.get_yticks()
new_ytickslab = []
u=0#todo simplify
for tick in ytickslab[1:-1] :
    new_ytickslab.append(r"${0}$".format(round(bg_used_radii_crop[int(tick)],2)))

ax.set_yticklabels(new_ytickslab)
ax.set_xlabel(r"$\theta$", size=20)
ax.set_ylabel(r"$r$",      size=20)

# set limits ---------------------------------------------------------
ax.set_xlim(Imin,Imax)
ax.set_ylim(0,Jmax-(Jmin+1))


# ADDITIONAL PLOTTING *************************************************
# draw hill sphere(s) (optional) -------------------------------------
if args.hillsphere :
    R_H = Hill_radius(r_p,q_p)
    thetas=np.linspace(0,2*np.pi,100)
    R_H_code = R_H/(r_p*dtheta)
    ax.plot( *circle(NSEC/2,j_p-1,R_H_code,thetas),     c='r', ls='--')
    ax.plot( *circle(NSEC/2,j_p-1,0.3*R_H_code,thetas), c='r', ls='-')


# draw stream lines --------------------------------------------------
# todo
if args.streamlines :
    print "Sorry, STREAMLINES are not implemented yet, come back later !"


# PRINTING OUTPUT *****************************************************

if args.output != ""  :
    fig.savefig(args.output)
else :
    plt.show()
