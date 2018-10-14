from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

#%%
def plot2D(x, y, p):
    fig = plt.figure(figsize=(11, 7), dpi=100)
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(x, y)
    surf = ax.plot_surface(X, Y, p[:], rstride=1, cstride=1, cmap=cm.viridis, linewidth=0, antialiased=False)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 1)
    ax.view_init(30, 225)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')

#%% Define interval
Ix = [0,2] #interval bounds x
Iy = [0,1] #interval bounds y
Lx = Ix[1] - Ix[0] #interval length x
Ly = Iy[1] - Iy[0] #interval length y

#spacial setup
nx = 50 #number of pieces the interval is divided into, spacial resolution, x
ny = 50 #y
nt = 100
dx = (Ix[1] - Ix[0]) / (nx - 1)
dy = (Iy[1] - Iy[0]) / (ny - 1)

#other parameters
c = 1 #wavespeed, change as necessary

##initial conditions
p = np.zeros((ny, nx))  # create a XxY vector of 0's
pd = np.zeros((ny, nx))
b  = np.zeros((ny, nx))

##plotting aids
x = np.linspace(Ix[0], Ix[1], nx)
y = np.linspace(Iy[0], Iy[1], ny)

# Source
b[int(ny / 4), int(nx / 4)]  = 100
b[int(3 * ny / 4), int(3 * nx / 4)] = -100

#%%
for it in range(nt):

    pd = p.copy()

    p[1:-1,1:-1] = (((pd[1:-1, 2:] + pd[1:-1, :-2]) * dy**2 +
                    (pd[2:, 1:-1] + pd[:-2, 1:-1]) * dx**2 -
                    b[1:-1, 1:-1] * dx**2 * dy**2) / 
                    (2 * (dx**2 + dy**2)))

    p[0, :] = 0
    p[ny-1, :] = 0
    p[:, 0] = 0
    p[:, nx-1] = 0

#%% Call functions
plot2D(x,y,p)
