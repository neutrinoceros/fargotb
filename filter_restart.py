#!/usr/bin/python
#-*-coding:utf-8-*-
# --------------------------
# Author : Clément Robert
# written april 2017
# --------------------------
# This program filters out all lines in orbitNNN.dat and planetNNN.dat files you may get after a
# long run, from where you want to restart, avoiding piling up useless data
#
# Arguments 
#    0   ) path to configuration file (usually *.par)
#    1   ) last output number you want to keep
#    [2] ) number of planets used. Default is one.

from lib_parsing import *

args = getScriptArgs()
try :
    config,n_restart,n_planets = args[0],int(args[1]),int(args[2])
except IndexError :
    config,n_restart = args[0],int(args[1])
    n_planets = 1
    print "Warning : if you don't use excactly 3 arguments, only one planet is considered."

DT        = parseValue (config, 'DT',        float)
t_restart = DT * n_restart 
plan_fmt = ['%d'] + ['%.18e']*10
orb_fmt  = ['%.14e']*6
for i in range(n_planets) :
   try :
        plan_data  = np.loadtxt("out/planet{0}.dat".format(i))
        orbit_data = np.loadtxt("out/orbit{0}.dat".format(i))
        print "data for planet %d loaded !" % (i)
        Icut = 0
        while plan_data[Icut,0] < n_restart :
            Icut += 1
        np.savetxt("out/planet{0}.dat".format(i),plan_data[0:Icut+1,], fmt=plan_fmt)

        Jcut = 0
        while orbit_data[Jcut,0] < t_restart :
            Jcut += 1
        np.savetxt("out/orbit{0}.dat".format(i),orbit_data[0:Jcut+1,], fmt=orb_fmt)
        
   except IOError :
       print i, "failed"
       pass
