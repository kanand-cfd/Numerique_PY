# -*- coding: utf-8 -*-
"""
Created on Thu May 21 09:48:36 2020

@author: mechi
"""

import numpy                       #here we load numpy
from matplotlib import pyplot      #here we load matplotlib

nx = 41  # number of nodes
dx = 2 / (nx-1)
nt = 200    #nt is the number of timesteps we want to calculate
dt = .05  #dt is the amount of time each timestep covers (delta t)
c = 1      #assume wavespeed of c = 1

u = numpy.ones(nx)      #numpy function ones()
u[int(.5 / dx):int(1 / dx + 1)] = 2  #setting u = 2 between 0.5 and 1 as per our I.C.s

un = numpy.ones(nx) #initialize a temporary array

def func(c, u, dx):
    f = numpy.zeros(u.shape)
    for i in range(1, len(u)):
        f[i] = - c * dt / dx * (u[i] - u[i-1])
    return f

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
    u = RK4(c, un, dt, dx)
    # Periodic Boundary Condition
    u[0] = un[0] - c * dt / dx * (un[0] - un[-2]) 
    u[-1] = u[0]
    if (n % 20 == 0):
        fig = pyplot.figure(figsize=(11,7), dpi=200)
        pyplot.plot(numpy.linspace(0, 2, nx), u);  
    

#pyplot.plot(numpy.linspace(0, 2, nx), u);    
