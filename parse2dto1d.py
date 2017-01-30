#!/usr/bin/python
#-*-coding:utf-8-*-
# --------------------------
# Author : Clément Robert
# written june 2016
# --------------------------
# This executable converts a 2d binary file from Fargo into a 
# plain ascii "1d" file containing 2 columns : 
# [radii, 1d integrated quantity]
#
# It is designed to be as easy as possible to embed into shell loops 
# 
# Arguments 
#    0                  ) path to configuration file (usually *.par)
#    1 to second-to-last) physical quantities, see TAGS for details 
#    last               ) output number 
#
# Options (as additional arguments)
#    'light') skip the radii column
#
# /!\ WARNING : The output file is written in the current directory

from lib_parsing import * # built-in module that comes with the toolbox

# Defintions **********************************************************

# PARSING *************************************************************

args = getScriptArgs()
if len(args)<3 or "-h" in args :
    print """USAGE :
    0) path to configuration file 
    1) {0}
    2) output number
    """.format('|'.join([str(k) for k in TAGS.keys]))
    sys.exit()
elif len(args)==3 :
    config,KEYS,NOUT = args
    KEYS = [KEYS]
else :
    NOUT   = args.pop()
    args.reverse()
    config = args.pop()
    KEYS   = args

OUTDIR  = parseString(config, 'OutputDir'       )
NRAD    = parseValue (config, 'nrad'            )
NSEC    = parseValue (config, 'nsec'            )
RMIN    = parseValue (config, 'rmin',      float)
RMAX    = parseValue (config, 'rmax',      float)
ninterm = parseValue (config, 'ninterm'         )
DT      = parseValue (config, 'DT',        float)

DR      = (RMAX-RMIN)/NRAD
dtheta  = 2.*np.pi/NSEC


# MAIN LOOP ***********************************************************

for key in KEYS :
    used_radii =  getrad(RMIN,RMAX,NRAD,DR,key)
    #either Rinf or Rmed is returned, according to $ke
    RMED = getrad(RMIN,RMAX,NRAD,DR,'d')
    RINF = getrad(RMIN,RMAX,NRAD,DR,'vr')

    field1D,EXFILE = get1Dfield(NRAD,NSEC,RMIN,RMAX,DR,OUTDIR,NOUT,RINF,RMED,key)

    if "light" in args :
        tabout = field1D
    else :
        tabout = np.column_stack((used_radii,field1D))

    saveoutput(tabout,key,NOUT,DT,ninterm,EXFILE)
