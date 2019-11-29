import sys
sys.path.insert(1, '/home/zade/athena/vis/python')  # Testing on laptop
from athena_read import vtk
import numpy as np

filename = '/home/zade/work/linwave/output/alfven_default/'
filename += 'LinWave.block0.out2.00000.vtk'
x, y, z, data = vtk(filename)
vel = data['vel']  # vel[z, y, x, component]?
vel[0, 0, 0, :]






test = vtk(filename)
# Arrays - test[0] = x, test[1] = y, test[2] = z
# Dict of numpy ndarrays - test[3] = data
len(x)
x

x[np.where(x < 1.01)]
y.shape
z.shape
data

dx = 0 if len(x) == 1 else x[1] - x[0]
dy = 0 if len(y) == 1 else y[1] - y[0]
dz = 0 if len(z) == 1 else z[1] - z[0]
Ls = [np.max(x)+dx, np.max(y)+dy, np.max(z)+dz]
Ns = [len(x), len(y), len(z)]

Ls
Ls[::-1]
