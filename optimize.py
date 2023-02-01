import numpy as np
from scipy.optimize import minimize
import hedging
import cashflows
import time 

""" optimize.py is used of the optimization of the hedging portfolio.

@autor: Floris
"""


""" This function calculates the objective value of a given vector x of the weights of the hedging portfolio.
This is a bit of a complicated function and is still undergoing changes

x: a 1D vector of weights, where [j] is the weigth coresponding to the j-th hedging instrument

return: the objective value
"""
def objective(x):
    N = len(x)
    T = len(x)
    R = 2

    bonds = hedging.createHedgingBonds(N)
    C = hedging.getCashflowMatrix(bonds, T)
    P =cashflows.getAllSimCashflows(R)
    # print(P)

    # C = [[1 for i in range(N)] for t in range(T)]
    # P = [1 for t in range(T)]
    # C = [[1,0,1,0,1], [0,1,0,1,0]]
    # P = [1,2,1,2,3]
    
    value = 0
    for r in range(R):
        tot = 0
        for t in range(T):
            temp = 0
            for i in range(N):
                temp += x[i] * C[i][t]
            temp -= P[r][t]
            tot += temp**2
        value += tot
    return value


""" This function optimizes the fuction objective """
def optimize():
    startTime = time.time()

    
    x0 = np.array([10000 for t in range(10)])
    print('optimization started')
    res = minimize(objective, x0, options={'disp': True})
    print(res.x)

    endTime = time.time()
    print(f"Calculating cashflows took {round(endTime- startTime,1)} seconds")
    # print(objective([1 for t in range(120)]))
optimize()