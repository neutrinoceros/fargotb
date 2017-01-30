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
