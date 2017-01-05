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

import fileinput          # used to add headers to outputfiles
from lib_parsing import * # built-in module that comes with the toolbox

# Defintions **********************************************************

# main routine ---------------------
def get1Dfield(key,nrad,nsec,rad,outdir,nout) :
    """self-explanatory enough ;-)"""
    if   key.islower() :
        field2D, exfile  = get2Dfield(key,nrad,nsec,outdir,nout)
    elif key.isupper() :
        recipe = RECIPES[TAGS[key]]
        field2D, exfile  = recipe(nrad,nsec,rad,outdir,nout)
    else :
        err = "key has to provided in pure-lower *or* pure-upper case"
        raise Keyerror(err)
    integral = field2D.sum(axis=1)/nsec
    return integral, exfile

# file management ------------------
def saveoutput(tab,k,nout,dt,nint,exfile) :
    """saving routine"""
    outfilename = "%s%s_1d.dat" % (TAGS[k], nout)
    print "saving to %s" % outfilename
    np.savetxt(outfilename,tab)

    currenttime  = DT * int(nout) * nint
    currentorbit = currenttime/(2.*np.pi)
    header  = "#original 2d file name        %s\n" % exfile
    header += "#time                         %e\n" % currenttime
    header += "#orbit                        %s\n" % currentorbit

    with open(outfilename,'r') as fi :
        content = fi.read()

    with open(outfilename,'w') as fi :
        fi.write(header)
        fi.write(content)


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

# print "parsing 1D %s field..." % (key)

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
    radii =  getrad(RMIN,RMAX,NRAD,DR,key)

    field1D,EXFILE = get1Dfield(key,NRAD,NSEC,radii,OUTDIR,NOUT)

    if "light" in args :
        tabout = field1D
    else :
        tabout = np.column_stack((radii,field1D))

    saveoutput(tabout,key,NOUT,DT,ninterm,EXFILE)
