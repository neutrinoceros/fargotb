from parsingFunctions import *

def getRinf(rmin,rmax,nrad,dr,spacing) :
    "returns nr+1 points"
    if spacing.lower() == "logarithmic" :
        rinf = np.array([rmin * np.exp(i * np.log(rmax/rmin)/nrad) for i in range(nrad+1)])
    else : #default is "Arithmetic"
        rinf = np.linspace(rmin,rmax,nrad+1)
    return rinf


def getRmed(rmin,rmax,nrad,dr,spacing) :
    "returns nr points"
    rinf = getRinf(rmin,rmax,nrad,dr,spacing)
    rmed = np.zeros(nrad)
    for i in range(nrad) :
        rmed[i]  = 2.*(rinf[i+1]**3  - rinf[i]**3)
        rmed[i] /= 3.*(rinf[i+1]**2  - rinf[i]**2)
    return rmed


def getrad(rmin,rmax,nrad,dr,key,spacing) :
    #the default radius is Rinf, because it is easier to compute
    if TAGS[key] in Centered :
        rad = getRmed(rmin,rmax,nrad,dr,spacing)
    else :
        rad = getRinf(rmin,rmax,nrad,dr,spacing)
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
