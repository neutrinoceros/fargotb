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

#parse values of h0,alpha

ALPHA_VISC  = parseValue(...)
ASPECTRATIO = parseValue()
out_dir     = parse....

#get time and semi-major axis from orbit0.dat

orbit0data = np.readtxt(out_dir+"/orbit0.dat").T
time = orbit0data[0].T
sma  = orbit0data[2].T

# compute extra columns

def vr_theo(r,h0,alpha) :
    return -1.5 * alpha * h0**2 / np.sqrt(r)
 
vr   = vr_theo(sma,ASPECTRATIO,ALPHA_VISC)

dotsma = ... #choose you algorithm

#pack everything nicely together

