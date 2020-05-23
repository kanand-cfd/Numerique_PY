# -*- coding: utf-8 -*-
"""
Created on Sat May 23 10:55:04 2020

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

# %% Parameter declaration
nx = 101
ny = 101
nt = 81
dx = 2 / (nx - 1)
dy = 2 / (ny - 1)
sigma = 0.2
dt = sigma * dx

x = np.linspace(0, 2, nx)
y = np.linspace(0, 2, ny)
X, Y = np.meshgrid(x, y)

u = np.ones((ny, nx))
v = np.ones((ny, nx))
un = np.ones((ny, nx))
vn = np.ones((ny, nx))

# Assign initial conditions
# set hat function I.C.: u(.5<=x<=1 && .5<=y<=1 ) is 2
u[int(.5 / dy):int(1 / dy + 1), int(.5 / dx):int(1 / dx + 1)] = 2

# set hat function I.C.: v(.5<=x<=1 && .5<=y<=1 ) is 2
v[int(.5 / dy):int(1 / dy + 1), int(.5 / dx):int(1 / dx + 1)] = 2

# %% Function for updating the hat function along with the hat functions
def data_gen(framenumber, u, v, plot):
    #change soln variable for the next frame
    un = u.copy()
    vn = v.copy()
    row, col = u.shape
    dx = 2./(row-1) #meshsize in x-direction
    dy = 2./(col-1) #meshsize in y-direction
    sigma = 0.2
    dt = sigma * dx
    u[0,:] = 1
    u[-1,:] = 1
    u[:,0] = 1
    u[:,-1] = 1
    
    v[0,:] = 1
    v[-1,:] = 1
    v[:, 0] = 1
    v[:, -1] = 1
    
    u[1:, 1:] = un[1:, 1:] - (un[1:,1:] * (dt / dx) * (un[1:,1:] - un[1:,:-1])) -\
        (vn[1:,1:] * (dt / dy) * (un[1:,1:] - un[:-1, 1:]))
    v[1:, 1:] = vn[1:, 1:] - (un[1:,1:] * (dt / dx) * (vn[1:,1:] - vn[1:,:-1])) -\
        (vn[1:,1:] * (dt / dy) * (vn[1:, 1:] - vn[:-1, 1:]))
    
    ax.clear()                      
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_zlabel('$u(x,y)$')
    ax.set_title('2D Non-Linear Convection')
    plot = ax.plot_surface(X, Y, u[:], **plot_args)
    
    return plot

# %% Final plot and animation generation
fig = plt.figure(figsize=(12,10), dpi=400) 
ax = fig.gca(projection='3d')                      
ax.plot_surface(X,Y,u[:])
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel('$u(x,y)$')
ax.set_title('2D Non-Linear Convection')
plot = ax.plot_surface(X, Y, u[:], **plot_args)
pam_ani = animation.FuncAnimation(fig, data_gen, fargs=(u, v, plot),
                              interval=50, blit=False)

pam_ani.save('convection_coupled.mp4', writer=writer)    