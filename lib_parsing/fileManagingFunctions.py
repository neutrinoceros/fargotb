from numpy import pi as NP_PI, savetxt
import fileinput          # used to add headers to outputfiles
from dictionnaries import *


def saveoutput(tab,k,nout,dt,nint,exfile) :
    """saving routine"""
    outfilename = "%s%s_1d.dat" % (TAGS[k], nout)
    print "saving to %s" % outfilename
    savetxt(outfilename,tab)

    currenttime  = dt * int(nout) * nint
    currentorbit = currenttime/(2.*NP_PI)
    header  = "#original 2d file name        %s\n" % exfile
    header += "#time                         %e\n" % currenttime
    header += "#orbit                        %s\n" % currentorbit

    with open(outfilename,'r') as fi :
        content = fi.read()

    with open(outfilename,'w') as fi :
        fi.write(header)
        fi.write(content)


