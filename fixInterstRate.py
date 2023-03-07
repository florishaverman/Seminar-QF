from prepayment import loadINGData, probPrepayment
from interestRate import simulationHullWhite
import Objective_Function_Methods as ofm
import HullWhiteMethods as hw
import pickle  # To save logistic model, to avoid training each time.
import Hedge_Quinten as hq
from scipy.optimize import minimize
import xlsxwriter

data = loadINGData('Current Mortgage portfolio')
data.drop(['Variable'], inplace=True, axis=1)
data.drop([3], inplace=True)
data.iloc[1] = data.iloc[1] * 12
current_euribor = loadINGData('Current Euribor Swap Rates')
prepayment_model = pickle.load(open('prepayment_model.sav', 'rb'))

alpha = 0.15
sigma = 0.02663
current_euribor = current_euribor.loc[:, 'Swap rate']
popt = hw.curve_parameters(current_euribor)
r_zero = current_euribor[0]
n_steps = 100
T = 120
# simulate interest rates
sim = []
for i in range(10):
    interest_rates = simulationHullWhite(alpha, sigma, popt, r_zero, n_steps, T)
    sim.append(interest_rates)

months = [i + 1 for i in range(T)]
wb = xlsxwriter.Workbook('New rates2' + '.xlsx')
ws = wb.add_worksheet('Simulated Interest Rates')
runs = [i + 1 for i in range(len(sim))]
ws.write('A1', 'Months/Runs')
ws.write_row('B1', runs)
ws.write_column('A2', months)
count_col = 1
for rate in sim:
    ws.write_column(1, count_col, rate)
    count_col += 1
wb.close()


