#!/usr/bin/python
#-*-coding:utf-8-*-
# --------------------------
# Author : Clément Robert
# written may 2017
# --------------------------

from lib_parsing import * # built-in module that comes with the toolbox
import matplotlib.pyplot as plt

# Defintions **********************************************************

# PARSING *************************************************************

#args = getScriptArgs()

config = ("/home/crobert/Bureau/sandboxPLOT2D/data/in/phase0.par") #tmp
NOUT = 20#tmp


OUTDIR  = parseString(config, 'OutputDir'       )
PlanetF = parseString(config, 'PlanetConfig'    )#to use
SPACING = parseString(config, 'RadialSpacing'   )
NRAD    = parseValue (config, 'nrad'            )
NSEC    = parseValue (config, 'nsec'            )
RMIN    = parseValue (config, 'rmin',      float)
RMAX    = parseValue (config, 'rmax',      float)
ninterm = parseValue (config, 'ninterm'         )
DT      = parseValue (config, 'DT',        float)

DR      = (RMAX-RMIN)/NRAD
dtheta  = 2.*np.pi/NSEC

base_theta = np.linspace(0.,2*np.pi,NSEC)


# get planetary info
r_p     = 1.#tmp
theta_p = 0#tmp
q_p     = 0.001#tmp


# MAIN LOOP ***********************************************************

# optionnally, we could have the option of using cartesian coordinates


# define plotting objects (fig, ax), choosing aspect carefully to have 
# same scale in both directions 
# this will be easy to spot when we plot hill "sphere"
fig = plt.figure()
ax = fig.add_subplot(211,aspect='auto')
ax2 = fig.add_subplot(212,aspect='auto')
#plot background
# define background field, vt, vr
# useful options should be density, label, FLI
bg_key = "d"#tmp
bg_field, bgfile = get2Dfield(bg_key,NRAD,NSEC,OUTDIR,NOUT)
bg_used_radii    = getrad(RMIN,RMAX,NRAD,DR,bg_key,SPACING)

def rotate(field,thetas,theta_p) :
    ns = len(thetas)
    j_p = 0
    while thetas[j_p] < theta_p :
        j_p += 1

    cesure  = ns/2 - j_p
    ffield1 = np.concatenate((field[:,-cesure:ns-1],field[:,0:j_p]),axis=1)
    ffield2 = field[:,j_p:-cesure]
    ffield  = np.concatenate((ffield1,ffield2),axis=1)
    return ffield,cesure

bg_field,cesure = rotate(bg_field,base_theta,theta_p)
ax.imshow(bg_field,cmap='viridis',aspect="auto")
ax.set_ylim(0,NRAD)

# crop plotting region, cut out fields (optional)  
# by default, the planet should be centered (this may be hard, especially near angular boundaries)
# dev note : croping should be done BEFORE plotting anything

crop_limit = 5.#tmp

def findRadialLimits(r_p,q_p,rads,croper=5.) :
    R_H = r_p*(q_p/3)**(1./3) # Hill Radius
    nr = len(rads)
    jmin,jmax = 0,nr-1
    while rads[jmin] < r_p-croper*R_H :
        jmin +=1
    while rads[jmax] > r_p+croper*R_H :
        jmax -=1
    return jmin,jmax

jmin,jmax = findRadialLimits(r_p,q_p,bg_used_radii,crop_limit)

ax2.imshow(bg_field,cmap='viridis',aspect="auto")
ax2.set_ylim(jmin,jmax)

# draw hill sphere(s)

# draw stream lines (optional)


# print out or save figure (optional flag)
fig.savefig("coucou.png")
