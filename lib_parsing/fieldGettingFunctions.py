from parsingFunctions import *

def getRinf(rmin,rmax,nrad,dr) :
    rinf = np.linspace(rmin,rmax-dr,nrad)
    return rinf


def getRmed(rmin,rmax,nrad,dr) :
    rinf = getRinf(rmin,rmax,nrad,dr)
    L = len(rinf)
    rmed = np.zeros(L)
    for i in range(L-1) :
        rmed[i]  = 2.*(rinf[i+1]**3  - rinf[i]**3)
        rmed[i] /= 3.*(rinf[i+1]**2  - rinf[i]**2)
    rmed[-1]  = 2.*((rinf[-1]+dr)**3 - rinf[-1]**3)
    rmed[-1] /= 3.*((rinf[-1]+dr)**2 - rinf[-1]**2)
    return rmed


def getrad(rmin,rmax,nrad,dr,key) :
    #the default radius is Rinf, because it is easier to compute
    if TAGS[key] in Centered :
        rad = getRmed(rmin,rmax,nrad,dr)
    else :
        rad = getRinf(rmin,rmax,nrad,dr)
    return rad


def get2Dfield(key,nrad,nsec,outdir,nout) :
    """read a 2D output data file"""
    qty     = TAGS[key]    
    exfile  = getexfile(outdir,qty,nout)
    try :
        field2D = np.fromfile(exfile).reshape(nrad,nsec)
    except IOError :
        print "IOError : {0} doesn't exist, aborting script".format(exfile)
        sys.exit(1)
    return field2D, exfile
