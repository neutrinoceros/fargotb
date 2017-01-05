import re               #regular expressions
import sys              #allow call to classic shell commands
import numpy as np      #sci computations and array classes

from dictionnaries import *

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
