import numpy as np
from scipy.optimize import minimize
import hedging
import cashflows
import time 
def rosen(x):
    """The Rosenbrock function"""
    return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)



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


startTime = time.time()

x0 = np.array([10000 for t in range(20)])
# res = minimize(objective, x0, options={'disp': True})
# print(res.x)

P =cashflows.getAllSimCashflows(2)
print(P[0][:20])
print()
print(P[1][:20])
endTime = time.time()
print(f"Calculating cashflows took {round(endTime- startTime,1)} seconds")
# print(objective([1 for t in range(120)]))