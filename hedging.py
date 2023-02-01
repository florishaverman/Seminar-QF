import cashflows


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
maxMaturit: An integer for the maximum length of the bond, in months
"""
def createHedgingBonds(maxMaturity):
    bonds = []
    for i in range(maxMaturity):
        bonds.append(Bond(i+1))
    return bonds

def getCashflowMatrix(bonds, m):
    C = []
    for bond in bonds:
        C.append(bond.getCashflowsFixedLength(m))
    return C

# m=12
# bonds = createHedgingBonds(m)
# for i in range(m):
#     print(bonds[i].getCashflows())

# print(getCashflowMatrix(bonds, m))
