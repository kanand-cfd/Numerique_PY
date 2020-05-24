# -*- coding: utf-8 -*-
"""
Created on Tue May 19 12:35:52 2020

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
# %% Parameters for solving 2D convection problem
nx = 81 #number of elements in x-direction
ny = 81 #number of elements in y-direction
nt = 100 #number of time steps
c = 1. #wave velocity in x and y direction
dx = 2./(nx-1) #meshsize in x-direction
dy = 2./(ny-1) #meshsize in y-direction

#Try other values of sigma {0.2,0.5,0.6,1} as well and see what happens 

sigma = 0.5    # CFL Number
dt = sigma * dx # Calulcating time-step using CFL condition 
    
x = np.linspace(0.,2.,nx)
y = np.linspace(0.,2.,ny)
X, Y = np.meshgrid(x,y) 

u = np.ones((ny,nx)) 
#un = np.zeros((ny,nx))

#assign initial conditions with a 
#"hat-function": u(.5<=x<=1 && .5<=y<=1 ) is 1
u[int(0.5/dy):int(1./dy+1.),int(0.5/dx):int(1./dx+1.)]=2. 

# %% Function for updating the hat function
def data_gen(framenumber, u, plot):
    #change soln variable for the next frame
    un = u.copy()
    row, col = u.shape
    c = 1. #wave velocity in x and y direction
    dx = 2./(row-1) #meshsize in x-direction
    dy = 2./(col-1) #meshsize in y-direction
    sigma = 0.5
    dt = sigma * dx
    u[0,:] = 1.
    u[-1,:] = 1.
    u[:,0] = 1.
    u[:,-1] = 1.

    u[1:-1,1:-1]=un[1:-1,1:-1]-(c*dt/dx*(un[1:-1,1:-1]-un[1:-1,0:-2]))-\
        (c*dt/dy*(un[1:-1,1:-1]-un[0:-2,1:-1]))
        
    ax.clear()                      
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_zlabel('$u(x,y)$')
    ax.set_title(r'$\frac{\partial V}{\partial t} + c \cdot \nabla{V}=0$')
    plot = ax.plot_surface(X, Y, u[:], **plot_args)
    return plot

# %% Final plot and animation generation
fig = plt.figure(figsize=(12,10), dpi=400) 
ax = fig.gca(projection='3d')                      
ax.plot_surface(X,Y,u[:])
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel('$u(x,y)$')
ax.set_title(r'$\frac{\partial V}{\partial t} + c \cdot \nabla{V}=0$')
# surf = ax.plot_surface(X, Y, u[:], cmap=cm.viridis)
plot = ax.plot_surface(X, Y, u[:], **plot_args)
pam_ani = animation.FuncAnimation(fig, data_gen, fargs=(u, plot),
                              interval=50, blit=False)

pam_ani.save('convection_2d.mp4', writer=writer)