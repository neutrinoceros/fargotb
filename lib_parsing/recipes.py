from functions import *
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
