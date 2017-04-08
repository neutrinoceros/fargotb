#!/usr/bin/python
#-*-coding:utf-8-*-
# --------------------------
# Author : Clément Robert
# written april 2017
# --------------------------


from lib_parsing import *

args = getScriptArgs()
if len(args) != 3 :
    print "error : wrong number of arguments"
    exit

N = int(args[0])
innerdisk_path = args[1]
outerdisk_path = args[2]

for k,tag in TAGS.items() :
    try :
        with open("{0}/gas{1}{2}.dat".format(innerdisk_path,tag,N),'r') as fi :
            inner_lines = fi.readlines()
        with open("{0}/gas{1}{2}.dat".format(outerdisk_path,tag,N),'r') as fi :
            outer_lines = fi.readlines()
        lines = inner_lines + outer_lines
        with open("out/gas{0}{1}.dat".format(tag,N),'w') as fi :
            for l in lines :
                fi.write(l)
    except IOError :
        pass
