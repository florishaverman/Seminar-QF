from prepayment import loadINGData, probPrepayment
from interestRate import simulationHullWhite
import Objective_Function_Methods as ofm
import HullWhiteMethods as hw
import pickle  # To save logistic model, to avoid training each time.
import Hedge_Quinten as hq
from scipy.optimize import minimize
import pandas as pd
import outputCreation as oc
import hedging as hd
import evaluation as eval

data = loadINGData('Current Mortgage portfolio')
data.drop(['Variable'], inplace=True, axis=1)
data.drop([3], inplace=True)
data.iloc[1] = data.iloc[1] * 12
current_euribor = loadINGData('Current Euribor Swap Rates')
# prepayment_model = pickle.load(open('prepayment_model.sav', 'rb'))
# simulated_cashflows, simulated_rates, prepayments = hq.generate_multiple_cashflows(data, current_euribor, prepayment_model, 0.15, 0.02663, 100, 120, 100)

# desired_cashflows = ofm.Compute_Cashflows_Exclusive_Edition(data)
# oc.writeCashflows('Short rate paths initial rate 0.045', desired_cashflows, simulated_cashflows, simulated_rates)

