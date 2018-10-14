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
nt = 100 #number of time steps to calculate
dt = 0.01 #length of one dt step, time resolution

#other parameters
c = 1 #wavespeed, change as necessary

#%% Set up initial conditions:
#y = 2 on [0.5,1], 1 elsewhere on [0,2], else 0
y = np.ones(nx) #keep track of values at each discrete spacial step
y[int(.5 / dx):int(1 / dx + 1)] = 2 #set points between 0.5 and 1 to two

#plt.plot(np.linspace(0, 2, nx), y) #plot the initial condition

yVals = [y.copy()] #initiate a storage array
yn = np.ones(nx) #initialize a temporary array

#%% Progress time steps 
for n in range(nt):  #loop over nt time steps
    yn = y.copy() ##copy the existing values of u into un
    for i in range(1, nx): ## you can try commenting this line and...
        y[i] = yn[i] - c * dt / dx * (yn[i] - yn[i-1])
    yVals.append(y.copy())

#plt.plot(np.linspace(0, 2, nx), y) #plot the final condition

#%% Animate the results
#set up animation parameters
fig = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(0, 2))
line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    x = np.linspace(0, 2, nx)
    y = yVals[i]
    line.set_data(x, y)
    return line,

anim = FuncAnimation(fig, animate, init_func=init,
                               frames=nt, interval=20, blit=True)
plt.show()


