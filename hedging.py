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
