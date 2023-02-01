from prepayment import *
from interestRate2 import *
from cashflows import *

""" 
Main.py should be able to execute all the code

@author: Floris
"""

def main():
    print("Hello World from main")
    startTime = time.time()

    R = 10
    Rcashflows = getAllSimCashflows(R)
    totCashflows = []
    for r in range(R):
        totCashflows.append(sum(Rcashflows[r]))
    print(totCashflows)

    endTime = time.time()
    print(f"Calculating cashflows took {round(endTime- startTime,1)} seconds")
    print('main is finished')
    
main()