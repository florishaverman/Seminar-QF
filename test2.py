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
#prepayment_model = pickle.load(open('prepayment_model.sav', 'rb'))
#simulated_cashflows, simulated_rates, prepayments = hq.generate_multiple_cashflows(data, current_euribor, prepayment_model, 0.15, 0.02663, 100, 120, 100)
#desired_cashflows = ofm.Compute_Cashflows_Exclusive_Edition(data)
#oc.writeCashflows('SimulatedCFnRates', desired_cashflows, simulated_cashflows, simulated_rates)
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
desired_values = ofm.compute_desired_values_exclusive_edition(desired_cashflows)

#maturities = []
#type_instr = ['zcb']

#maturities = [i + 1 for i in range(120)]

#zcb_margin = hq.zcb_margin_optimization(desired_cashflows, simulated_cashflows)
#zcb_value = hq.zcb_value_optimization(desired_values, simulated_rates, simulated_cashflows, zcb_margin)
#zcb_10 = hq.elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_rates, 0.1, zcb_margin)
#zcb_25 = hq.elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_rates, 0.25, zcb_margin)
#zcb_50 = hq.elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_rates, 0.5, zcb_margin)
#zcb_75 = hq.elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_rates, 0.75, zcb_margin)
#zcb_90 = hq.elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_rates, 0.9, zcb_margin)
#oc.writeHedge('zcb margin hedge', zcb_margin, maturities, type_instr)
#oc.writeHedge('zcb value hedge', zcb_value, maturities, type_instr)
#oc.writeHedge('zcb elastic 0.1 hedge', zcb_10, maturities, type_instr)
#oc.writeHedge('zcb elastic 0.25 hedge', zcb_25, maturities, type_instr)
#oc.writeHedge('zcb elastic 0.5 hedge', zcb_50, maturities, type_instr)
#oc.writeHedge('zcb elastic 0.75 hedge', zcb_75, maturities, type_instr)
#oc.writeHedge('zcb elastic 0.9 hedge', zcb_90, maturities, type_instr)

zcb_margin_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\zcb margin hedge.xlsx', sheet_name='Hedge with zcb')
zcb_value_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\zcb value hedge.xlsx', sheet_name='Hedge with zcb')
zcb_10_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\zcb elastic 0.1 hedge.xlsx', sheet_name='Hedge with zcb')
zcb_25_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\zcb elastic 0.25 hedge.xlsx', sheet_name='Hedge with zcb')
zcb_50_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\zcb elastic 0.5 hedge.xlsx', sheet_name='Hedge with zcb')
zcb_75_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\zcb elastic 0.75 hedge.xlsx', sheet_name='Hedge with zcb')
zcb_90_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\zcb elastic 0.9 hedge.xlsx', sheet_name='Hedge with zcb')
#swaption_margin_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\swaption margin hedge.xlsx', sheet_name='Hedge with swaption')
#swaption_value_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\swaption value hedge.xlsx', sheet_name='Hedge with swaption')
#swaption_10_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\swaption elastic 0.1 hedge.xlsx', sheet_name='Hedge with swaption')
#swaption_50_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\swaption elastic 0.5 hedge.xlsx', sheet_name='Hedge with swaption')
#swaption_75_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\swaption elastic 0.75 hedge.xlsx', sheet_name='Hedge with swaption')
#swaption_90_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\swaption elastic 0.9 hedge.xlsx', sheet_name='Hedge with swaption')
zcb_margin = []
zcb_value = []
zcb_10 = []
zcb_25 = []
zcb_50 = []
zcb_75 = []
zcb_90 = []
#swaption_margin = []
#swaption_value = []
#swaption_10 = []
#swaption_50 = []
#swaption_75 = []
#swaption_90 = []
for i in range(zcb_value_df.shape[0]):
    zcb_margin.append(zcb_margin_df.iloc[i,1])
    zcb_value.append(zcb_value_df.iloc[i,1])
    zcb_10.append(zcb_10_df.iloc[i,1])
    zcb_25.append(zcb_25_df.iloc[i,1])
    zcb_50.append(zcb_50_df.iloc[i,1])
    zcb_75.append(zcb_75_df.iloc[i,1])
    zcb_90.append(zcb_90_df.iloc[i,1])
#for i in range(swaption_margin_df.shape[0]):
#    swaption_margin.append(swaption_margin_df.iloc[i,1])
#    swaption_value.append(swaption_value_df.iloc[i,1])
#    swaption_10.append(swaption_10_df.iloc[i,1])
#    swaption_50.append(swaption_50_df.iloc[i,1])
#    swaption_75.append(swaption_75_df.iloc[i,1])
#    swaption_90.append(swaption_90_df.iloc[i,1])
type_instr = ['swaption']
maturities = []
simulated_values = []
for r in range(100):
   sim_val = ofm.Altered_Value(simulated_cashflows[r], simulated_rates[r])
   simulated_values.append(sim_val)
zcb_margin_differences = ofm.compute_margin_differences(desired_cashflows, simulated_cashflows, zcb_margin)
zcb_value_differences = ofm.compute_value_differences(simulated_cashflows, simulated_rates, desired_values, zcb_value)
zcb_10_margin_differences = ofm.compute_margin_differences(desired_cashflows, simulated_cashflows, zcb_10)
zcb_10_value_differences = ofm.compute_value_differences(simulated_cashflows, simulated_rates, desired_values, zcb_10)
zcb_25_margin_differences = ofm.compute_margin_differences(desired_cashflows, simulated_cashflows, zcb_25)
zcb_25_value_differences = ofm.compute_value_differences(simulated_cashflows, simulated_rates, desired_values, zcb_25)
zcb_50_margin_differences = ofm.compute_margin_differences(desired_cashflows, simulated_cashflows, zcb_50)
zcb_50_value_differences = ofm.compute_value_differences(simulated_cashflows, simulated_rates, desired_values, zcb_50)
zcb_75_margin_differences = ofm.compute_margin_differences(desired_cashflows, simulated_cashflows, zcb_75)
zcb_75_value_differences = ofm.compute_value_differences(simulated_cashflows, simulated_rates, desired_values, zcb_75)
zcb_90_margin_differences = ofm.compute_margin_differences(desired_cashflows, simulated_cashflows, zcb_90)
zcb_90_value_differences = ofm.compute_value_differences(simulated_cashflows, simulated_rates, desired_values, zcb_90)
swaptions = hd.create_swaptions(data)
swaption_margin = hq.swaption_margin_optimization(zcb_margin_differences, simulated_rates, swaptions, zcb_margin)
oc.writeHedge('swaption margin hedge same coupon yearly', swaption_margin, maturities, type_instr)
swaption_value = hq. swaption_elastic_optimization(zcb_margin_differences, zcb_value_differences, simulated_rates, swaptions, 0, zcb_value, swaption_margin)
oc.writeHedge('swaption value same coupon yearly', swaption_value, maturities, type_instr)
swaption_10 = hq. swaption_elastic_optimization(zcb_10_margin_differences, zcb_10_value_differences, simulated_rates, swaptions, 0.1, zcb_10, swaption_margin)
oc.writeHedge('swaption elastic 0.1 same coupon yearly', swaption_10, maturities, type_instr)
swaption_10 = hq. swaption_elastic_optimization(zcb_25_margin_differences, zcb_25_value_differences, simulated_rates, swaptions, 0.25, zcb_25, swaption_margin)
oc.writeHedge('swaption elastic 0.25 same coupon yearly', swaption_10, maturities, type_instr)
swaption_50 = hq. swaption_elastic_optimization(zcb_50_margin_differences, zcb_50_value_differences, simulated_rates, swaptions, 0.5, zcb_50, swaption_margin)
oc.writeHedge('swaption elastic 0.5 same coupon yearly', swaption_50, maturities, type_instr)
swaption_75 = hq. swaption_elastic_optimization(zcb_75_margin_differences, zcb_75_value_differences, simulated_rates, swaptions, 0.75, zcb_75, swaption_margin)
oc.writeHedge('swaption elastic 0.75 same coupon yearly', swaption_75, maturities, type_instr)
swaption_90 = hq. swaption_elastic_optimization(zcb_90_margin_differences, zcb_90_value_differences, simulated_rates, swaptions, 0.9, zcb_90, swaption_margin)
oc.writeHedge('swaption elastic 0.9 same coupon yearly', swaption_90, maturities, type_instr)