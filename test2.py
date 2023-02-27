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

data = loadINGData('Current Mortgage portfolio')
data.drop(['Variable'], inplace=True, axis=1)
data.drop([3], inplace=True)
data.iloc[1] = data.iloc[1] * 12
current_euribor = loadINGData('Current Euribor Swap Rates')
# prepayment_model = pickle.load(open('prepayment_model.sav', 'rb'))

desired_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\SimulatedCFnRates.xlsx', sheet_name='Desired CF')
cf_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\SimulatedCFnRates.xlsx', sheet_name='Simulated CF')
rates_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\SimulatedCFnRates.xlsx', sheet_name='Simulated Interest Rates')
desired_cashflows = []
simulated_cashflows = []
simulated_rates = []
for i in range(desired_df.shape[0]):
    desired_cashflows.append(desired_df.iloc[i, 1])
for i in range(cf_df.shape[1]-1):
    sim_cf = []
    sim_rates = []
    for j in range(cf_df.shape[0]):
        sim_cf.append(cf_df.iloc[j, i+1])
        sim_rates.append(rates_df.iloc[j, i+1])
    simulated_cashflows.append(sim_cf)
    simulated_rates.append(sim_rates)

desired_cashflows = ofm.Compute_Cashflows_Exclusive_Edition(data)
#simulated_cashflows, simulated_interest_rates = hq.generate_multiple_cashflows(data, current_euribor, prepayment_model, 1.5, 0.2336, 100, 120, 100)
#oc.writeCashflows('SimulatedCFnRates', desired_cashflows, simulated_cashflows, simulated_interest_rates)
optimal_x = hq.zcb_margin_optimization(desired_cashflows, simulated_cashflows)
#altered_value = ofm.Altered_Value(simulated_cashflows[0], simulated_interest_rates[0])
#altered_value2 = ofm.Altered_Value(simulated_cashflows[1], simulated_interest_rates[1])
#optimal_x2 = hq.zcb_mean_margin_optimization(desired_cashflows, simulated_cashflows)
#difference = [optimal_x[i]-optimal_x2[i] for i in range(len(optimal_x))]
differences = ofm.compute_margin_differences(desired_cashflows, simulated_cashflows, optimal_x)
#print(difference)
#desired_values = ofm.Compute_Time_Values(data)
#optimal_x3 = hq.zcb_value_optimization(desired_values, simulated_rates, simulated_cashflows)
#optimal_x4 = hq.elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_rates, 0.1)
#optimal_x5 = hq.elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_rates, 0.25)
#optimal_x6 = hq.elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_rates, 0.5)
#optimal_x7 = hq.elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_rates, 0.75)
#optimal_x8 = hq.elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_rates, 0.9)
#maturities = []
#type_instr = ['zcb']
#for i in range(120):
#    maturities.append(i + 1)
#oc.writeHedge('zcb margin hedge', optimal_x, maturities, type_instr)
#oc.writeHedge('zcb mean margin hedge', optimal_x2, maturities, type_instr)
#oc.writeHedge('zcb value hedge', optimal_x3, maturities, type_instr)
#oc.writeHedge('zcb elastic 0.1 hedge', optimal_x4, maturities, type_instr)
#oc.writeHedge('zcb elastic 0.25 hedge', optimal_x5, maturities, type_instr)
#oc.writeHedge('zcb elastic 0.5 hedge', optimal_x6, maturities, type_instr)
#oc.writeHedge('zcb elastic 0.75 hedge', optimal_x7, maturities, type_instr)
#oc.writeHedge('zcb elastic 0.9 hedge', optimal_x8, maturities, type_instr)
#print(optimal_x)
#test = ofm.zcb_total_value(optimal_x, simulated_interest_rates[0])
#test2 = ofm.Altered_Value(simulated_cashflows[0], simulated_interest_rates[0])
#test3 = [sum(x) for x in zip(test, test2)]
#difference = [test3[i] - desired_values[i] for i in range(len(test3))]
#print(difference)
#test = ofm.zcb_total_value(test, simulated_interest_rates[0])
#print(simulated_interest_rates[0])
#print(test)
test3 = [100 for _ in range(120)]
test = hd.create_swaptions(120, 0.02829)
test2 = hq.swaption_elastic_objective(test3, differences, simulated_rates, test, 0.75)
print(test2)