import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

#%% Define interval
I = [0,2] #interval bounds
L = I[1] - I[0] #interval length

#spacial setup
nx = 41 #number of pieces the interval is divided into, spacial resolution
dx = L / (nx - 1) #size of one dx step

#time setup
nt = 200 #number of time steps to calculate
dt = 0.01 #length of one dt step, time resolution

#other parameters
c = 1 #wavespeed, change as necessary

#%% Set up initial conditions:
#y = 2 on [0.5,1], 1 elsewhere on [0,2], else 0
yl = np.ones(nx) #keep track of values at each discrete spacial step
yl[int(.5 / dx):int(1 / dx + 1)] = 2 #set points between 0.5 and 1 to two

yn = np.ones(nx) #keep track of values at each discrete spacial step
yn[int(.5 / dx):int(1 / dx + 1)] = 2 #set points between 0.5 and 1 to two

#plt.plot(np.linspace(0, 2, nx), y) #plot the initial condition

linVals = [yl.copy()] #initiate a storage array
nonLinVals = [yn.copy()] #initiate a storage array

ynl = np.ones(nx) #initialize a temporary array
ynn = np.ones(nx) #initialize a temporary array

#%% Progress time steps 
for n in range(nt):  #loop over nt time steps
    ynl = yl.copy() ##copy the existing values of u into un
    ynn = yn.copy() ##copy the existing values of u into un
    for i in range(1, nx): ## you can try commenting this line and...
        yl[i] = ynl[i] - c * dt / dx * (ynl[i] - ynl[i-1])
        yn[i] = yn[i] - ynn[i] * dt / dx * (ynn[i] - ynn[i-1])
    linVals.append(yl.copy())
    nonLinVals.append(yn.copy())

#plt.plot(np.linspace(0, 2, nx), y) #plot the final condition

#%% Animate the results
#set up animation parameters
fig = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(0, 2))
line1, = ax.plot([], [], lw=2, label = 'Linear')
line2, = ax.plot([], [], lw=2, label = 'Nonlinear')
plt.legend()

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2,

def animate(i):
    x = np.linspace(0, 2, nx)
    y1 = linVals[i]
    y2 = nonLinVals[i]
    line1.set_data(x, y1)
    line2.set_data(x, y2)
    return line1, line2,

anim = FuncAnimation(fig, animate, init_func=init,
                               frames=nt, interval=20, blit=True)
plt.show()


