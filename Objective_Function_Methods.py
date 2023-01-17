# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 16:16:28 2023

@author: qblan
"""

import pandas as pd
from operator import add


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
    

def Compute_Relative_MSE(expected, real):
    N = len(expected)
    MSE = 0
    for i in range(N):
        MSE += (abs(expected[i]-real[i])/expected[i])**2
    MSE = MSE/N
    return MSE


def Compute_Absolute_MSE(expected, real):
    N = len(expected)
    MSE = 0
    for i in range(N):
        MSE += (expected[i]-real[i])**2
    MSE = MSE/N
    return MSE