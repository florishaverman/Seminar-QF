from prepayment import *
from interestRate2 import *
from cashflows import *
from Hedge_Quinten import *
from Objective_Function_Methods import *
from hedging import *
import pandas as pd
import Hedge_Quinten
import Objective_Function_Methods
import hedging
import HullWhiteMethods
import evaluation

""" 
Main.py should be able to execute all the code

@author: Floris
"""

def main():
    print("Hello World from main")
    startTime = time.time()

    optimizeThreeWays()
    
    # print(HullWhiteMethods.swapRate(12, 0.02))

    # for i in range(120):
    #     print(i, optimal_x[i] + simulated_cashflows[2][i])


    #max_maturity = 20
    #interest_rate = 0.03
    #swaptionSet = create_swaptions(max_maturity, interest_rate)
    #for s in swaptionSet:
    #    print(s.swaption_cashflows(interest_rates))
    endTime = time.time()
    print(f"Running main took {round(endTime- startTime,1)} seconds")
    print('main is finished')



def optimizeThreeWays():
    data = loadINGData('Current Mortgage portfolio')
    data.drop(['Variable'], inplace=True, axis=1)
    data.drop([3], inplace=True)
    data.iloc[1] = data.iloc[1] * 12
    current_euribor = loadINGData('Current Euribor Swap Rates')
    # prepayment_model = pickle.load(open('prepayment_model.sav', 'rb'))

    desired_df = pd.read_excel('Data/SimulatedCFnRates.xlsx', sheet_name='Desired CF')
    cf_df = pd.read_excel('Data/SimulatedCFnRates.xlsx', sheet_name='Simulated CF')
    rates_df = pd.read_excel('Data/SimulatedCFnRates.xlsx', sheet_name='Simulated Interest Rates')
    desired_cashflows = []
    simulated_cashflows = []
    simulated_rates = []
    for i in range(desired_df.shape[0]):
        desired_cashflows.append(desired_df.iloc[i, 1])
    for i in range(cf_df.shape[1]-1):
        sim_cf = []
        sim_rates = []
        for j in range(cf_df.shape[0]):
            sim_cf.append(cf_df.iloc[j, i+1])
            sim_rates.append(rates_df.iloc[j, i+1])
        simulated_cashflows.append(sim_cf)
        simulated_rates.append(sim_rates)

    desired_margin_cashflows = Objective_Function_Methods.Compute_Cashflows_Exclusive_Edition(data)
    optimal_x = Hedge_Quinten.zcb_margin_optimization(desired_margin_cashflows, simulated_cashflows)
    differences = Objective_Function_Methods.compute_margin_differences(desired_margin_cashflows, simulated_cashflows, optimal_x)


    swaptionSet = hedging.createSwaptionSetBetweenMaturities()
    # for s in swaptionSet:
    #     print(s.get_t1(),s.get_t2(), s.get_strike())

    combinedOptimizedPortfolio = swaption_elastic_optimization(differences, simulated_rates, swaptionSet, 0.95)
    print(combinedOptimizedPortfolio)
    marginOptimizedPortfolio = swaption_margin_optimization(differences, simulated_rates, swaptionSet, optimal_x)
    print(marginOptimizedPortfolio)
    valueOptimizedPortfolio = swaption_value_optimization(differences, simulated_rates, swaptionSet, optimal_x)
    print(valueOptimizedPortfolio)

main()