# -*- coding: utf-8 -*-
"""
Created on Sat May 23 23:35:52 2020

@author: mechi
"""

# %% Import packages
from __future__ import division
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# %% Plot and animation specs
plot_args = {'rstride': 1, 'cstride': 1, 'cmap':
             cm.viridis, 'linewidth': 0.01, 'antialiased': True, 'color': 'k',
             'shade': True}
 
Writer = animation.writers['ffmpeg']
writer = Writer(fps=12, metadata=dict(artist='KA'), bitrate=1800)    

plt.style.use('_classic_test')

# %% Parameter Declaration and Variable Initialization
nx = 41
ny = 41
nt = 120
dx = 2 / (nx - 1)
dy = 2 / (ny - 1)
sigma = 0.01
nu = 0.05
dt = sigma * dx * dy / nu

x = np.linspace(0, 2, nx)
y = np.linspace(0, 2, ny)
X, Y = np.meshgrid(x, y)

u = np.ones((ny, nx))
v = np.ones((ny, nx))
un = np.ones((ny, nx))
vn = np.ones((ny, nx))

# Assign initial condtions as hat function
u[int(0.5/dy):int(1/dy + 1), int(0.5/dx):int(1/dx + 1)] = 2.
v[int(0.5/dy):int(1/dy + 1), int(0.5/dx):int(1/dx + 1)] = 2.

# %% Function for updating the hat function along with animation frame
def data_gen(framenumber, u, v, plot):
    #change soln variable for the next frame
    un = u.copy()
    vn = v.copy()
    row, col = u.shape
    dx = 2./(row-1) #meshsize in x-direction
    dy = 2./(col-1) #meshsize in y-direction
    sigma = 0.01
    nu = 0.01
    dt = sigma * dx * dy / nu
    u[0,:] = 1
    u[-1,:] = 1
    u[:,0] = 1
    u[:,-1] = 1
    
    v[0,:] = 1
    v[-1,:] = 1
    v[:, 0] = 1
    v[:, -1] = 1
    
    u[1:-1, 1:-1] = un[1:-1, 1:-1] - (un[1:-1,1:-1] * (dt / dx) * (un[1:-1,1:-1] - un[1:-1,0:-2]))-\
        (vn[1:-1,1:-1] * (dt / dy) * (un[1:-1,1:-1] - un[0:-2, 1:-1])) +\
        nu * dt / dx**2 * (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] +\
        un[1:-1,0:-2]) + nu * dt / dy**2 * (un[2:,1:-1] - 2 * un[1:-1,1:-1] + un[0:-2,1:-1])
                   
    v[1:-1, 1:-1] = vn[1:-1, 1:-1] - (un[1:-1,1:-1] * (dt / dx) * (vn[1:-1,1:-1] - vn[1:-1,0:-2]))-\
        (vn[1:-1,1:-1] * (dt / dy) * (vn[1:-1, 1:-1] - vn[0:-2, 1:-1])) +\
        nu * dt / dx**2 * (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] +\
        un[1:-1,0:-2]) + nu * dt / dy**2 * (un[2:,1:-1] - 2 * un[1:-1,1:-1] + un[0:-2,1:-1])
    
    ax.clear()                      
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_zlabel('$u(x,y)$')
    ax.set_title(r'$\frac{\partial V}{\partial t} + V \cdot \nabla{V} = \nu {\nabla}^2 V$')
    plot = ax.plot_surface(X, Y, u[:], **plot_args)
    
    return plot

# %% Final plot and animation generation
fig = plt.figure(figsize=(12,10), dpi=400) 
ax = fig.gca(projection='3d')                      
ax.plot_surface(X,Y,u[:])
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel('$u(x,y)$')
ax.set_title(r'$\frac{\partial V}{\partial t} + V \cdot \nabla{V} = \nu {\nabla}^2 V$')
plot = ax.plot_surface(X, Y, u[:], **plot_args)
pam_ani = animation.FuncAnimation(fig, data_gen, fargs=(u, v, plot),
                              interval=100, blit=False)

pam_ani.save('Burgers_2D.mp4', writer=writer)    