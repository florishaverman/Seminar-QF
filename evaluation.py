import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

import Hedge_Quinten
import Objective_Function_Methods
import hedging
import HullWhiteMethods
import prepayment

def getData():
    data = prepayment.loadINGData('Current Mortgage portfolio')
    data.drop(['Variable'], inplace=True, axis=1)
    data.drop([3], inplace=True)
    data.iloc[1] = data.iloc[1] * 12
    current_euribor = prepayment.loadINGData('Current Euribor Swap Rates')
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
    return data, desired_cashflows,simulated_cashflows,simulated_rates

def plotXY(x,y):
    xpoints = np.array(x)
    ypoints = np.array(y)

    plt.plot(xpoints, ypoints)
    plt.show()

def plotY(y):
    ypoints = np.array(y)

    plt.plot(ypoints)
    plt.show()

def plotList(list):
    
    plt.plot(list, label = 'line ')
    plt.show()

def plotMatrix(matrix, nameX, nameY):
    for i in range(len(matrix)):
        plt.plot(matrix[i], label = 'line ' + str(i))
    #plt.plot(extra, color = 'black' )
    plt.xlabel(nameX)
    plt.ylabel(nameY)
    plt.show()


def main():
    data, desired_cashflows,simulated_cashflows,simulated_rates = getData()
    desired_margin_cashflows = Objective_Function_Methods.Compute_Cashflows_Exclusive_Edition(data)
    optimal_x = Hedge_Quinten.zcb_margin_optimization(desired_margin_cashflows, simulated_cashflows)
    differences = Objective_Function_Methods.compute_margin_differences(desired_margin_cashflows, simulated_cashflows, optimal_x)


    # plotList(optimal_x) #Gives a plot of the weights of the hedging porfolio with only zcb
    plotMatrix(differences, 'Months', 'Deviation from derised margin') #Plots all the net cashflows when the portfolio is hedged with zcb's
#main()

def sandBox():
    prices = []
    yields = []
    
    for i in range(1,120):
        tempPrice = HullWhiteMethods.bondPrice(i, 0.15, 0, 0.0266, 0.01, -2.85668639e-06,  9.30831377e-05, -1.02552560e-03,  2.96105820e-02)
        tempYield = -1*  math.log(tempPrice)/ (i/12)

        prices.append(tempPrice)
        yields.append(tempYield)
    # plotY(prices)
    sr = HullWhiteMethods.swapRate(120, 0, 0.01)
    print(sr)
    plotY(sr)

# sandBox()