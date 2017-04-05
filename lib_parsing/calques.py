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


def getScaleHeightsWherePlanetsAre(planetcfgfile,h0,betas) :
    hs = scaleHeight(smas,h0,beta)
    return hs

# This is really what motivated this "calque" branch -----------------------------------

def findWKZ(rmed,rmin,rmax,aspectratio,beta,border) :
    #WKZ stands for "wave killing zone"
    #border should be 0 or 1 to denote "in" and "out" respectively

    if border == 0 : #int
        d1 = rmed[25]-rmed[0]
        d2 = 5.0*scaleHeight(rmin,aspectratio,beta)
        d3 = .15*(1.-rmin)#this "1" stands for the current semi-major axis of the closest planet, should be refined in the general case
        w  = max([d1,d2,d3])#width of the wave killing zone
        WKZrads = rmin, rmin+w

    else : #ext
        d1 = rmed[-1]-rmed[-25]
        d2 = 5.0*scaleHeight(rmax,aspectratio,beta)
        d3 = 0.
        w  = max([d1,d2,d3])
        WKZrads = rmax-w, rmax

    return WKZrads
