from fieldGettingFunctions import *
from recipes import *


def get1Dfield(nrad,nsec,rmin,rmax,dr,outdir,nout,Rinf,Rmed,key) :
    """This is the main macro. Self-explanatory enough ;-)"""
    if   key.islower() :
        field2D, exfile = get2Dfield(key,nrad,nsec,outdir,nout)
    elif key.isupper() :
        recipe = RECIPES[TAGS[key]]
        field2D, exfile = recipe(nrad,nsec,rmin,rmax,dr,outdir,nout,Rinf,Rmed)
    else :
        err = "key has to provided in pure-lower *or* pure-upper case"
        raise Keyerror(err)
    integral = field2D.sum(axis=1)/nsec
    return integral, exfile
