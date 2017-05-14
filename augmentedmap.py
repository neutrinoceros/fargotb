#!/usr/bin/python
#-*-coding:utf-8-*-
# --------------------------
# Author : Clément Robert
# written may 2017
# --------------------------

from lib_parsing import * # built-in module that comes with the toolbox

#enhancements 
#     * we could add the option of using cartesian coordinates
#     * logscaling is not taken into account yet
#     * yticks could be better

# Defintions **********************************************************

def Hill_radius(r_p,q_p) :
    return r_p*(q_p/3)**(1./3)

def OmegaFrame(r_p,q_p) :
    return np.sqrt((1.+q_p)/r_p**3)#todo : check

def findRadialLimits(r_p,q_p,rads,croper=5.) :
    R_H = Hill_radius(r_p,q_p)
    nr = len(rads)
    jmin,jmax = 0,nr
    while rads[jmin] < r_p-croper*R_H :
        jmin +=1
    while rads[jmax-2] > r_p+croper*R_H :#todo : check -2 ???
        jmax -=1
    return jmin,jmax

def findAzimLimits(r_p,q_p,thetas,croper=5.) :
    R_H = Hill_radius(r_p,q_p)
    ns = len(thetas)
    imin,imax = 0,ns
    while r_p*thetas[imin] < -croper*R_H :
        imin +=1
    while r_p*thetas[imax-2] > croper*R_H :#todo : check -2 ???
        imax -=1
    return imin,imax

def crop_field(field,jmin,jmax) :
    #devnote : we may be able to crop in i as well here
    cfield = field[jmin:jmax,:]
    return cfield

def shift(field,thetas,theta_p) :
    """this routine shifts the array along the theta axis
    to make the planet appear in the middle of the plot"""
    ns = len(thetas)
    i_p = 0
    while thetas[i_p] < theta_p :
        i_p += 1

    cesure  = ns/2 - i_p
    rfield1 = np.concatenate((field[:,-cesure:ns-1],field[:,0:i_p+1]),axis=1)
    rfield2 = field[:,i_p:-cesure]
    rfield  = np.concatenate((rfield1,rfield2),axis=1)
    return rfield

def circle(x0,y0,r,theta) :
    return x0+r*np.cos(theta), y0+r*np.sin(theta)

def get_pilabel_from_fraction(f) :
    num   = f.numerator
    den   = f.denominator
    if num == 0 :
        label = r"$0$"
    else :
        if num == 1 :
            num = ''
        elif num == -1 :
            num = '-'
        if den == 1 :
            label = r"${0}\pi$".format(num)
        else :
            label = r"${0}\pi/{1}$".format(num,den)
    return label

# PARSING *************************************************************

parser = argparse.ArgumentParser()
# mandatories --------------------------------------------------------
parser.add_argument('config', help="path to configuration file .par")
parser.add_argument('NOUT', type=int, help="output number")
# switches -----------------------------------------------------------
parser.add_argument('-c', '--center',  action= 'store_true',
                    help="traces 0.3*R_H and R_H levels")
parser.add_argument('-tc','--thetacrop',   action= 'store_true',
                    help="crop the figure in the azimuthal direction")
parser.add_argument('-s', '--hillsphere',  action= 'store_true',
                    help="traces 0.3*R_H and R_H levels")
parser.add_argument('-sl','--streamlines', action= 'store_true',
                    help="add streamlines")
parser.add_argument('-q','--quiver', action= 'store_true',
                    help="add quiver of velocity field (NOT IMPLEMENTED YET)")
parser.add_argument('--debug', action= 'store_true',
                    help="print debug informations")
# keywords arguments -------------------------------------------------
parser.add_argument('-bg','--background',dest='bg_key',
                    help="define background field using keys (label, density, radial flow FLI ...)",
                    choices=['l','d','rf','f','blank'], default = 'd')
parser.add_argument('-z' ,'--zoom',      dest='crop_limit', type=float,
                    help="zoom around the planet",
                    default = 1000)
parser.add_argument('-o' ,'--output',
                    help="define picture output file name",
                    default = "")
parser.add_argument('-d','--streamlines-density',dest='sldensity', type=int,
                    help="streamlines density",
                    default = 5)

# conversion ---------------------------------------------------------
args = parser.parse_args()
if args.thetacrop :
    azim_crop_limit = args.crop_limit
else :
    azim_crop_limit = 1000

if args.bg_key == 'rf' :
    #here, put verif of the existence of the postprocessed file
    pass

elif args.bg_key == 'f' :
    print "Sorry, FLI postprocessing is not implemented yet, come back later !"
    exit(-1)

elif args.bg_key == 'blank' :
    pass

# fetching of numerical configuration --------------------------------
OUTDIR  = parseString(args.config, 'OutputDir'       )
SPACING = parseString(args.config, 'RadialSpacing'   )
Frame   = parseString(args.config, 'Frame'           )
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


# define plotting objects (fig, ax),
# todo : choose aspect carefully to have same scale in both directions
# errors are easy to spot when we plot Hill "spheres"
fig = plt.figure()
ax = fig.add_subplot(111,aspect='auto')


# plot background *****************************************************
# define background field, vt, vr

try :
    bg_field,     bgfile = get2Dfield(args.bg_key,NRAD,NSEC,OUTDIR,args.NOUT)
    bg_used_radii        = getrad(RMIN,RMAX,NRAD,DR,args.bg_key,SPACING)
except KeyError :#thats how we handle the blank case
    bg_field,     bgfile = get2Dfield('d',NRAD,NSEC,OUTDIR,args.NOUT)
    bg_used_radii        = getrad(RMIN,RMAX,NRAD,DR,'d',SPACING)

vrad_field,   vrfile = get2Dfield('vr',NRAD,NSEC,OUTDIR,args.NOUT)
vtheta_field, vtfile = get2Dfield('vt',NRAD,NSEC,OUTDIR,args.NOUT)


# shifting to center the planet
if args.center :
    bg_field           = shift(bg_field,     base_theta,theta_p)
    vrad_field         = shift(vrad_field,   base_theta,theta_p)
    vtheta_field       = shift(vtheta_field, base_theta,theta_p)

# radial cropping
Jmin,Jmax = findRadialLimits(r_p,q_p,bg_used_radii,args.crop_limit)
bg_field_crop      = bg_field     [Jmin:Jmax,:]
vrad_field_crop    = vrad_field   [Jmin:Jmax,:]
vtheta_field_crop  = vtheta_field [Jmin:Jmax,:]
bg_used_radii_crop = bg_used_radii[Jmin:Jmax  ]


# get rid of the keplerian component as
# Streamlines and velocity field are only
# interesting in the Co-orbital frame
if Frame.upper() == "FIXED" :
    vtheta_field_crop -= OmegaFrame(r_p,q_p)


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
sector_range       = Imax-Imin
angular_range      = sector_range *2*np.pi/NSEC
angular_range_frac = angular_range/(2.0*np.pi)

# azimuthal cropping
Jmin,Jmax = findRadialLimits(r_p,q_p,bg_used_radii,args.crop_limit)
bg_field_crop      = bg_field_crop     [:,Imin:Imax]
vrad_field_crop    = vrad_field_crop   [:,Imin:Imax]
vtheta_field_crop  = vtheta_field_crop [:,Imin:Imax]

# PLOTTING ************************************************************
# background and associated colorbar ---------------------------------
if args.bg_key != 'blank' :
    try :
        im = ax.imshow(bg_field_crop,
                       cmap=CMAPS[args.bg_key],
                       aspect="auto",
                       interpolation='none')
    except ValueError :
        print "Warning : color map not available, using default gnuplot style."
        im = ax.imshow(bg_field_crop,
                       cmap='gnuplot',
                       aspect="auto",
                       interpolation='none')

    cb = fig.colorbar(im,orientation='vertical')
    cb.set_label(AxLabels[args.bg_key],size=20, rotation=0)

# set limits ---------------------------------------------------------
ax.set_ylim(0,Jmax-(Jmin+1))
ax.set_xlim(0,sector_range-1)

# ticks --------------------------------------------------------------

if args.debug :
    print "In --debug mode, orignial ticks are left on the x/y axis"
else :
    maxdiv = NSEC
    while frac(1,maxdiv) < angular_range_frac :
        maxdiv -=1
    if args.thetacrop and args.crop_limit < 1000 :#fix
        maxdiv+=1
    div = maxdiv*4
    fracticks  = [frac(2*n,div) for n in range(-2,3)]
    thetaticks = [np.pi*f for f in fracticks]

    xticks = [(t/np.pi+1.0)*NSEC/2 - Imin for t in thetaticks]

    xtickslab = [r"${0}\pi/{1}$".format(f.numerator,f.denominator) for f in fracticks]
    xtickslab = [get_pilabel_from_fraction(f) for f in fracticks]#devnote : may be simplified
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtickslab)

    ytickslab = ax.get_yticks()
    ytickslab = [r"${0}$".format(round(bg_used_radii_crop[int(tick)],2))
                 for tick in ytickslab[:-1]]

    ax.set_yticklabels(ytickslab)

ax.set_xlabel(r"$\theta$", size=20)
ax.set_ylabel(r"$r$",      size=20)



# OPTIONAL PLOTTING ***************************************************
xxx = np.arange(sector_range)
yyy = np.arange(0,Jmax-Jmin)
R_H = Hill_radius(r_p,q_p)
R_H_code = R_H/(r_p*dtheta)
thetas=np.linspace(0,2*np.pi,100)

# draw hill sphere(s) ------------------------------------------------
if args.hillsphere :
    lc = SPOTOUTCOLORS[args.bg_key]
    ax.plot( *circle(sector_range/2,j_p-1,R_H_code,thetas),     c=lc, ls='--')
    ax.plot( *circle(sector_range/2,j_p-1,0.3*R_H_code,thetas), c=lc, ls='-')

# draw stream lines --------------------------------------------------
if args.streamlines :
    if args.bg_key == 'blank' :
        slcolor = 'b'
    else :
        slcolor = 'w'

    ax.streamplot(xxx, yyy, vtheta_field_crop, vrad_field_crop,
                  density=(args.sldensity,args.sldensity),
                  color=slcolor,
                  arrowsize=0.7,
                  linewidth=0.15)

# draw velocity field ------------------------------------------------
if args.quiver :
    ax.quiver(xxx, yyy, vtheta_field_crop, vrad_field_crop,
              color='k',
              alpha = 0.4)

# PRINTING OUTPUT *****************************************************

if args.output != ""  :
    fig.savefig(args.output)
else :
    print "This is the interactive live mode. Use -o or --output to save your picture"
    plt.ion()
    plt.show()
    plt.ioff()
    raw_input("press enter to quit     ")
