from prepayment import loadINGData, probPrepayment
from interestRate import simulationHullWhite
import Objective_Function_Methods as ofm
import HullWhiteMethods as hw
import pickle  # To save logistic model, to avoid training each time.
import Hedge_Quinten as hq
from scipy.optimize import minimize

data = loadINGData('Current Mortgage portfolio')
data.drop(['Variable'], inplace=True, axis=1)
data.drop([3], inplace=True)
data.iloc[1] = data.iloc[1] * 12
current_euribor = loadINGData('Current Euribor Swap Rates')
prepayment_model = pickle.load(open('prepayment_model.sav', 'rb'))

alpha = 1.5
sigma = 0.2663
current_euribor = current_euribor.loc[:, 'Swap rate']
popt = hw.curve_parameters(current_euribor)
r_zero = current_euribor[0]
n_steps = 100
T = 120
# simulate interest rates
sim = []
for i in range(100):
    interest_rates = simulationHullWhite(alpha, sigma, popt, r_zero, n_steps, T)
    sim.append(interest_rates)
for i in sim:
    for j in i:
        print(j)


