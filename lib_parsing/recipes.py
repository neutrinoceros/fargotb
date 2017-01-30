from functions import *
# /!\ dev note : 
# all recipes must share their arguments

def getSigmaInf(nrad,nsec,rmin,rmax,dr,outdir,nout,Rinf,Rmed) :
    #dev note : this a prototype, we're missing declaration and testing
    sigmaMed,filesig = get2Dfield('d' ,nrad,nsec,outdir,nout)

    sigmaInf = sigmaMed.copy()
    for i in range(1, nrad) :
        for j in range(nsec) :
          sigmaInf[i,j] = (sigmaMed[i-1,j] * (Rmed[i] - Rinf[i]) + sigmaMed[i,j] * (Rinf[i] - Rmed[i-1])) / (Rmed[i] - Rmed[i-1])  
    return sigmaInf, filesig


def getflow(nrad,nsec,rmin,rmax,dr,outdir,nout,Rinf,Rmed) :
    """new method : define flow at Rinf by shifting density
    --extrapolation based on what is found is fargo--"""
    sigmaInf,filesig = getSigmaInf(nrad,nsec,rmin,rmax,dr,outdir,nout,Rinf,Rmed)

    sigma,filesig = get2Dfield('d' ,nrad,nsec,outdir,nout)
    vrad,filevrad = get2Dfield('vr',nrad,nsec,outdir,nout)
    used_files  = [filesig, filevrad]

    flow2D = 2*np.pi*vrad*sigmaInf
    for i in range(nrad) :
        flow2D[i] *= Rinf[i]


    return flow2D, used_files

# -----------------------------------------------------------
RECIPES = {"flow" : getflow}
