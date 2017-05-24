#!/usr/bin/python
#-*-coding:utf-8-*-
# --------------------------
# Author : Clément Robert
# written may 2017
# --------------------------

from lib_parsing import * # built-in module that comes with the toolbox

# PARSING *************************************************************

parser = argparse.ArgumentParser()
# mandatories --------------------------------------------------------
parser.add_argument('config', help="path to configuration file .par")
parser.add_argument('NOUT', type=int, help="output number")
# switches -----------------------------------------------------------
parser.add_argument('-c', '--center',  action= 'store_true',
                    help="traces 0.3*R_H and R_H levels")
parser.add_argument('-tc','--thetazoom',   action= 'store_true',
                    help="crop the figure in the azimuthal direction")
parser.add_argument('-s', '--hillsphere',  action= 'store_true',
                    help="traces 0.3*R_H and R_H levels")
parser.add_argument('-sl','--streamlines', action= 'store_true',
                    help="add streamlines")
parser.add_argument('-q','--quiver', action= 'store_true',
                    help="add quiver of velocity field")
parser.add_argument('--scaling', action= 'store_true',
                    help="use real (log?) scaling (much longer to compute image)")
parser.add_argument('--debug', action= 'store_true',
                    help="print debug informations")
# keywords arguments -------------------------------------------------
parser.add_argument('-bg','--background',dest='bg_key',
                    help="define background field using keys (label, density, radial flow FLI ...)",
                    choices=['l','d','rf','f','blank'], default = 'd')
parser.add_argument('-z' ,'--zoom', type=float,
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
if args.thetazoom :
    azim_zoom = args.zoom
    orientationcm = 'vertical'
else :
    azim_zoom = 1000
    orientationcm = 'horizontal'

if azim_zoom < 1000 :
    args.center = True

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

#usePhysicalUnits = args.scaling and SPACING.lower() == "logarithmic"
usePhysicalUnits = True #hardcoding

# minimal postprocessing ---------------------------------------------
DR      = (RMAX-RMIN)/NRAD
dtheta  = 2.*np.pi/NSEC

base_theta    = np.linspace(0.,2*np.pi,NSEC)
rotated_theta = np.linspace(-np.pi,np.pi,NSEC)

# get planetary info -------------------------------------------------
planet_dat  = np.loadtxt(OUTDIR+"planet0.dat")
line_number = 0
i = 0
while line_number < args.NOUT :
    line = planet_dat[i]
    line_number = line[0]
    i += 1

q_p = line[5]
x_p = line[1]
y_p = line[2]

r_p     = np.sqrt(x_p**2+y_p**2)
theta_p = atan2(x_p,y_p)

R_H     = Hill_radius(r_p,q_p)

# define plotting objects (fig, ax),
# todo : choose aspect carefully to have same scale in both directions
# errors are easy to spot when we plot Hill "spheres"
fig = plt.figure()
ax = fig.add_subplot(111,aspect='auto')


# plot background *****************************************************
# define background field, vt, vr

if args.bg_key in TAGS.keys() :
    bg_field,     bgfile = get2Dfield(args.bg_key,NRAD,NSEC,OUTDIR,args.NOUT)
    bg_used_radii        = getrad(RMIN,RMAX,NRAD,DR,args.bg_key,SPACING)
else :#blank case
    bg_field,     bgfile = get2Dfield('d',NRAD,NSEC,OUTDIR,args.NOUT)
    bg_used_radii        = getrad(RMIN,RMAX,NRAD,DR,'d',SPACING)

vrad_field,   vrfile = get2Dfield('vr',NRAD,NSEC,OUTDIR,args.NOUT)
vtheta_field, vtfile = get2Dfield('vt',NRAD,NSEC,OUTDIR,args.NOUT)

# get rid of the keplerian component as
# Streamlines and velocity field are only
# interesting in the Co-orbital frame
if Frame.upper() == "FIXED" :
    vtheta_field -= OmegaFrame(r_p,q_p)

used_theta = base_theta -np.pi
ang_width = np.pi

if args.center :
    # shifting to center the planet
    bg_field,corr           = shift(bg_field,     used_theta,theta_p)
    vrad_field,corr         = shift(vrad_field,   used_theta,theta_p)
    vtheta_field,corr       = shift(vtheta_field, used_theta,theta_p)
    used_theta -= corr

if args.zoom < 1000. :
    Jmin,Jmax = findRadialLimits(r_p,bg_used_radii,args.zoom*R_H)
    bg_field      = bg_field     [Jmin:Jmax,:]
    vrad_field    = vrad_field   [Jmin:Jmax,:]
    vtheta_field  = vtheta_field [Jmin:Jmax,:]
    bg_used_radii = bg_used_radii[Jmin:Jmax  ]

    RMIN_ = r_p - args.zoom * R_H
    RMAX_ = r_p + args.zoom * R_H

    if args.thetazoom :
        Imin,Imax = findAzimuthalLimits(r_p,used_theta,args.zoom*R_H)
        bg_field      = bg_field     [:,Imin:Imax]
        vrad_field    = vrad_field   [:,Imin:Imax]
        vtheta_field  = vtheta_field [:,Imin:Imax]
        used_theta    = used_theta   [Imin:Imax  ]
        ang_width = args.zoom * R_H/r_p
else :
    RMIN_ = RMIN
    RMAX_ = RMAX

TMIN_ = -ang_width
TMAX_ = TMIN_+2*ang_width

# PLOTTING ************************************************************
# background and associated colorbar ---------------------------------
if args.bg_key in TAGS.keys() :
    im = ax.add_collection(gen_patchcollection(used_theta,bg_used_radii,bg_field.T,args.bg_key))
    cb = fig.colorbar(im,orientation=orientationcm)
    cb.set_label(AxLabels[args.bg_key],size=20, rotation=0)

ax.set_aspect('equal')
ax.set_xlabel(r"$\theta$", size=20)
ax.set_ylabel(r"$r$",      size=20)

ax.set_ylim(RMIN_,RMAX_)
ax.set_xlim(TMIN_,TMAX_)


# OPTIONAL PLOTTING ***************************************************
thetas=np.linspace(0,2*np.pi,100)
XCENTER = (theta_p -np.pi)%np.pi
if args.center :
    XCENTER = 0.0

# draw hill sphere(s) ------------------------------------------------
if args.hillsphere :
    ycenter   = r_p
    lc = SPOTOUTCOLORS[args.bg_key]
    ax.plot( *circle(XCENTER,ycenter,R_H,thetas),     c=lc, ls='--')
    ax.plot( *circle(XCENTER,ycenter,0.3*R_H,thetas), c=lc, ls='-')

# draw stream lines --------------------------------------------------
if args.streamlines :
    pass
# draw velocity field ------------------------------------------------
if args.quiver :
    #note : "DR is not a constant in log radialspacing, but it's a good enough approximation
    #here, as we represent v_t and v_r from a same point even though they are not technically
    #defined at the same locations.
    ax.quiver(used_theta+dtheta/2, bg_used_radii+DR/2, vtheta_field, vrad_field,
              color='k',
              alpha = 0.4)

# PRINTING OUTPUT *****************************************************
if args.output != ""  :
    fig.savefig(args.output,dpi=300)
else :
    print "This is the interactive live mode. Use -o or --output to save your picture"
    plt.ion()
    plt.show()
    plt.ioff()
    raw_input("press enter to quit     ")
