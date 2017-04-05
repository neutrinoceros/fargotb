from parsingFunctions import *


# First part should be use to COMPUTE a minimal resolution ----------------------------

def hillRad(a,q) :
    #assumes low eccentricity
    return a*(q/3)**(1./3)


def getHillRadii(planetcfgfile) :
    #parse masses as q
    #...
    qs = ... 

    #parse original locations
    #...
    smas = ...

    #compute radii Rh
    HillRadii = hillRad(smas,qs)
    return HillRadii


def scaleHeight(r,h0,beta=0.) :
    return h0*r**(1.+beta)


def getScaleHeightsWherePlanetsAre(planetcfgfile) :
    

# This is really what motivated this "calque" branch -----------------------------------

def findWKZ(border) :
    #WKZ stands for "wave killing zone"
    #border should be 0 or 1 to denote "in" and "out" respectively

    PLANETS     = parseString(config, 'Planets'         )#wip, this is not right
    SPACING     = parseString(config, 'RadialSpacing'   )
    ASPECTRATIO = parseValue (config, 'AspectRatio'     )
    BETA        = parseValue (config, 'FlaringIndex'    )
    NRAD        = parseValue (config, 'nrad'            )
    NSEC        = parseValue (config, 'nsec'            )
    RMIN        = parseValue (config, 'rmin',      float)
    RMAX        = parseValue (config, 'rmax',      float)

    RMED = getrad(RMIN,RMAX,NRAD,DR,'d',SPACING)
    RINF = getrad(RMIN,RMAX,NRAD,DR,'vr',SPACING)

    if border == 0 : #int
        d1 = RMED[25]-RMED[0]
        d2 = 5.0*scaleHeight(RMIN,ASPECTRATIO,BETA)
        d3 = .15*(1.-Rinf)#this "1" stands for the current semi-major axis of the closest planet, should be refined in the general case
    else : #ext
        d1 = RMED[-1]-RMED[-25]
        d2 = 5.0*scaleHeight(RMAX,ASPECTRATIO,BETA)
        d3 = .15*(1.-Rinf)#this "1" stands for the current semi-major axis of the closest planet, should be refined in the general case

    return max([d1,d2,d3]) #width of the wave killing zone
