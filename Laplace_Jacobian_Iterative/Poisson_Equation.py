# -*- coding: utf-8 -*-
"""
Created on Tue May 26 10:20:50 2020

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
    ax.plot_surface(X, Y, p[:], rstride=1, cstride=1, cmap=cm.RdBu,
                           linewidth=0.05,antialiased=True, color='k')
    ax.view_init(30,225)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_zlabel('$p$')
    plt.savefig(string)

# %% Poisson Function
def Poisson2d(p, dy, dx, nx, ny, nt, b):
    pd = np.empty_like(p)
    
    for it in range(nt):
        pd = p.copy()
        p[1:-1,1:-1] = ((dy*dy)*(pd[1:-1,2:] + pd[1:-1,0:-2]) + (dx*dx)*(pd[2:,1:-1] +\
                        pd[0:-2,1:-1]) - b[1:-1, 1:-1]*(dx*dx)*(dy*dy)) / (2*(dx*dx + dy*dy))
            
        p[:,0] = 0 
        p[ny-1,:] = 0 
        p[0,:] = 0 
        p[:,nx-1] = 0 
    
    return p

# %% Variable Declarations
nx = 51
ny = 51
nt = 100
dx = 2 / (nx - 1)
dy = 2 / (ny - 1)

# Initialization
p = np.zeros((ny,nx))
b = np.zeros((ny,nx))
x = np.linspace(0, 2, nx)
y = np.linspace(0, 1, ny)


# Source Term
b[int(ny/4), int(nx/4)] = 100.0
b[int(3 * ny / 4), int(3 * nx / 4)] = -100

# Plot Initial Conditions
plot2D(x, y, p, 'Initial_Conditions_Laplace.png')

# Call Laplace
Poisson2d(p, dy, dx, nx, ny, nt, b)

#Plot final field
plot2D(x, y, p, 'Final_Result_Laplace.png')