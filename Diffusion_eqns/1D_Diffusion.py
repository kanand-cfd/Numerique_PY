# -*- coding: utf-8 -*-
"""
Created on Sat May 23 17:54:04 2020

@author: mechi
"""

# %% Import packages
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-poster')

# %% Parameter declaration & variable initialisation
nx = 41
dx = 2 / (nx - 1)
nt = 40
nu = 0.3
sigma = 0.2
dt = sigma * dx**2 / nu

u = np.ones(nx)
u[int(0.5 / dx):int(1 / dx + 1)] = 2.

un = np.ones(nx)

# %% Iterate through time
for n in range(nt):
    un = u.copy()
    u[1:-1] = un[1:-1] + nu * dt / dx**2 * (un[2:] - 2 * un[1:-1] + un[0:-2])
    if (n % 10 == 0):
        plt.plot(np.linspace(0, 2, nx), u)
        plt.xlabel('$x$')
        plt.ylabel('$u$')
        plt.title('1D Diffusion')
