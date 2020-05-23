# -*- coding: utf-8 -*-
"""
Created on Tue May 19 00:34:36 2020

@author: mechi
"""
# %%
from mpl_toolkits.mplot3d import Axes3D    #New Library required for projected 3d plots

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
#%matplotlib inline
plt.style.use('_classic_test')
# %%
nx = 81 #number of elements in x-direction
ny = 81 #number of elements in y-direction
nt = 100 #number of time steps
dt = 0.005 #time step
c = 1. #wave velocity in x and y direction
dx = 2./(nx-1) #meshsize in x-direction
dy = 2./(ny-1) #meshsize in y-direction

# %%
x = np.linspace(0.,2.,nx)
y = np.linspace(0.,2.,ny)
X, Y = np.meshgrid(x,y) 

u = np.zeros((ny,nx)) 
un = np.zeros((ny,nx))

#assign initial conditions with a 
#"hat-function": u(.5<=x<=1 && .5<=y<=1 ) is 1
u[int(0.5/dy):int(1./dy+1.),int(0.5/dx):int(1./dx+1.)]=1. 

#plot the initial condition
#the figsize parameter can be used to produce different sized images
fig = plt.figure(figsize=(11,7), dpi=100) 
ax = fig.gca(projection='3d')                      
ax.plot_surface(X,Y,u[:]);
surf = ax.plot_surface(X, Y, u[:], cmap=cm.viridis)
ax.set_xlabel('$x$')
ax.set_xlim(0, 2)
# ax.set_ylabel('$y$')
ax.set_ylim(0, 2)
# ax.set_zlabel('$u(x,y)$')
ax.set_zlim(1, 2)
ax.set_title('2D Linear Convection')

# %%set up initial conditions
u = np.zeros((ny,nx))
u[int(0.5/dy):int(1./dy+1.),int(0.5/dx):int(1./dx+1.)]=1.

# %% loop across number of time steps

for n in range(nt+1):
    un = u.copy()
    row, col = u.shape
    u[0,:] = 0.
    u[-1,:] = 0.
    u[:,0] = 0.
    u[:,-1] = 0.
    for j in range(1, row): #x-direction loop
        for i in range(1, col): #y-direction loop
            u[j,i] = un[j, i] - (c*dt/dx*(un[j,i] - un[j,i-1]))-(c*dt/dy*(un[j,i]-un[j-1,i]))
    if (n % 10 == 0):
        fig = plt.figure(figsize=(12,8), dpi=200); ax = fig.gca(projection='3d')
        ax.plot_surface(X,Y,u[:]);
        surf = ax.plot_surface(X, Y, u[:], cmap=cm.viridis)
        ax.set_xlabel('$x$')
        # ax.set_xlim(0, 2)
        ax.set_ylabel('$y$')
        # ax.set_ylim(0, 2)
        ax.set_zlabel('$u(x,y)$')
        # ax.set_zlim(1, 2)
        ax.set_title('2D Linear Convection')

