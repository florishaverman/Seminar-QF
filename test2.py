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

simulated_cashflows, simulated_interest_rates = hq.generate_multiple_cashflows(data, current_euribor, prepayment_model, 1.5, 0.2336, 100, 120, 2)
desired_cashflows = ofm.Compute_Cash_Flows(data)
#optimal_x = hq.zcb_margin_optimization(desired_cashflows, simulated_cashflows)
#altered_value = ofm.Altered_Value(simulated_cashflows[0], simulated_interest_rates[0])
#altered_value2 = ofm.Altered_Value(simulated_cashflows[1], simulated_interest_rates[1])
#optimal_x2 = hq.zcb_mean_margin_optimization(desired_cashflows, simulated_cashflows)
#difference = [optimal_x[i]-optimal_x2[i] for i in range(len(optimal_x))]
#print(difference)
desired_values = ofm.Compute_Time_Values(data)
optimal_x = hq.elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_interest_rates, 1)
#optimal_x = hq.zcb_value_optimization(desired_values, simulated_interest_rates, simulated_cashflows)
print(optimal_x)
#test = ofm.zcb_total_value(optimal_x, simulated_interest_rates[0])
#test2 = ofm.Altered_Value(simulated_cashflows[0], simulated_interest_rates[0])
#test3 = [sum(x) for x in zip(test, test2)]
#difference = [test3[i] - desired_values[i] for i in range(len(test3))]
#print(difference)
#test = [10000 for i in range(120)]
#test = ofm.zcb_total_value(test, simulated_interest_rates[0])
#print(simulated_interest_rates[0])
#print(test)