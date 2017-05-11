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
R_H     = r_p*(q_p/3)**(1./3) # Hill Radius

# MAIN LOOP ***********************************************************

# crop plotting region, cut out fields (optional)  
# by default, the planet should be centered (this may be hard, especially near angular boundaries)
crop_limit = 5. #(as a multiple of R_H)

# optionnally, we could have the option of using cartesian coordinates


# define plotting objects (fig, ax), choosing aspect carefully to have 
# same scale in both directions 
# this will be easy to spot when we plot hill "sphere"
fig = plt.figure()
ax = fig.add_subplot(111,aspect='auto')

#plot background
# define background field, vt, vr
# useful options should be density, label, FLI
bg_key = "d"#tmp
bg_field, bgfile = get2Dfield(bg_key,NRAD,NSEC,OUTDIR,NOUT)
bg_used_radii    = getrad(RMIN,RMAX,NRAD,DR,bg_key,SPACING)
def flip(field) :
    "flip the array upside down to accomodate imshow()"
    nr,ns = field.shape
    ffield = np.zeros((nr,ns))
    for i in range(nr) :
        ffield[i] = field[nr-(i+1)]
    return ffield

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

bg_field = flip(bg_field)
bg_field,cesure = rotate(bg_field,base_theta,theta_p)
ax.imshow(bg_field,cmap='viridis',aspect="auto")

# draw hill sphere(s)


# draw stream lines (optional)


# print out or save figure (optional flag)
fig.savefig("coucou.png")
