# general tools
import numpy as np
import math
from HullWhiteMethods import theta

import pandas as pd  # for reading excel data file


# Simulate interest rates using Hull-White model

def simulationHullWhite(alpha, sigma, popt, r_zero, n_steps, T):
    # Number of steps per period
    delta = (1 / n_steps)

    # 2D matrix storing the simulated interest rates per month
    sim_rates = []
    # Store rates for all steps
    rates = [r_zero]
    # Simulate T months with S steps per month
    for t in range(T):
        # Here: determine theta for current period
        theta_curr = theta(alpha, sigma, t/12, *popt)
        for s in range(n_steps):
            # Euler discretization for simulating next step
            sim = rates[-1] + alpha * (theta_curr - rates[-1]) * delta + sigma * np.random.normal(0, delta)
            rates.append(sim)
        # Append interest rate to matrix of interest rates
        interest_rate = rates[-1]
        sim_rates.append(interest_rate)

    # Output: list of interest rates for each month up to final period for one simulation run
    return sim_rates
