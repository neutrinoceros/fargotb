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
#    0) path to configuration file (usually called "template.par")
#    1) physical quantity (see qty dict for details)
#    2) output number 
#
# Options (as additional arguments)
#    'light') skip the radii column
#
# /!\ WARNING : The output file is written in the current directory

import numpy as np      #sci computations and array classes
import re               #regular expressions
import sys              #allow call to classic shell commands
import fileinput        #used to add headers to outputfiles


# DEFINITIONS
#----------------------------------------------------------------------

def getScriptArgs() :
    """returns a list containing all the arguments 
    given to the script in order"""
    args = [a for a in  sys.argv]
    args.reverse(); args.pop(); args.reverse();
    return args

def parseString(configfile, key) :
    """returns the string associated with $key"""
    with open(config,'r') as fi :
        rawcontent = fi.readlines()
        content = r''
        for c in rawcontent :
            content+=c

    exp   = key + r'\s*\S*'
    regex = re.compile(exp,re.IGNORECASE)
    m     = regex.search(content)
    param = m.group().split()[1]
    return param

def parseValue(config, key) :
    """returns the value associated with the word $key 
    in a specified $config file.
    The function is not case sensible regarding $key."""
    with open(config,'r') as fi :
        rawcontent = fi.readlines()
        content = r''
        for c in rawcontent :
            content+=c

    exp   = key + r'[ \t]*[0-9]+[.e]?[+-]?[0-9]*'
    regex = re.compile(exp,re.IGNORECASE)
    m     = regex.search(content)
    param = m.group().split()[1]
    if '.' in param or 'e' in param :
        value = float(param)
    else :
        value = int(param)
    return value

qtydict = {"d"  : "dens",
           "t"  : "temperature",
           "p"  : "Pressure",
           "vr" : "vrad",
           "vt" : "vtheta",
           "df" : "epsilon",
           "l"  : "label",
           "do" : "dustdens",
           "go" : "gasonlydens"
           }


# PARSING
#----------------------------------------------------------------------

args = getScriptArgs()
if len(args)<3 :
    print """mandatory arguments : 
    0) path to configuration file 
    1) {0}
    2) output number
    """.format('|'.join([str(k) for k in qtydict.keys]))
    sys.exit()

config,key,nout = args

qty       = qtydict[key]

outputdir = parseString(config, 'OutputDir')
exfile    = outputdir+"gas"+qty+str(nout)+".dat"

nrad    = parseValue(config,'nrad')
nsec    = parseValue(config,'nsec')
rmin    = parseValue(config,'rmin')
rmax    = parseValue(config,'rmax')
ninterm = parseValue(config,"ninterm")
DT      = parseValue(config,'DT')

print "2D -> 1D parsing in ",exfile," found :"
print "nrad=%d, nsec=%d, rmin=%e, rmax=%e" % (nrad, nsec, rmin, rmax)

dr       = (rmax-rmin)/nrad
dtheta   = 2.*np.pi/nsec  


# reshape the data
#----------------------------------------------------------------------

tab      = np.fromfile(exfile).reshape(nrad,nsec)
radii    = np.linspace(rmin,rmax,nrad)
#nb : there should be a coefficient applied here
integral = tab.sum(axis=1)/nsec
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if "light" in args :
    tabout = integral
else :
    tabout = np.column_stack((radii,integral))


# SAVING
#----------------------------------------------------------------------

outfilename = "%s%s_1d.dat" % (qty, nout)
print "saving to %s" % outfilename
np.savetxt(outfilename,tabout)

currenttime  = DT * int(nout) * ninterm
currentorbit = currenttime/(2.*np.pi)
header  = "#original 2d file name        %s\n" % exfile
header += "#time                         %e\n" % currenttime
header += "#orbit                        %s\n" % currentorbit

with open(outfilename,'r') as fi :
    content = fi.read()

with open(outfilename,'w') as fi :
    fi.write(header)
    fi.write(content)
