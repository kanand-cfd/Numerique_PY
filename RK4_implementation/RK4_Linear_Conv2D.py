# -*- coding: utf-8 -*-
"""
Created on Thu May 21 20:47:15 2020

@author: mechi
"""

# %% Import Packages
from mpl_toolkits.mplot3d import Axes3D    #New Library required for projected 3d plots
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# %% Plot specs
plot_args = {'rstride': 1, 'cstride': 1, 'cmap':
             cm.viridis, 'linewidth': 0.01, 'antialiased': True, 'color': 'k',
             'shade': True}

plt.style.use('_classic_test')
        
# %% Variable initialisation
nx = 81 #number of elements in x-direction
ny = 81 #number of elements in y-direction
nt = 500 #number of time steps
dt = 0.05 #time step
c = 1. #wave velocity in x and y direction
dx = 2./(nx-1) #meshsize in x-direction
dy = 2./(ny-1) #meshsize in y-direction

# %% Mesh and Variable Initialisation
x = np.linspace(0.,2.,nx)
y = np.linspace(0.,2.,ny)
X, Y = np.meshgrid(x,y) 

u = np.ones((ny,nx)) 
un = np.ones((ny,nx))

#assign initial conditions with a 
#"hat-function": u(.5<=x<=1 && .5<=y<=1 ) is 1
u[int(0.5/dy):int(1./dy+1.),int(0.5/dx):int(1./dx+1.)]= 2.

# %% Function to calculate u_(n+1)
def func(c, u, dx):
    f = np.zeros(u.shape)
    nx, ny = u.shape
    for j in range(1, nx):
        for i in range(1, ny):
            f[j,i] = - (c*dt/dx*(un[j,i] - un[j,i-1]))-(c*dt/dy*(un[j,i]-un[j-1,i]))
    return f

# %% RK4 implementation
def RK4(c, u, dt, dx):
    u1 = u.copy()
    
    K1 = func(c, u1, dx)
    
    u2 = u1 + 0.5*K1
    K2 = func(c, u2, dx)
    
    u3 = u1 + 0.5*K2
    K3 = func(c, u3, dx)
    
    u4 = u1 + 0.5*K3
    K4 = func(c, u4, dx)
    
    u_new = u + (dt / 6)*(K1 + 2*K2 + 2*K3 + K4)
    
    return u_new

# %% Implement the time loop
t = 0
    
for n in range(nt):
    t += n*dt
    un = u.copy()
    u[0,:] = 1.
    u[-1,:] = 1.
    u[:,0] = 1.
    u[:,-1] = 1.
    u = RK4(c, un, dt, dx)
    if (n % 50 == 0):
        fig = plt.figure(figsize=(12,10), dpi=400); ax = fig.gca(projection='3d')
        ax.plot_surface(X,Y,u[:]);
        surf = ax.plot_surface(X, Y, u[:], **plot_args)
        ax.set_xlabel('$x$')
        ax.set_xlim(0, 2)
        ax.set_ylabel('$y$')
        ax.set_ylim(0, 2)
        ax.set_zlabel('$u(x,y)$')
        ax.set_zlim(1, 2)
        ax.set_title('2D Linear Convection')
