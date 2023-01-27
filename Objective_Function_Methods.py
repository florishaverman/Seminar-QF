# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 16:16:28 2023

@author: qblan
"""

import pandas as pd
from operator import add


# This method returns a list of cash flows that would occur starting from the present if there would be no prepayments. It takes the original mortgage portfolio as input.
def Compute_Cash_Flows(mortgageData):
    max_len = max(mortgageData.iloc[1])
    cash_flows = []
    for i in range(max_len):
        addition = 0
        for j in range(6):
            if mortgageData.iloc[1,j] >= i+1:
                addition += mortgageData.iloc[2,j]/12*mortgageData.iloc[0,j]
            if mortgageData.iloc[1,j] == i+1:
                addition += mortgageData.iloc[0,j]
        cash_flows.append(addition)
    return cash_flows


# This method computes for the next 120 months (The longest loan has an FIRP of 10 years) the net present value of the mortgage portfolio at that time    
def Compute_Time_Values(mortgageData):
    max_len = max(mortgageData.iloc[1])
    total_value = []
    for j in range(6):
        value = []
        for i in range(max_len):
            addition = 0
            if mortgageData.iloc[1,j] >= max_len-i:
                addition += mortgageData.iloc[2,j]/12*mortgageData.iloc[0,j]/(1+mortgageData.iloc[2,j])
            if mortgageData.iloc[1,j] == max_len-i:
                addition += mortgageData.iloc[0,j]/(1+mortgageData.iloc[2,j])
            if i>0:
                addition += value[i-1]/(1+mortgageData.iloc[2,j])
            value.append(addition)
        if j == 0:
            total_value = value
        if j>0:
            total_value = [sum(x) for x in zip(total_value, value)]
    total_value.reverse()
    return total_value
    

# This method computes the relative MSE (relative to the expected cash flows or value) with the expected and predicted series as input.
def Compute_Relative_MSE(expected, real):
    N = len(expected)
    MSE = 0
    for i in range(N):
        MSE += (abs(expected[i]-real[i])/expected[i])**2
    MSE = MSE/N
    return MSE


# This method computes the MSE in absolute terms and as such is probably completely irrelevant.
def Compute_Absolute_MSE(expected, real):
    N = len(expected)
    MSE = 0
    for i in range(N):
        MSE += (expected[i]-real[i])**2
    MSE = MSE/N
    return MSE


#This function recursively computes the cashflows resulting from a  ortgage portfolio and a sequence of prepayment rates.
def Altered_Cashflows(empty_list, prepayment_rates, portfolio):
    if not prepayment_rates:
        return empty_list
    cash_flow = 0
    for i in range(6):
        if portfolio.iloc[1,i] > 0:
            cash_flow += prepayment_rates[0]*portfolio.iloc[0,i]
            portfolio.iloc[0,i] -= prepayment_rates[0]*portfolio.iloc[0,i]
            cash_flow += portfolio.iloc[2,i]/12*portfolio.iloc[0,i]
            if portfolio.iloc[1,i] == 1:
                cash_flow += portfolio.iloc[0,i]
            portfolio.iloc[1,i] = portfolio.iloc[1,i] - 1
    empty_list.append(cash_flow)
    new_rates = prepayment_rates[1:]
    output = Altered_Cashflows(empty_list, new_rates, portfolio)
    return output