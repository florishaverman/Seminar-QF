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


# This Function Computes A() in the bond curve expression in the Hull-White model
def A(T, kappa, t, sigma, a, b, c, d):
    A = kappa * Riemann(kappa, sigma, t, T, a, b, c, d) + sigma**2/(4*kappa**3) * \
        (exp(-2*kappa*(T-t)) * (4*exp(kappa*(T-t)) - 1) - 3) + sigma**2*(T-t)/(2*kappa**2)
    return A


# This Function Computes B() in the bond curve expression in the Hull-White model
def B(kappa, tau):
    B = 1 / kappa * (exp(-kappa * tau) - 1)
    return B


# Determine the analytical zero-coupon bond price for Hull-White
def bondPrice(T, kappa, tau, sigma, r, a, b, c, d):
    bond_price = exp(A(T, kappa, tau, sigma, a, b, c, d) + B(kappa, tau) * r)
    return bond_price


# This function is to be integrated for A() and therefore needs to be defined
def integrand(T, t, kappa, sigma, a, b, c, d):
    function = theta(kappa, sigma, T - t, a, b, c, d) * B(kappa, T - t)
    return function


# This function defines the time varying mean theta(t) for the Hull-White model
def theta(kappa, sigma, t, a, b, c, d):
    value = 1 / kappa * func_deriv(t, a, b, c, d) + func(t, a, b, c, d) + (sigma ** 2) / (2 * kappa ** 2) * \
            (1 - exp(-2 * kappa * t))
    return value


# This function integrates integrand()
def integral(T, kappa, t, sigma, a, b, c, d):
    value = quad(integrand, 0, T - t, args=(T, kappa, sigma, a, b, c, d))[0]
    return value


# This function is a generic polynomial of the third order used to fit the swap curve
def func(x, a, b, c, d):
    return a * x ** 3 + b * x ** 2 + c * x + d


# This function fits the parameters of a given function to given data
def curve_parameters(data):
    xdata = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    popt, pcov = curve_fit(func, xdata, data)
    return popt


# This function gives the value of the derivative of the fitted forward curve.
# I added d as input, because than you can just enter
# *popt as input, where popt is the output from curve_parameters()
def func_deriv(x, a, b, c, d):
    return 3 * a * x ** 2 + 2 * b * x + c


# This function returns a riemann sum as an approximation of an integral
def Riemann(kappa, sigma, t, T, a, b, c, d):
    value = 0
    tau = T - t
    for i in range(10000):
        variable = tau/10000 * i
        value += theta(kappa, sigma, variable, a, b, c, d) * B(kappa, variable) * (tau/10000)
    return value


# This function returns an integral approximation using monte carlo simulation
def Monte_Carlo(kappa, sigma, t, T, a, b, c, d):
    value = 0
    for i in range(10000):
        draw = np.random.uniform(0, T - t)
        value += theta(kappa, sigma, draw, a, b, c, d) * B(kappa, draw) * ((T - t)/10000)
    return value