#!/usr/bin/python
#-*-coding:utf-8-*-
# --------------------------
# Author : Clément Robert
# written april 2017
# --------------------------


from lib_parsing import *

#args = getScriptArgs()
N = 20

for k,tag in TAGS.items() :
    try :
        with open("../inner_ref/out/gas{0}{1}.dat".format(tag,N),'r') as fi :
            inner_lines = fi.readlines()
        with open("../outer_ref/out/gas{0}{1}.dat".format(tag,N),'r') as fi :
            outer_lines = fi.readlines()
        lines = inner_lines + outer_lines
        with open("out/gas{0}{1}.dat".format(tag,N),'w') as fi :
            for l in lines :
                fi.write(l)
    except IOError :
        pass
