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

def plotMatrix(matrix, nameX ='', nameY = '', saveUnder = '', showPlot = True):
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
    for i in range(len(namesExcelZCB)):
        data = pd.read_excel('data/' + namesExcelZCB[i] + '.xlsx')
        optimal_x = data[data.columns[1]]
        matrix.append(optimal_x)
    plotMatrix(matrix, 'Months', 'Position in ZCB', saveUnder= 'plot of hedging portfolios ZCB', showPlot=False) #Plots all the net cashflows when the portfolio is hedged with zcb's

def plotAllSwaptionHedgePortfolios():
    namesExcelSwaption = ['swaption margin hedge', 'swaption elastic 0.1 hedge',
                           'swaption elastic 0.5 hedge', 'swaption elastic 0.75 hedge', 'swaption elastic 0.9 hedge']
    matrix = []
    for i in range(len(namesExcelSwaption)):
        data = pd.read_excel('data/' + namesExcelSwaption[i] + '.xlsx')
        optimal_x = data[data.columns[1]]
        matrix.append(optimal_x)
    plotMatrix(matrix, 'Swaptions', 'Position in Swaptions', saveUnder= 'plot of hedging portfolios Swaption', showPlot=False) #Plots all the net cashflows when the portfolio is hedged with zcb's


def main():
    print("hello from Floris")
    
    namesExcelZCB = ['zcb margin hedge', 'zcb elastic 0.1 hedge', 'zcb elastic 0.25 hedge', 'zcb elastic 0.5 hedge', 'zcb elastic 0.75 hedge', 'zcb elastic 0.9 hedge', 'zcb value hedge' ]
    namesExcelSwaption = ['swaption margin hedge', 'swaption elastic 0.1 hedge',
                           'swaption elastic 0.5 hedge', 'swaption elastic 0.75 hedge', 'swaption elastic 0.9 hedge']
    
    data, desired_cashflows,simulated_cashflows,simulated_rates = getData()
    desired_margin_cashflows = Objective_Function_Methods.Compute_Cashflows_Exclusive_Edition(data)
    df = pd.read_excel('data/' + namesExcelZCB[0]+ '.xlsx')
    optimal_x = df[df.columns[1]]
    differences = Objective_Function_Methods.compute_margin_differences(desired_margin_cashflows, simulated_cashflows, optimal_x)
    

    swaptionSet = hedging.create_swaptions(data)
    swaptionPosition =  pd.read_excel('data/' + namesExcelSwaption[0]+ '.xlsx').iloc[:, 1]
    swaptionSet = [hedging.Swaption(0, 24, 0.02829)]
    line1 = []
    line2 = []

    hedge = []
    tottotCashflows = []
    # for i in range(len(simulated_cashflows)):
    for i in range(3):
        for k  in range(len(swaptionSet)):
            swaption = swaptionSet[k]
            t1 = swaption.get_t1()
            t2 = swaption.get_t2()
            cashflow = swaption.swaption_cashflows(simulated_rates[i])
            if (HullWhiteMethods.swapRate(int(t2-t1), 0, simulated_rates[i][t1])[-1] < swaption.get_strike()):
                print(HullWhiteMethods.swapRate(int(t2-t1), 0, simulated_rates[i][t1])[-1])
                totCashflow = []
                for j in range(120):
                    totCashflow.append(cashflow[j]*swaptionPosition[k])
                print(sum(totCashflow))
                # plotY(totCashflow,saveUnder = 'test' + str(i), showPlot = True)
                plotMatrix([totCashflow, differences[i]],saveUnder = 'test' + str(i), showPlot = True)

    # plotList(optimal_x) #Gives a plot of the weights of the hedging porfolio with only zcb
    # plotMatrix(differences, 'Months', 'Deviation from derised margin', saveUnder= "test", showPlot=False) #Plots all the net cashflows when the portfolio is hedged with zcb's


    # plotMatrix(simulated_rates, 'Months', 'Short rate', saveUnder= 'Simulated short rates', showPlot=False) #plots all simulated rates
    # plotMatrix(simulated_cashflows, 'Months', 'Cash flow', saveUnder= 'Simulated cashflows', showPlot=False) #plots all simulated cashflows
    # plotAllDifferencesFromMarginZCBHedge()
    # plotAllZCBHedgePortfolios()
    # plotAllSwaptionHedgePortfolios()
main()
