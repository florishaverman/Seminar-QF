# general tools
import numpy as np
import math
from HullWhiteMethods import theta

import pandas as pd  # for reading excel data file


# Simulate interest rates using Hull-White model

def simulationHullWhite(alpha, sigma, popt, r_zero, delta, T, random):
    # Number of steps per period
    S = math.floor(1 / delta)

    # 2D matrix storing the simulated interest rates per month
    sim_rates = []
    # Store rates for all steps
    rates = [r_zero]
    # Simulate T months with S steps per month
    for t in range(T):
        # Here: determine theta for current period
        theta_curr = theta(kappa=alpha, sigma=sigma, t=t, a=popt[0], b=popt[1],c= popt[2], d=popt[3])
        for s in range(0, S):
            # Euler discretization for simulating next step
            sim = rates[-1] + (theta_curr - alpha * rates[-1]) * delta + sigma * random.standard_normal()
            rates.append(sim)
        # Append interest rate to matrix of interest rates
        interest_rate = rates[-1]
        sim_rates.append(interest_rate)

    # Output: list of interest rates for each month up to final period for one simulation run
    return sim_rates

def main():

    # Forward curve parameters used in theta
    popt = [ -2.85668639e-06,  9.30831377e-05, -1.02552560e-03, 2.96105820e-02 ]
    alpha = 1.5  # = kappa
    sigma = 0.12
    r_zero = 1
    delta = 0.01
    T = 120
    interest_rates = simulationHullWhite(alpha, sigma, popt, r_zero, delta, T,np.random.default_rng(42))
    print(interest_rates)

    
