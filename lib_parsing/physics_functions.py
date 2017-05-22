import numpy as np

def Hill_radius(r_p,q_p) :
    return r_p*(q_p/3)**(1./3)

def OmegaFrame(r_p,q_p) :
    return np.sqrt((1.+q_p)/r_p**3)#todo : check

def atan2(x,y) :
    if x > 0. :
        return np.arctan(y/x)
    elif x < 0. :
        if y >= 0. :
            return np.arctan(y/x) + np.pi
        else :
            return np.arctan(y/x) - np.pi
    else : #(x == 0)
        if y > 0. :
            return +np.pi/2
        elif y < 0. :
            return -np.pi/2
        else : # (y == 0)
            print "error, atan2(0,0) is undefined"
            return -1000
