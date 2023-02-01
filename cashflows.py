from prepayment import *
from interestRate2 import *
import HullWhiteMethods as hw
import pickle  # To save logistic model, to avoid training each time.
import numpy as np

""" 

Cashflows.py is used for calculating the simulated cashflows of the morgage portfolio

The whole process is split up in different function. The basic order is:
First the prepayment rates are calculated for all mortgage portfolios for each interation, based on the simulated interest rates from the Hull-White model
These are given in a big 3D matrix with dimentions, for each simulation (r/R is used for this), each mortgage portfolio (i/T is used for this)
and finally each time point (t/T is used for time). 

This is used to create a 2D array with per simulation, the total cashflows at time t. Where the cashflows of the different portfolios are summed. 

@author: Floris

"""


""" 
This function returns a 3D matrix R x N x T with all the prepayment rates
Thus getPrepayments(coupon_rate, FIRP, R, hullWhiteParam)[r][i][t] is the prepayment rate from the r-th simulation for portfolio i at time t. 
coupon_rate: The vector of the coupon rates for each of the 6 portfolios
FIRP: The vector of remain tems for each of the 6 portfolios
R: The number of simulations
hullWhiteParam: A vector containing the hull white parameters: [alpha, sigma, popt, r_zero, delta, T, random]

return: a 3D array, where [r][i][t] is the prepayment rate from the r-th simulation for portfolio i at time t.
"""
def getPrepayments(coupon_rate, FIRP, R, hullWhiteParam):
    alpha = hullWhiteParam[0]
    sigma = hullWhiteParam[1]
    popt = hullWhiteParam[2]
    r_zero = hullWhiteParam[3]
    delta = hullWhiteParam[4]
    T = hullWhiteParam[5]
    random = hullWhiteParam[6]
    #load prepayment model
    prepayment_model = pickle.load(open('prepayment_model.sav', 'rb'))

    # Store all simulated cashflows
    numPortfolios = 6
    sim_prepay_rates = [ [[0 for i in range(max(FIRP))] for i in range(numPortfolios)] for j in range(R) ]

    for r in range(R):
        interest_rates = simulationHullWhite(alpha, sigma, popt, r_zero, delta, T, random)
        for i in range(numPortfolios):
            for t in range(FIRP[i]):
                # ref_rate = 0.015 + interest_rates[t]#should be calcuated with the swap rate, use swap rate of 0 now.
                ref_rate = 0.015 + random.random()*0.03
                incentive = coupon_rate[i] - ref_rate
                sim_prepay_rates[r][i][t] = round(probPrepayment(prepayment_model, incentive)[0], 5)
    return sim_prepay_rates

""" This fuctions returns a 1D array with the cashflows for 1 portfolio, including prepayments, interest rate payments and final repayment.
prepaymentRate: A 1D vector of prepayment rates of length at least the length of the portfolio
notional: The notional value of the portfolio
FIRP: The remaining term of the  portfolio
coupon_rate: The coupon rate of the portfolio

return: 1D array, where [t] is the cashflow at time t. 
"""
def getCashflowPortfolio(prepaymentRate, notional, FIRP, coupon_rate):
    outstanding = notional
    cashflow = [0] *120
    for t in range(FIRP):
        interest = outstanding * coupon_rate / 12
        prepayment = prepaymentRate[t] * outstanding
        outstanding = outstanding - prepayment
        cashflow[t] = round(interest + prepayment, 4)
    cashflow[FIRP-1] = round(cashflow[FIRP-1] + outstanding, 4)
    return cashflow

""" 
This function calculates the cashflows of one simulation run.
prepaymentRate: A 2D array of prepayment rates, where [i][t] is the prepayment rate of portfolio i at time t. 
notional: The vector of the notional values for each of the 6 portfolios
coupon_rate: The vector of the coupon rates for each of the 6 portfolios
FIRP: The vector of remain tems for each of the 6 portfolios

return: 2D array, where [i][t] is the cashflow of portfolio i at time t.
"""
def getAllCashflows(prepaymentRates, notional, FIRP, coupon_rate):
    numPortfolios = 6
    allCashflows = []
    for i in range(numPortfolios):
        allCashflows.append(getCashflowPortfolio(prepaymentRates[i], notional[i], FIRP[i], coupon_rate[i]))
    return allCashflows

""" 
This functions calculates aggregates the cashflows by portfolio, resulting in the total cashflow at each point in time
prepaymentRate: A 2D array of prepayment rates, where [i][t] is the prepayment rate of portfolio i at time t. 
notional: The vector of the notional values for each of the 6 portfolios
coupon_rate: The vector of the coupon rates for each of the 6 portfolios
FIRP: The vector of remain tems for each of the 6 portfolios

return: 1D array with the total cashflows at each point in time t. 
"""
def getTotCashflows(prepaymentRates, notional, FIRP, coupon_rate):
    cashflows = getAllCashflows(prepaymentRates, notional, FIRP, coupon_rate)
    totCashflows = [0] * 120
    for t in range(120):
        tot = 0
        for i in range(6):
            tot += cashflows[i][t]
        totCashflows[t] = tot
    return totCashflows

""" 
THIS IS THE MAIN FUNCTION

This function creates a 2D array, where [r][t] is the cashflow of the r-th simulation at time time t.
This functions uses the hull white parameters that are defined within this function. 
R: This is the only import parameter needed and is the number of simulations

return: 2D array, where [r][t] is the cashflow of the r-th simulation at time time t
"""
def getAllSimCashflows(R):
    data = loadINGData('Current Mortgage portfolio')
    data = data.drop('Variable', axis=1)
    margin = data.loc[4, 1]
    notional = np.array(data.loc[0])
    FIRP = np.array(data.loc[1]*12)  # In months
    coupon_rate = np.array(data.loc[2])

    ### White hull parameters ###
    current_euribor = loadINGData('Current Euribor Swap Rates')
    current_euribor = current_euribor.loc[:, 'Swap rate']
    
    alpha = 1.5  # = kappa
    sigma = 0.12
    popt = hw.curve_parameters(current_euribor)
    r_zero = 1
    delta = 0.01
    T = 120
    random = np.random.default_rng(123)
    hullWhiteParam = [alpha, sigma, popt, r_zero, delta, T, random]

    sim_prepay_rates = getPrepayments(coupon_rate, FIRP, R, hullWhiteParam)
    # print(sim_prepay_rates)
    Rcashflows = []
    for r in range(R):
        Rcashflows.append(getTotCashflows(sim_prepay_rates[r], notional, FIRP, coupon_rate))
    return Rcashflows

# used to try some stuff in this file. 
def main():
    print("Hello World from cashflows.py")
    startTime = time.time()

    R = 10
    Rcashflows = getAllSimCashflows(R)
    totCashflows = []
    for r in range(R):
        totCashflows.append(sum(Rcashflows[r]))
    print(totCashflows)

    endTime = time.time()
    print(f"Calculating cashflows took {round(endTime- startTime,1)} seconds")
    print('Cashflows.py is finished')

# main()
