# -*- coding: utf-8 -*-
"""
Created on Tue May 26 08:55:40 2020

@author: mechi
"""

# %% Import packages
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import mpl_toolkits.mplot3d as Axes3D
plt.style.use('_classic_test')

# %% Plot function
def plot2D(x, y, p, string):
    
    fig = plt.figure(figsize=(12,10), dpi=600)
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(x, y)
    surf = ax.plot_surface(X, Y, p[:], rstride=1, cstride=1, cmap=cm.RdBu,
                           linewidth=0.05,antialiased=True)
    ax.set_xlim(0,2)
    ax.set_ylim(0,1)
    ax.view_init(30,225)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_zlabel('$p$')
    plt.savefig(string)

# %% Laplace Function
def laplace2d(p, y, dy, dx, l1norm_target):
    l1norm = 1
    pn = np.empty_like(p)
    
    while l1norm > l1norm_target:
        pn = p.copy()
        p[1:-1,1:-1] = ((dy*dy)*(pn[1:-1,2:] + pn[1:-1,0:-2]) + (dx*dx)*(pn[2:,1:-1] +\
                        pn[0:-2,1:-1])) / (2*(dx*dx + dy*dy))
            
        p[:,0] = 0 # p = 0 @ x = 0
        p[:,-1] = y # p = y @ x = 2
        p[0,:] = p[1,:] # dp/dy = 0 @ y = 0
        p[-1,:] = p[-2,:] # dp/dy = 0 @ y = 1
        l1norm = (np.sum(np.abs(p[:]) - np.abs(pn[:])) /
                  np.sum(np.abs(pn[:])))
    
    return p

# %% Variable Declarations
nx = 41
ny = 41
dx = 2 / (nx - 1)
dy = 2 / (ny - 1)

# initial conditions
p = np.zeros((ny,nx))

##plotting aids
x = np.linspace(0, 2, nx)
y = np.linspace(0, 1, ny)

# boundary conditions
p[:,0] = 0  # p = 0 @ x = 0
p[:, -1] = y # p = y @ x = 2
p[0, :] = p[1, :] # dp/dy = 0 @ y = 0
p[-1, :] = p[-2, :] # dp/dy = 0 @ y = 1
 
     
# Plot Initial Conditions
plot2D(x, y, p, 'Initial_Conditions.png')

# Call Laplace
laplace2d(p, y, dy, dx, 1e-4)

#Plot final field
plot2D(x, y, p, 'Final_Result.png')