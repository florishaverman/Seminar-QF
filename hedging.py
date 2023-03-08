import cashflows

""" Hedging.py is used to construct the instruments used for hedging.
It contains a class Bonds, which represent a bond with zero coupon and with a fixed maturity.



@autor: Floris """


""" 
This class contains of the information of bonds and allows to calculate the cashflows of bonds.
"""
class Bond:
    #A bond is characterized by its maturity
    #A bond is a zero coupon bond by definition
    def __init__(self, maturity):
        self.maturity = maturity
        # self.coupon = coupon
    
    def getCashflows(self):
        cashflow = [0] * (self.maturity-1)
        cashflow.append(1)
        return cashflow
    
    def getCashflowsFixedLength(self, numMonths):
        cashflow = [0] * numMonths
        cashflow[self.maturity - 1] = 1
        return cashflow
    
    def getMaturity(self):
        return self.maturity

#

"""
This fuction creates bonds with maturity from 1 month till maxMaturity
maxMaturity: An integer for the maximum length of the bond, in months

return: an 1D array with bonds randging in maturity from 1 month till maxMaturity
"""
def createHedgingBonds(maxMaturity):
    bonds = []
    for i in range(maxMaturity):
        bonds.append(Bond(i+1))
    return bonds

""" This function calculates the cashflow matrix for given bonds and up to time T
bonds: an 1D array of bonds (of the class Bonds)
T: the amout of months you want the cashflows for

return: A 2D array, where [b][t] is the cashflow of bond b at time t
"""
def getCashflowMatrix(bonds, T):
    C = []
    for bond in bonds:
        C.append(bond.getCashflowsFixedLength(T))
    return C

# m=12
# bonds = createHedgingBonds(m)
# for i in range(m):
#     print(bonds[i].getCashflows())

# print(getCashflowMatrix(bonds, m))


class Swaption:
    # The swaption is characterized by the time of inception t1, maturity t2 and the fixed leg rate (the strike). The floating leg is just the interest rate.
    def __init__(self, t1, t2, strike):
        self.t1 = t1
        self.t2 = t2
        self.strike = strike

    def get_t1(self):
        return self.t1

    def get_t2(self):
        return self.t2

    def get_strike(self):
        return self.strike
    

    # This function computes the cashflows for a swaption as they would happen for a given simulation if the swaption was exercised.
    # Input: self = a swaption object, interest_rates = one interest rate simulation.
    # Output: cashflows for the swaption in case of exercise
    def swaption_cashflows(self, interest_rates):
        t1 = self.t1
        t2 = self.t2
        strike = self.strike
        cashflows = []
        for i in range(120):
            if t1 > i or t2 < i:
                cashflows.append(0)
            else:
                cashflows.append(interest_rates[i] - strike)
        return cashflows


    # This function computes the npv for every t of a given interest rate simulation for the cashflows resulting from exercising a swaption
    # Input: self = a swaption object, interest_rates = one sequence of simulated interest rates.
    # Ouput: The computed npv's
    def swaption_value(self, interest_rates):
        cashflows = Swaption.swaption_cashflows(self, interest_rates)
        values = []
        for t in range(120):
            value = cashflows[120 - t - 1]/(1 + (interest_rates[120 - t -1]/12))
            if t > 0:
                value += values[t - 1]/(1 + (interest_rates[120 - t -1]/12))
            values.append(value)
        values.reverse()
        return values

    
def create_swaptions(data):
    swaptions = []
    FIRP = data.iloc[1].tolist()
    coupon = data.iloc[2].tolist()
    for i in range(len(FIRP)):
        swaptions.append(Swaption(0, FIRP[i], coupon[i] - 0.015))
    return swaptions


def total_swaption_cashflows(positions, swaptions, interest_rates):
    cash_flows = []
    for i in range(len(interest_rates)):
        list = [0 for _ in range(120)]
        for s in range(len(swaptions)):
            temp = Swaption.swaption_cashflows(swaptions[s], interest_rates[i])
            list = [list[j] + positions[s] * temp[j] for j in range(120)]
        cash_flows.append(list)
    return cash_flows
