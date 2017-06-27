import numpy as np

def circle(x0,y0,r,theta) :
    return x0+r*np.cos(theta), y0+r*np.sin(theta)

def ellipse(x0,y0,ax_x,ax_y,theta) :
    return x0+ax_x*np.cos(theta), y0+ax_y*np.sin(theta)


def bilinear_interpolate(field, xgrid, ygrid, x, y):
    I = 0
    while xgrid[I] < x :
        I+=1
    x0 = xgrid[I-1]
    x1 = xgrid[I]
    J = 0
    while ygrid[J] < y :
        J+=1
    y0 = ygrid[J-1]
    y1 = ygrid[J]

    va = field[ J-1, I-1 ]
    vb = field[ J  , I-1 ]
    vc = field[ J-1, I   ]
    vd = field[ J  , I   ]

    wa = (x1-x) * (y1-y)
    wb = (x1-x) * (y-y0)
    wc = (x-x0) * (y1-y)
    wd = (x-x0) * (y-y0)
    return wa*va + wb*vb + wc*vc + wd*vd
