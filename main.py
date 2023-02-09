from prepayment import *
from interestRate2 import *
from cashflows import *
from Hedge_Quinten import *
from outputCreation import *
from Objective_Function_Methods import *

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

#main()

def getSimCF():
    data = loadINGData('Current Mortgage portfolio')
    data.drop(['Variable'], inplace=True, axis=1)
    data.drop([3], inplace=True)
    data.iloc[1] = data.iloc[1] * 12
    current_euribor = loadINGData('Current Euribor Swap Rates')
    prepayment_model = pickle.load(open('prepayment_model.sav', 'rb'))

    alpha = 1.5
    sigma = 0.2663
    n_steps = 100
    T = 120
    R = 100
    cf, rates = generate_multiple_cashflows(data, current_euribor, prepayment_model, alpha, sigma, n_steps, T, R)
    desired_cf = Compute_Cash_Flows(data)
    writeCashflows('Simulated CF', desired_cf, cf)

getSimCF()
