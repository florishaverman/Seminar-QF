# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 16:16:28 2023

@author: qblan
"""

import pandas as pd
from operator import add


# This method returns a list of cash flows that would occur starting from the present if there would be no prepayments.
# It takes the original mortgage portfolio as input.
def Compute_Cash_Flows(mortgageData):
    max_len = max(mortgageData.iloc[1])
    cash_flows = []
    for i in range(max_len):
        addition = 0
        for j in range(6):
            if mortgageData.iloc[1, j] >= i + 1:
                addition += mortgageData.iloc[2, j] / 12 * mortgageData.iloc[0, j]
            if mortgageData.iloc[1, j] == i + 1:
                addition += mortgageData.iloc[0, j]
        cash_flows.append(addition)
    return cash_flows


def Compute_Cashflows_Exclusive_Edition(mortgageData):
    max_len = max(mortgageData.iloc[1])
    cash_flows = []
    for i in range(max_len):
        addition = 0
        for j in range(6):
            if mortgageData.iloc[1, j] >= i + 1:
                addition += 0.015 / 12 * mortgageData.iloc[0, j]
        cash_flows.append(addition)
    return cash_flows


# This method computes for the next 120 months (The longest loan has an FIRP of 10 years) the net present value
# of the mortgage portfolio at that time
def Compute_Time_Values(mortgageData):
    max_len = max(mortgageData.iloc[1])
    total_value = []
    for j in range(6):
        value = []
        for i in range(max_len):
            addition = 0
            if mortgageData.iloc[1, j] >= max_len - i:
                addition += mortgageData.iloc[2, j] / 12 * mortgageData.iloc[0, j] / (1 + mortgageData.iloc[2, j] / 12)
            if mortgageData.iloc[1, j] == max_len - i:
                addition += mortgageData.iloc[0, j] / (1 + mortgageData.iloc[2, j] / 12)
            if i > 0:
                addition += value[i - 1] / (1 + mortgageData.iloc[2, j] / 12)

            value.append(addition)
        if j == 0:
            total_value = value
        if j > 0:
            total_value = [sum(x) for x in zip(total_value, value)]
    total_value.reverse()
    return total_value


# This method computes the relative MSE (relative to the expected cash flows or value) with the expected and
# predicted series as input.
def Compute_Relative_MSE(expected, real):
    N = len(expected)
    MSE = 0
    for i in range(N):
        MSE += (abs(expected[i] - real[i]) / expected[i]) ** 2
    MSE = MSE / N
    return MSE


# This method computes the MSE in absolute terms and as such is probably completely irrelevant.
def Compute_Absolute_MSE(expected, real):
    N = len(expected)
    MSE = 0
    for i in range(N):
        MSE += (expected[i] - real[i]) ** 2
    MSE = MSE / N
    return MSE


# This function recursively computes the cashflows per mortgage resulting from a  mortgage portfolio
# and a sequence of prepayment rates. IMPORTANT: empty_list is a list of 6 empty lists, one for each mortgage
# and prepayment_rates is a list of six prepayment rate lists. So one for every mortgage
def Altered_Cashflows(empty_list, prepayment_rates, mortgageData):
    portfolio = mortgageData.copy()
    new_rates = prepayment_rates
    if not prepayment_rates[0]:
        return empty_list
    for i in range(6):
        cash_flow = 0
        if portfolio.iloc[1, i] > 0:
            cash_flow += prepayment_rates[i][0] * portfolio.iloc[0, i]
            portfolio.iloc[0, i] -= prepayment_rates[i][0] * portfolio.iloc[0, i]
            cash_flow += portfolio.iloc[2, i] / 12 * portfolio.iloc[0, i]
            if portfolio.iloc[1, i] == 1:
                cash_flow += portfolio.iloc[0, i]
            portfolio.iloc[1, i] = portfolio.iloc[1, i] - 1
        empty_list[i].append(cash_flow)
        new_rates[i] = prepayment_rates[i][1:]
    output = Altered_Cashflows(empty_list, new_rates, portfolio)
    return output


# This function computes the total cashflows for the entire portfolio for given cashflows per mortgage
def Total_Altered_Cashflows(cash_flows):
    result = []
    for i in range(120):
        cash_flow = 0
        for j in range(6):
            if len(cash_flows[j]) > i:
                cash_flow += cash_flows[j][i]
        result.append(cash_flow)
    return result


# This function caculates the value of the portfolio when prepayment is involved
def Altered_Value(cash_flows, interest_rates):
    total_value = []
    for j in range(120):
        addition = cash_flows[120 - j - 1] / (1 + ((interest_rates[120 - j - 1] + 0.015) / 12))
        if j > 0:
            addition += total_value[j - 1] / (1 + ((interest_rates[120 - j - 1] + 0.015) / 12))
        total_value.append(addition)
    total_value.reverse()
    return total_value


# This function returns all npv for a zcb hedge portfolio for a given simulation
# Input: positions = zcb positions in the hedge portfolios for all 120 maturities, interest_rates = simulated interest_rates.
def zcb_total_value(positions, interest_rates):
    T = len(interest_rates)
    values = []
    for t in range(T):
        value = positions[120 - t - 1]/(1 + (interest_rates[120 - t -1]/12))
        if t > 0:
            value += values[t - 1]/(1 + (interest_rates[120 - t -1]/12))
        values.append(value)
    values.reverse()
    return values

def compute_margin_differences(desired_cashflows, simulated_cashflows, optimal_x):
    differences = []
    for i in range(len(simulated_cashflows)):
        list = [ round(desired_cashflows[j] - optimal_x[j] - simulated_cashflows[i][j]) for j in range(len(simulated_cashflows[i]))]
        differences.append(list)
    return differences