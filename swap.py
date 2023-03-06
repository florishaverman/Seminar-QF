
from Objective_Function_Methods import Altered_Cashflows, Total_Altered_Cashflows
import HullWhiteMethods
import interestRate
import prepayment
import evaluation


current_euribor = prepayment.loadINGData('Current Euribor Swap Rates')
current_euribor = current_euribor.loc[:, 'Swap rate']
popt = HullWhiteMethods.curve_parameters(current_euribor)

alpha = 0.03  # = kappa
sigma = 0.15
r_zero = 0.02
# r_zero = current_euribor[0]
n_steps = 100
T = 120
TT = 10

# # Determine the analytical zero-coupon bond price for Hull-White
# def bondPrice(T, kappa, tau, sigma, r, a, b, c, d):
#     bond_price = exp(A(T, kappa, tau, sigma, a, b, c, d) + B(kappa, tau) * r)
#     return bond_price
price = HullWhiteMethods.bondPrice(2, alpha, 2, sigma, r_zero, popt[0], popt[1], popt[2], popt[3])
# print(price)
prices = []
for i in range(11):
    prices.append(HullWhiteMethods.bondPrice(4, alpha, i, sigma, r_zero, popt[0], popt[1], popt[2], popt[3]))
    print(prices[i])
# evaluation.plotXY( [i for i in range(11)], prices)

# interest_rates = interestRate.simulationHullWhite(alpha, sigma, popt, r_zero, n_steps, T)
# print(interest_rates)