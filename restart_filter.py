#!/usr/bin/python
#-*-coding:utf-8-*-

from lib_parsing import *


args = getScriptArgs()
try :
    n_restart,n_planets = int(args[0]),int(args[1])
except IndexError :
    n_restart = int(args[0])
    print "Warning : if you don't use excactly 2 arguments, only the first one is used."


plan_fmt = ['%d'] + ['%.18e']*10
for i in range(10) :
   try :
        plan_data  = np.loadtxt("out/planet{0}.dat".format(i))
        orbit_data = np.loadtxt("out/orbit{0}.dat".format(i))
        print "data for planet %d loaded !" % (i)
        Icut = 0
        while plan_data[Icut,0] < n_restart :
            Icut += 1
        np.savetxt("out/planet{0}.dat".format(i),plan_data[0:Icut+1,], fmt=plan_fmt)

   except IOError :
       print i, "failed"
       pass
