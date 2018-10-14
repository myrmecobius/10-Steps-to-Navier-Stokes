import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import sympy
from sympy.utilities.lambdify import lambdify
from sympy import init_printing
init_printing(use_latex=True)

#%% Set up SymPy LaTeX Initial conditions
x, nu, t = sympy.symbols('x nu t')
phi = (sympy.exp(-(x - 4 * t)**2 / (4 * nu * (t + 1))) +
       sympy.exp(-(x - 4 * t - 2 * sympy.pi)**2 / (4 * nu * (t + 1))))
phiprime = phi.diff(x)
u = -2 * nu * (phiprime / phi) + 4
ufunc = lambdify((t, x, nu), u)

#%% Define interval
#spacial setup
nx = 101 #number of pieces the interval is divided into, spacial resolution
dx = 2 * np.pi / (nx - 1) #size of one dx step

#time setup
nt = 500 #number of time steps to calculate

#other parameters
nu = 0.07 #the value of viscosity
dt = dx * nu #define dt

#%% Set up NumPy initial conditions:
x = np.linspace(0, 2 * np.pi, nx)
yn = np.empty(nx) #initialize a temporary array
t = 0

y = np.asarray([ufunc(t, x0, nu) for x0 in x]) #keep track of values at each discrete spacial step
yVals = [y.copy()] #initiate a storage array
#plt.plot(np.linspace(0, 2*np.pi, nx), y) #plot initial condition
y_analytical = np.asarray([ufunc(nt * dt, xi, nu) for xi in x]) #analytical solution
yVals_analytical = [y_analytical.copy()]
#plt.plot(x, y_analytical) #plot analytical solution

#plt.figure(figsize=(11, 7), dpi=100)
#plt.plot(x,y, marker='o', lw=2, label='Computational')
#plt.plot(x, y_analytical, label='Analytical')
#plt.xlim([0, 2 * np.pi])
#plt.ylim([0, 8])
#plt.legend();

#%% Progress time steps 
for n in range(nt):  #loop over nt time steps
    yn = y.copy() ##copy the existing values of u into un
    for i in range(1, nx-1):
        y[i] = yn[i] - yn[i] * dt / dx *(yn[i] - yn[i-1]) + nu * dt / dx**2 *\
                (yn[i+1] - 2 * yn[i] + yn[i-1])
    y[0] = yn[0] - yn[0] * dt / dx * (yn[0] - yn[-2]) + nu * dt / dx**2 *\
                (yn[1] - 2 * yn[0] + yn[-2])
    y[-1] = y[0]
    
    y_analytical = np.asarray([ufunc(n * dt, xi, nu) for xi in x]) #analytical solution
    
    yVals_analytical.append(y_analytical.copy())
    yVals.append(y.copy())

#plt.plot(np.linspace(0, 2, nx), y) #plot the final condition

#%% Animate the results
#set up animation parameters
fig = plt.figure()
ax = plt.axes(xlim=(0, 2*np.pi), ylim=(0, 8))
line1, = ax.plot([], [], lw=2, label = 'Computational')
line2, = ax.plot([], [], lw=2, label = 'Analytical')
plt.legend()

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2,

def animate(i):
    x = np.linspace(0, 2*np.pi, nx)
    y1 = yVals[i]
    y2 = yVals_analytical[i]
    line1.set_data(x, y1)
    line2.set_data(x, y2)
    return line1, line2,

anim = FuncAnimation(fig, animate, init_func=init,
                               frames=nt, interval=20, blit=True)
plt.show()


