#!/usr/bin/python
#-*-coding:utf-8-*-

# --------------------------
# Author : Clément Robert
# written november 2016
# --------------------------
# This is a fake simulation program used to run tests on monitoring.sh
#
# WARNING : one has to "mkdir tmp" whereever this program is run beforehand

import numpy as np
import time

radius  = np.linspace(0,4*np.pi,1000)
inity   = np.sin(radius)
profile = np.column_stack((radius,inity))

dt = 1.
T  = 5.
I  = 0
while I < 100 :
    inity   = np.sin(radius+I*dt/T)
    profile = np.column_stack((radius,inity))
    np.savetxt("tmp/gasdens%i.dat" % I, profile)
    time.sleep(1)
    I+=1
    print "I = " , I
