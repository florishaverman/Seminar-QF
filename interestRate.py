# general tools
import numpy as np
import math

import pandas as pd  # for reading excel data file


### Simulate interest rates using Hull-White model

def simulationHullWhite(theta, alpha, sigma, r_zero, R, delta, T):
    # Number of steps per period
    S = math.floor(1 / delta)

    # 2D matrix storing the simulated interest rates per month
    sim_rates = [[0] * T for i in range(R)]
    # Simulate for R replications
    for r in range(R):
        rates = [r_zero]
        # Simulate T months with S steps per month
        for t in range(T):
            for s in range(1, S):
                # Euler discretization for simulating next step
                sim = rates[r][s - 1] + (theta - alpha * rates[r][s - 1]) * delta + sigma * np.random.normal(0, 1)
                rates.append(sim)
            # Append interest rate to matrix of interest rates
            interest_rate = rates[-1]
            sim_rates[r][t] = interest_rate