from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.cm as cm

def gen_patchcollection(grid_x,grid_y,data) :
    dimX = len(grid_x)
    dimY = len(grid_y)
    patches = []
    for i in range(dimX) :
        for j in range(dimY) :
            xy = grid_x[i], grid_y[j]
            try :
                width  = grid_x[i+1] - grid_x[i]
            except IndexError :
                pass
            try :
                height = grid_y[j+1] - grid_y[j]
            except IndexError :
                pass
            rect = Rectangle(xy=xy, width=width, height=height,
                             #rasterized=True,#todo : check usage of this line
                             linewidth=0,
                             linestyle="None")
            patches.append(rect)
    patchcollection = PatchCollection(patches,linewidth=0,cmap=cm.viridis)
    data1d = data.reshape(-1)
    patchcollection.set_array(data1d)
    return patchcollection
