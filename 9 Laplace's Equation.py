from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

#%%
def plot2D(x, y, p, Ix, Iy):
    fig = plt.figure(figsize=(11, 7), dpi=100)
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(x, y)
    surf = ax.plot_surface(X, Y, p[:], rstride=1, cstride=1, cmap=cm.viridis, linewidth=0, antialiased=False)
    ax.set_xlim(Ix[0], Ix[1])
    ax.set_ylim(Iy[0], Iy[1])
    ax.view_init(30, 225)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    
#%%
def laplace2d(p, y, dx, dy, l1norm_target):
    l1norm = 1
    pn = np.empty_like(p)

    while l1norm > l1norm_target:
        pn = p.copy()
        p[1:-1, 1:-1] = ((dy**2 * (pn[1:-1, 2:] + pn[1:-1, 0:-2]) +
                         dx**2 * (pn[2:, 1:-1] + pn[0:-2, 1:-1])) /
                        (2 * (dx**2 + dy**2)))
            
        p[:, 0] = 0  # p = 0 @ x = 0
        p[:, -1] = y  # p = y @ x = 2
        p[0, :] = p[1, :]  # dp/dy = 0 @ y = 0
        p[-1, :] = p[-2, :]  # dp/dy = 0 @ y = 1
        l1norm = (np.sum(np.abs(p[:]) - np.abs(pn[:])) /
                np.sum(np.abs(pn[:])))
     
    return p

#%% Define interval
Ix = [0,2] #interval bounds x
Iy = [0,1] #interval bounds y
Lx = Ix[1] - Ix[0] #interval length x
Ly = Iy[1] - Iy[0] #interval length y

#spacial setup
nx = 31 #number of pieces the interval is divided into, spacial resolution, x
ny = 31 #y
dx = Lx / (nx - 1) #size of one dx step
dy = Ly / (ny - 1) #dy

#other parameters
c = 1 #wavespeed, change as necessary

##initial conditions
p = np.zeros((ny, nx))  # create a XxY vector of 0's

##plotting aids
x = np.linspace(Ix[0], Ix[1], nx)
y = np.linspace(Iy[0], Iy[1], ny)

##boundary conditions
p[:, 0] = 0  # p = 0 @ x = 0
p[:, -1] = y  # p = y @ x = 2
p[0, :] = p[1, :]  # dp/dy = 0 @ y = 0
p[-1, :] = p[-2, :]  # dp/dy = 0 @ y = 1

#%% Call functions
p = laplace2d(p, y, dx, dy, 1e-4)
plot2D(x,y,p, Ix, Iy)
