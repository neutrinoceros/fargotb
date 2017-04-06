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
ninterm   = parseValue (config, 'ninterm'         )
t_restart = DT * n_restart * ninterm
plan_fmt = ['%d'] + ['%.18g']*10
orb_fmt  = ['%.14e']*6
for i in range(n_planets) :
   try :
        plan_file = "out/planet{0}.dat".format(i)
        lines = filter(lambda x:int(x.split('\t')[0])<=n_restart,open(plan_file,'r'))
        open(plan_file,'w').write("".join(lines))

        orb_file  = "out/orbit{0}.dat".format(i)
        lines = filter(lambda x:float(x.split('\t')[0])<=t_restart,open(orb_file,'r'))
        open(orb_file,'w').write("".join(lines))
        
   except IOError :
       print i, "failed"
       pass
