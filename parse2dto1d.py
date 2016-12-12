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

import numpy as np      #sci computations and array classes
import re               #regular expressions
import sys              #allow call to classic shell commands
import fileinput        #used to add headers to outputfiles


# Defintions **********************************************************

# lower-case keys correspond to existing .dat files. 
# This dictionnary provides the corresponding rootnames of those files
#
# upper-case keys do not correspond to existing .dat files but rather
# are computed using $RECIPES defined in the following

TAGS = {"d"  : "dens",
        "t"  : "temperature",
        "p"  : "Pressure",
        "vr" : "vrad",
        "vt" : "vtheta",
        "df" : "epsilon",
        "l"  : "label",
        "do" : "dustdens",
        "go" : "gasonlydens",
        #--------------------
        "PHI": "flow"
       }

Centered  = ["dens", "temperature", "Pressure",
             "espilon", "label", "dustdens", "gasonlydens",
             "vtheta"]

Staggered = ["vrad"]

# parsing functions ----------------
def getScriptArgs() :
    """get a list of the arguments given to the script in order"""
    args = [a for a in  sys.argv]
    args.reverse(); args.pop(); args.reverse();
    return args

def parseString(configfile, key) :
    """fetch a string associated with $key"""
    with open(configfile,'r') as fi :
        rawcontent = fi.readlines()
        content = r''
        for c in rawcontent :
            content+=c

    exp   = key + r'\s*\S*'
    regex = re.compile(exp,re.IGNORECASE)
    m     = regex.search(content)
    param = m.group().split()[1]
    return param

def parseValue(configfile, key, kind=int) :
    """
    fetch a numerical value associated with $key 
    /!\ This is not case sensible regarding $key.
    """
    with open(configfile,'r') as fi :
        rawcontent = fi.readlines()
        content = r''
        for c in rawcontent :
            content+=c

    exp   = key + r'[ \t]*[0-9]+[.e]?[+-]?[0-9]*'
    regex = re.compile(exp,re.IGNORECASE)
    m     = regex.search(content)
    param = m.group().split()[1]
    if '.' in param or 'e' in param or kind == float :
        value = float(param)
    else :
        value = int(param)
    return value

def getexfile(outdir,qty,nout) :
    """put together the exact path to the base data file"""
    exfile = outdir+"gas"+qty+str(nout)+".dat"
    return exfile

def get2Dfield(key,nrad,nsec,outdir,nout) :
    """read a 2D output data file"""
    qty     = TAGS[key]    
    exfile  = getexfile(outdir,qty,nout)
    field2D = np.fromfile(exfile).reshape(nrad,nsec)
    return field2D, exfile

# /!\ dev note : 
# all recipes must share their arguments

def getflow(nrad,nsec,rad,outdir,nout) :
    """compute the radial mass flow of the medium"""
    sigma,filesig = get2Dfield('d' ,nrad,nsec,outdir,nout)
    vrad,filevrad = get2Dfield('vr',nrad,nsec,outdir,nout)
    flow2D = 2*np.pi*vrad*sigma
    for i in range(flow2D.shape[0]) :
        flow2D[i] *= rad[i]
    files  = [filesig, filevrad]
    return flow2D, files

RECIPES = {"flow" : getflow}

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

def getrad(rmin,rmax,nrad,dr,key) :
    #the default radius is Rinf
    radii   = np.linspace(rmin,rmax-dr,nrad)
    if TAGS[key] in Centered :
        #we convert to Rmed if needed
        L = len(radii)
        radii_new = np.zeros(L)
        for i in range(L-1) :
            radii_new[i]  = 2.*(radii[i+1]**3 - radii[i]**3)
            radii_new[i] /= 3.*(radii[i+1]**2 - radii[i]**2)
        radii_new[-1]  = 2.*((radii[-1]+dr)**3 - radii[-1]**3)
        radii_new[-1] /= 3.*((radii[-1]+dr)**2 - radii[-1]**2)
        radii = radii_new
    return radii

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
