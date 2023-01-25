# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 14:06:05 2023

@author: qblan
"""

from math import exp
from scipy.integrate import quad
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from math import tan


#This Function Computes A() in the bondcurve expression in the Hull-White model
def A(T, kappa, tau, sigma):
    A = -(sigma**2)/(4*kappa**3)*(3+exp(-2*kappa*tau)-4*exp(-kappa*tau)-2*kappa*tau)+kappa*integral(T, kappa, tau, sigma)
    return A


#This Function Computes B() in the bondcurve expression in the Hull-White model
def B (kappa, tau):
    B = -1/kappa*(1-exp(-kappa*tau))
    return B


#This function is to be integrated for A() and therefore needs to be defined
def integrand(T, z, kappa, tau, sigma):
    function = theta(kappa, sigma, T-z)*B(kappa, z)
    return function
    
    
#This function defines the time varying mean theta(t) for the Hull-White model    
def theta(kappa, sigma, t):
    value = 1/kappa*func_deriv(t,a,b,c,d) + func(t,a,b,c,d) + (sigma**2)/(2*kappa**2)*(1-exp(-2*kappa*t))
    return value


#This function integrates integrand()
def integral(T, kappa, tau, sigma):
    value = quad(integrand, 0, tau, args=(T, kappa, tau, sigma))[0]
    return value


#This function is a generic polynomial of the third order used to fit the swap curve
def func(x,a,b,c,d):
    return a*(x)**3 + b*(x)**2 + c*(x) + d


#This function fits the parameters of a given function to given data
def curve_parameters(data):
    xdata = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    popt, pcov = curve_fit(func, xdata, data)
    return popt
    

#This function gives the value of the derivative of the fitted forward curve. I added d as input, because than you can just enter
# *popt as input, where popt is the output from curve_parameters()
def func_deriv(x,a,b,c,d):
    return 3*a*x**2+2*b*x+c