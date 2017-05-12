#!/usr/bin/python
#-*-coding:utf-8-*-
# --------------------------
# Author : Clément Robert
# written february 2017
# --------------------------


from lib_parsing import * # built-in module that comes with the toolbox
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# MODES = {'c' : pl.contour,
#          'q' : pl.quiver,
#          '3d': pl.plot_surface
#          }

# PARSING *************************************************************

args = getScriptArgs()

#config,NOUT,mode = args
config,NOUT = args

# if len(args)<3 or "-h" in args :
#     print """USAGE :
#     0) path to configuration file 
#     1) {0}
#     2) output number
#     """.format('|'.join([str(k) for k in MODES.keys]))
#     sys.exit()
# elif len(args)==2 :
#     config,NOUT = args
#     KEYS = [KEYS]
# else :
#     print "error : exception not handled yet"
#     exit

OUTDIR  = parseString(config, 'OutputDir'       )
SPACING = parseString(config, 'RadialSpacing'   )
NRAD    = parseValue (config, 'nrad'            )
NSEC    = parseValue (config, 'nsec'            )
RMIN    = parseValue (config, 'rmin',      float)
RMAX    = parseValue (config, 'rmax',      float)
ninterm = parseValue (config, 'ninterm'         )
DT      = parseValue (config, 'DT',        float)

DR      = (RMAX-RMIN)/NRAD
dtheta  = 2.*np.pi/NSEC


# MAIN LOOP ***********************************************************


RINF = getrad(RMIN,RMAX,NRAD,DR,'vr',SPACING)
RMED = getrad(RMIN,RMAX,NRAD,DR,'d',SPACING)

radrange,thetarange = np.meshgrid(RINF,np.linspace(0,2*np.pi,NSEC))

flow2d,EXFILE = getflow(NRAD,NSEC,RMIN,RMAX,DR,OUTDIR,NOUT,RINF,RMED)
#pl.MODES[mode](radrange.T,thetarange.T,flow2d)
cm=plt.cm.RdBu
plt.contourf(radrange.T,thetarange.T,flow2d,cmap=cm)

plt.colorbar()
plt.contour(radrange.T,thetarange.T,flow2d,levels=[0])
plt.savefig("2dflow{0}.png".format(NOUT))    
