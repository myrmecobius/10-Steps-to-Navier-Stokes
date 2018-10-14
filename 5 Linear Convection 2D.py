from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import pyplot as plt
import time

#%% Define interval
Ix = [0,2] #interval bounds x
Iy = [0,2] #interval bounds y
Lx = Ix[1] - Ix[0] #interval length x
Ly = Iy[1] - Iy[0] #interval length y

#spacial setup
nx = 81 #number of pieces the interval is divided into, spacial resolution, x
ny = 81 #y
dx = Lx / (nx - 1) #size of one dx step
dy = Ly / (ny - 1) #dy

#time setup
nt = 200 #number of time steps to calculate
sigma = .2 #parameter
dt = sigma * dx  #length of one dt step, time resolution
c = 1

#%%
x = np.linspace(Ix[0], Ix[1], nx) #initialize spacial variable grid, x
y = np.linspace(Iy[0], Iy[1], ny) #y

z = np.ones((ny, nx)) #Initial condition in 2D
zn = np.ones((ny, nx))
z[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2
zVals = [z.copy()]

#fig1 = plt.figure(figsize=(11, 7), dpi=100) #define figure
#ax1 = fig1.gca(projection='3d') #set figure as 3D
X, Y = np.meshgrid(x, y) #define independent variables
#surf = ax1.plot_surface(X, Y, z[:], cmap=cm.viridis) #plot initial condition

#%%
for n in range(nt + 1): ##loop across number of time steps
    zn = z.copy()
    z[1:, 1:] = (zn[1:, 1:] - (c * dt / dx * (zn[1:, 1:] - zn[1:, :-1])) -
                              (c * dt / dy * (zn[1:, 1:] - zn[:-1, 1:])))
    z[0, :] = 1
    z[-1, :] = 1
    z[:, 0] = 1
    z[:, -1] = 1
    zVals.append(z.copy())

#%%
fig = plt.figure(figsize=(11, 7), dpi=100)
ax = fig.gca(projection='3d')
ax.set_zlim(0, 2)

wframe = None
tstart = time.time()
for i in range(nt):
    # If a line collection is already remove it before drawing.
    if wframe:
        ax.collections.remove(wframe)

    # Plot the new wireframe and pause briefly before continuing.
    Z = zVals[i]
    wframe = ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2)
    plt.pause(.001)
