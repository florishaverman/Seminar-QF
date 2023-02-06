from prepayment import loadINGData, probPrepayment
from interestRate import simulationHullWhite
from Objective_Function_Methods import Altered_Cashflows, Total_Altered_Cashflows
import HullWhiteMethods as hw
import pickle  # To save logistic model, to avoid training each time.
import hedging
from scipy.optimize import minimize


# Ik heb het cashflow_generator script even in een functie gezet om het makkelijker te maken qua gebruik
def generate_cashflows(data, current_euribor, prepayment_model, alpha, sigma, n_steps, T):
    margin = data.iloc[3, 1]
    FIRP = data.iloc[1].tolist()  # In months
    coupon_rate = data.iloc[2].tolist()
    current_euribor = current_euribor.loc[:, 'Swap rate']
    popt = hw.curve_parameters(current_euribor)
    prepay_rate = [[] for _ in range(6)]

    # Here we obtain a list of simulated interest rates under Hull-White
    # should theta vary over time?
    interest_rates = simulationHullWhite(alpha, sigma, popt, current_euribor[0], n_steps, T)
    tenor = T
    while tenor > 0:
        # Determine the swap rates up to last tenor by approximating bond prices
        bond_price, swap_rates = [], []
        sum_bond_price = 0
        step_length_swap = 1 / 12
        for t in range(tenor):
            bp = hw.bondPrice(4, alpha, 1, sigma, interest_rates[T - tenor], *popt)
            bond_price.append(bp)
            sum_bond_price += bp
            sr = (1 - bp) / (step_length_swap * sum_bond_price)
            swap_rates.append(sr)

        # Determine prepayment rate per mortgage
        for i in range(6):
            if FIRP[i] > 0:
                ref_rate = swap_rates[FIRP[i] - 1] + margin
                incentive = coupon_rate[i] - ref_rate
                prepay_rate_mortgage = probPrepayment(prepayment_model, incentive)
                prepay_rate[i].append(prepay_rate_mortgage[0])
        # Update FIRP and tenor
        FIRP[:] = [f - 1 for f in FIRP]
        tenor -= 1        
    # Generate simulated cashflows based on prepayment rate
    for i in range(120):
        for j in range(6):
            if len(prepay_rate[j]) < i + 1:
                prepay_rate[j].append(0)
    sc = Altered_Cashflows([[] for _ in range(6)], prepay_rate, data)
    simulated_cashflows = Total_Altered_Cashflows(sc)
    return simulated_cashflows


# Ik heb even een aparte functie gemaakt om generate_cashflows te loopen, omdat dat even wat overzichtelijker was
# voor mezelf qua het cashflow generator script omschrijven tot een functie.
def generate_multiple_cashflows(data, current_euribor, prepayment_model, alpha, sigma, n_steps, T, R):
    sim_cashflow_array = [[] for _ in range(R)]
    for i in range(R):
        sim_cashflow_array[i] = generate_cashflows(data, current_euribor, prepayment_model, alpha, sigma, n_steps, T)
    return sim_cashflow_array


# A function to calculate the objective function for margin stability using just zero coupon bonds
def zcb_margin_objective(hedge_cashflow, required_cashflow, sim_cashflows):
    MSE = 0
    for i in range(len(sim_cashflows)):
        MSE += ((required_cashflow - sim_cashflows[i] - hedge_cashflow)/required_cashflow)**2
    return MSE


def zcb_margin_optimization(desired_cashflows, simulated_cashflows):
    print('Starting optimization')
    result = []
    for t in range(len(desired_cashflows)):
        required_cashflow = desired_cashflows[t]
        sim_cashflows = []
        for i in range(len(simulated_cashflows)):
            sim_cashflows.append(simulated_cashflows[i][t])
        x0 = 10000
        opt_monthly_bonds = minimize(zcb_margin_objective, x0, args=(required_cashflow, sim_cashflows))
        result.append(opt_monthly_bonds.x[0])
    print('Finished Optimization')
    return result
