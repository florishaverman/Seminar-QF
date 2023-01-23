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

def A(T, kappa, tau, sigma):
    A = -(sigma**2)/(4*kappa**3)*(3+exp(-2*kappa*tau)-4*exp(-kappa*tau)-2*kappa*tau)+kappa*integral(T, kappa, tau, sigma)
    return A


def B (kappa, tau):
    B = -1/kappa*(1-exp(-kappa*tau))
    return B



def integrand(T, z, kappa, tau, sigma):
    function = theta(kappa, sigma, T-z)*B(kappa, z)
    return function
    
    
    
def theta(kappa, sigma, t):
    value = kappa + sigma
    return value


def integral(T, kappa, tau, sigma):
    value = quad(integrand, 0, tau, args=(T, kappa, tau, sigma))[0]
    return value