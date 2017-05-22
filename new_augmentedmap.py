#!/usr/bin/python
#-*-coding:utf-8-*-
# --------------------------
# Author : Clément Robert
# written may 2017
# --------------------------

from lib_parsing import * # built-in module that comes with the toolbox
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.cm as cm


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
                    help="add quiver of velocity field")
parser.add_argument('--scaling', action= 'store_true',
                    help="use real (log?) scaling (much longer to compute image)")
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

usePhysicalUnits = args.scaling and SPACING.lower() == "logarithmic"

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
