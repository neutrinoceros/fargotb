#!/usr/bin/python
#-*-coding:utf-8-*-
# --------------------------
# Author : Clément Robert
# written april 2017
# --------------------------

import numpy as np
from lib_parsing import *

args = getScriptArgs()

#unpack args
print args[0]

config = args[0]
#parse values of h0,alpha

ALPHA_VISC  = parseValue(config, 'ALPHAVISCOsity',   float)
ASPECTRATIO = parseValue(config, 'ASPECTRATIO', float)
out_dir     = parseString(config, 'OutputDir')

#get time and semi-major axis from orbit0.dat

orbit0data = np.loadtxt(out_dir+"/orbit0.dat").T
time = orbit0data[0]
sma  = orbit0data[2]

# compute extra columns

def vr_theo(r,h0,alpha) :
    return -1.5 * alpha * h0**2 / np.sqrt(r)
 
vrth  = vr_theo(sma,ASPECTRATIO,ALPHA_VISC)

#dotsma = ... #choose you algorithm
smadot = np.zeros(len(sma))
#pack everything nicely together
array = np.column_stack([time,sma,smadot,vrth])
np.savetxt("typeII.dat",array,fmt="%.14e %.14e %.14e %.14e")
