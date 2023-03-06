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
#current_euribor = loadINGData('Current Euribor Swap Rates')
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

maturities = []
type_instr = ['zcb']
#maturities = [24, 36, 60, 84, 96, 120]
maturities = [i + 1 for i in range(120)]

zcb_margin = hq.zcb_margin_optimization(desired_cashflows, simulated_cashflows)
zcb_value = hq.zcb_value_optimization(desired_values, simulated_rates, simulated_cashflows, zcb_margin)
zcb_10_elastic = hq.elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_rates, 0.1, zcb_margin)
zcb_25_elastic = hq.elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_rates, 0.25, zcb_margin)
zcb_50_elastic = hq.elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_rates, 0.5, zcb_margin)
zcb_75_elastic = hq.elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_rates, 0.75, zcb_margin)
zcb_90_elastic = hq.elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_rates, 0.9, zcb_margin)
oc.writeHedge('zcb margin hedge', zcb_margin, maturities, type_instr)
oc.writeHedge('zcb value hedge', zcb_value, maturities, type_instr)
oc.writeHedge('zcb elastic 0.1 hedge', zcb_10_elastic, maturities, type_instr)
oc.writeHedge('zcb elastic 0.25 hedge', zcb_25_elastic, maturities, type_instr)
oc.writeHedge('zcb elastic 0.5 hedge', zcb_50_elastic, maturities, type_instr)
oc.writeHedge('zcb elastic 0.75 hedge', zcb_75_elastic, maturities, type_instr)
oc.writeHedge('zcb elastic 0.9 hedge', zcb_90_elastic, maturities, type_instr)

#zcb_margin_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\zcb margin hedge.xlsx', sheet_name='Hedge withzcb')
#zcb_value_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\zcb value hedge.xlsx', sheet_name='Hedge withzcb')
#zcb_10_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\zcb elastic 0.1 hedge.xlsx', sheet_name='Hedge withzcb')
#zcb_50_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\zcb elastic 0.5 hedge.xlsx', sheet_name='Hedge withzcb')
#zcb_75_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\zcb elastic 0.75 hedge.xlsx', sheet_name='Hedge withzcb')
#zcb_90_df = pd.read_excel('D:\ING Case\Seminar-QF\Data\zcb elastic 0.9 hedge.xlsx', sheet_name='Hedge withzcb')
#zcb_margin = []
#zcb_value = []
#zcb_10 = []
#zcb_50 = []
#zcb_75 = []
#zcb_90 = []
#for i in range(zcb_margin_df.shape[0]):
#    zcb_margin.append(zcb_margin_df.iloc[i,1])
#    zcb_value.append(zcb_value_df.iloc[i,1])
#    zcb_10.append(zcb_10_df.iloc[i,1])
#    zcb_50.append(zcb_50_df.iloc[i,1])
#    zcb_75.append(zcb_75_df.iloc[i,1])
#    zcb_90.append(zcb_90_df.iloc[i,1])
#zcb_margin_differences = ofm.compute_margin_differences(desired_cashflows, simulated_cashflows, zcb_margin)
#zcb_value_differences = ofm.compute_value_differences(simulated_cashflows, simulated_rates, desired_values, zcb_value)
#zcb_10_margin_differences = ofm.compute_margin_differences(desired_cashflows, simulated_cashflows, zcb_10)
#zcb_10_value_differences = ofm.compute_value_differences(simulated_cashflows, simulated_rates, desired_values, zcb_10)
#zcb_50_margin_differences = ofm.compute_margin_differences(desired_cashflows, simulated_cashflows, zcb_50)
#zcb_50_value_differences = ofm.compute_value_differences(simulated_cashflows, simulated_rates, desired_values, zcb_50)
#zcb_75_margin_differences = ofm.compute_margin_differences(desired_cashflows, simulated_cashflows, zcb_75)
#zcb_75_value_differences = ofm.compute_value_differences(simulated_cashflows, simulated_rates, desired_values, zcb_75)
#zcb_90_margin_differences = ofm.compute_margin_differences(desired_cashflows, simulated_cashflows, zcb_90)
#zcb_90_value_differences = ofm.compute_value_differences(simulated_cashflows, simulated_rates, desired_values, zcb_90)
#swaptions = hd.create_swaptions(data)
#swaption_margin = hq.swaption_margin_optimization(zcb_margin_differences, simulated_rates, swaptions, zcb_margin)
#oc.writeHedge('swaption margin hedge', swaption_margin, maturities, type_instr)
#value_factor = hq.compute_MSE_factor(simulated_cashflows, simulated_rates, desired_cashflows, desired_values, zcb_value)
#swaption_value = hq. swaption_elastic_optimization(zcb_margin_differences, zcb_value_differences, simulated_rates, swaptions, 0, zcb_value, value_factor, swaption_margin)
#.writeHedge('swaption value hedge', swaption_value, maturities, type_instr)
#factor_10 = hq.compute_MSE_factor(simulated_cashflows, simulated_rates, desired_cashflows, desired_values, zcb_10)
#swaption_10 = hq. swaption_elastic_optimization(zcb_10_margin_differences, zcb_10_value_differences, simulated_rates, swaptions, 0.1, zcb_10, factor_10, swaption_margin)
#oc.writeHedge('swaption elastic 0.1 hedge', swaption_10, maturities, type_instr)
#factor_50 = hq.compute_MSE_factor(simulated_cashflows, simulated_rates, desired_cashflows, desired_values, zcb_50)
#swaption_50 = hq. swaption_elastic_optimization(zcb_50_margin_differences, zcb_50_value_differences, simulated_rates, swaptions, 0.5, zcb_50, factor_50, swaption_margin)
#oc.writeHedge('swaption elastic 0.5 hedge', swaption_50, maturities, type_instr)
#factor_75 = hq.compute_MSE_factor(simulated_cashflows, simulated_rates, desired_cashflows, desired_values, zcb_75)
#swaption_75 = hq. swaption_elastic_optimization(zcb_75_margin_differences, zcb_75_value_differences, simulated_rates, swaptions, 0.75, zcb_75, factor_75, swaption_margin)
#oc.writeHedge('swaption elastic 0.75 hedge', swaption_75, maturities, type_instr)
#factor_90 = hq.compute_MSE_factor(simulated_cashflows, simulated_rates, desired_cashflows, desired_values, zcb_90)
#swaption_90 = hq. swaption_elastic_optimization(zcb_90_margin_differences, zcb_90_value_differences, simulated_rates, swaptions, 0.9, zcb_90, factor_90, swaption_margin)
#oc.writeHedge('swaption elastic 0.9 hedge', swaption_90, maturities, type_instr)