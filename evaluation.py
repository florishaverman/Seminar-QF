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

def plotY(y,saveUnder = '', showPlot = True):
    ypoints = np.array(y)
    plt.plot(ypoints)
    if (saveUnder != ''):
        plt.savefig('plots/Floris/' + saveUnder + '.png')
    if (showPlot): 
        plt.show()

def plotList(list):
    
    plt.plot(list, label = 'line ')
    plt.show()

def plotMatrix(matrix, nameX, nameY, saveUnder = '', showPlot = True):
    for i in range(len(matrix)):
        plt.plot(matrix[i], label = 'line ' + str(i))
    #plt.plot(extra, color = 'black' )
    plt.xlabel(nameX)
    plt.ylabel(nameY)
    if (saveUnder != ''):
        plt.savefig('plots/Floris/' + saveUnder + '.png')
    if (showPlot): 
        plt.show()


def plotDifferenceFromMarginZCBHedge(desired_margin_cashflows, simulated_cashflows, fileName):
    data = pd.read_excel('data/' + fileName+ '.xlsx')
    optimal_x = data[data.columns[1]]
    differences = Objective_Function_Methods.compute_margin_differences(desired_margin_cashflows, simulated_cashflows, optimal_x)

    # plotList(optimal_x) #Gives a plot of the weights of the hedging porfolio with only zcb
    plotMatrix(differences, 'Months', 'Deviation from derised margin', saveUnder= fileName, showPlot=False) #Plots all the net cashflows when the portfolio is hedged with zcb's

def plotAllDifferencesFromMarginZCBHedge():
    namesExcelZCB = ['zcb margin hedge', 'zcb elastic 0.1 hedge', 'zcb elastic 0.25 hedge', 'zcb elastic 0.5 hedge', 'zcb elastic 0.75 hedge', 'zcb elastic 0.9 hedge', 'zcb value hedge' ]
    
    data, desired_cashflows,simulated_cashflows,simulated_rates = getData()
    desired_margin_cashflows = Objective_Function_Methods.Compute_Cashflows_Exclusive_Edition(data)

    for i in range(7):
        plotDifferenceFromMarginZCBHedge(desired_margin_cashflows, simulated_cashflows, namesExcelZCB[i])

def plotAllZCBHedgePortfolios():
    namesExcelZCB = ['zcb margin hedge', 'zcb elastic 0.1 hedge', 'zcb elastic 0.25 hedge', 'zcb elastic 0.5 hedge', 'zcb elastic 0.75 hedge', 'zcb elastic 0.9 hedge', 'zcb value hedge' ]
    matrix = []
    for i in range(7):
        data = pd.read_excel('data/' + namesExcelZCB[i] + '.xlsx')
        optimal_x = data[data.columns[1]]
        matrix.append(optimal_x)
    plotMatrix(matrix, 'Months', 'Position in ZCB', saveUnder= 'portfolio plot of portfolios', showPlot=False) #Plots all the net cashflows when the portfolio is hedged with zcb's

def main():
    print("hello from Floris")
    # plotAllDifferencesFromMarginZCBHedge()
    # plotAllZCBHedgePortfolios()
main()
