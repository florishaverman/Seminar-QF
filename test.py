from prepayment import loadINGData, probPrepayment
from interestRate import simulationHullWhite
import HullWhiteMethods as hw

# Mortgage information
data = loadINGData('Current Mortgage portfolio')
data = data.drop('Variable', axis=1)
margin = data.loc[4, 1]
notional = data.loc[0]
FIRP = data.loc[1]*12  # In months
coupon_rate = data.loc[2]

# Forward curve parameters used in theta
current_euribor = loadINGData('Current Euribor Swap Rates')
current_euribor = current_euribor.loc[:, 'Swap rate']
popt = hw.curve_parameters(current_euribor)

# Parameters as input for Hull-White
# Obtained from swaption data
alpha = 1.5  # = kappa
sigma = 0.2663
r_zero = current_euribor[0]
delta = 100
T = 120

# Here we obtain a list of simulated interest rates under Hull-White
# should theta vary over time?
interest_rates = simulationHullWhite(alpha, sigma, popt, r_zero, delta, T)
# Determine the swap rates up to last tenor by approximating bond prices
tenor = T
bond_price, swap_rates = [], []
sum_bond_price = 0
step_length_swap = 1 / 12
'''
for t in range(1, tenor):
    bp = hw.bondPrice(t, alpha, t, sigma, interest_rates[0], *popt)
    bond_price.append(bp)
    sum_bond_price += bp
    sr = (1 - bp)/(step_length_swap * sum_bond_price)
    swap_rates.append(sr)
print(sum_bond_price)
'''
print(hw.A(2, alpha, 1, sigma, *popt))
print(hw.integral(2, alpha, 1, sigma, *popt))
