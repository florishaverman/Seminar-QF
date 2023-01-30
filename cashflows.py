from prepayment import loadINGData, probPrepayment
from interestRate2 import simulationHullWhite
import HullWhiteMethods as hw
import pickle  # To save logistic model, to avoid training each time.
import numpy as np
import time  # to time the functions
import math #for math


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
                ref_rate = 0.015 #should be calcuated with the swap rate, use swap rate of 0 now.
                incentive = coupon_rate[i] - ref_rate
                sim_prepay_rates[r][i][t] = round(probPrepayment(prepayment_model, incentive)[0], 5)
    return sim_prepay_rates

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

def getAllCashflows(prepaymentRates, notional, FIRP, coupon_rate):
    numPortfolios = 6
    allCashflows = []
    for i in range(numPortfolios):
        allCashflows.append(getCashflowPortfolio(prepaymentRates[i], notional[i], FIRP[i], coupon_rate[i]))
    return allCashflows

def getTotCashflows(prepaymentRates, notional, FIRP, coupon_rate):
    cashflows = getAllCashflows(prepaymentRates, notional, FIRP, coupon_rate)
    totCashflows = [0] * 120
    for t in range(120):
        tot = 0
        for i in range(6):
            tot += cashflows[i][t]
        totCashflows[t] = tot
    return totCashflows

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
    Rcashflows = []
    for r in range(R):
        Rcashflows.append(getTotCashflows(sim_prepay_rates[r], notional, FIRP, coupon_rate))
    return Rcashflows

def main():
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

main()


#sim_prepay_rates [r][i][t] where r is the simulation (1-R), i is the portfolio (1-6), t is the time (1-120)
# print(sim_prepay_rates[0][0])
# cashflows2 = getCashflows(sim_prepay_rates[0], notional, FIRP, coupon_rate)
# i= 0
# print(cashflows2[i])
# print(len(cashflows2[i]))
# print(sum(cashflows2[i]))

 
""" 
 ### BIN ###
def getCashflows(prepaymentRates, notional, FIRP, coupon_rate):
    numPortfolios = len(notional)
    numMonths = max(FIRP)
    # numPortfolios = 2
    # numMonths = 10
    # cashflows = [[0] * numMonths] * numPortfolios
    # print(FIRP[0])
    
    toReturn  = []
    for i in range(numPortfolios):
        cashflows = [0]*numMonths
        for t in range(FIRP[i]):
            #interest payment per month
            interest = coupon_rate[i] * notional[i] / 12
            # prepayments
            prepayment = prepaymentRates[i][t] * notional[i]
            notional[i] -= prepayment
            cashflows.append( round(prepayment + interest, 4))
                
        # cashflows[i][FIRP[i]-1] = round(cashflows[i][FIRP[i]-1]+ notional[i], 4)
        cashflows[-1] = round(cashflows[-1]+ notional[i], 4)
        toReturn.append(cashflows)
    return toReturn



def A(t,T):
    return math.exp(-B(t, T, alpha) )

def B(t,T, alpha):
    return (1 - math.exp(-alpha * (T - t))) / alpha

def getBondPrice(t,T, rt, alpha):
    return A(t,T) * math.exp(-B(t,T, alpha) * rt) """



