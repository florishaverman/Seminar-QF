from prepayment import loadINGData, probPrepayment
from interestRate import simulationHullWhite
import Objective_Function_Methods as ofm
import HullWhiteMethods as hw
import pickle  # To save logistic model, to avoid training each time.
import hedging as h
from scipy.optimize import minimize
from time import process_time


# Ik heb het cashflow_generator script even in een functie gezet om het makkelijker te maken qua gebruik
# Het doet precies wat het cashflow_generator script doet maar dan voor maar één iteratie.
# Input: data = mortgage portfolio data in mijn vorm (alleen notional, FIRP, coupon en margin, een 4x6 dataframe),
# current euribor = the sequence uit de current euribor sheet, prepayment model = al ingelaadde model van Floris, 
# (alpha, sigma) = hull-white parameters, n_steps = het aantal stappen dat in een maand wordt gesimuleerd via hull-white,
# T = de maximale FIRP. 
# Output: Een lijst met 120 cashflows, 1 voor elke maand.
def generate_cashflows(data, current_euribor, prepayment_model, alpha, sigma, n_steps, T):
    margin = data.iloc[3, 1]
    FIRP = data.iloc[1].tolist()  # In months
    coupon_rate = data.iloc[2].tolist()
    current_euribor = current_euribor.loc[:, 'Swap rate']
    popt = hw.curve_parameters(current_euribor)
    prepay_rate = [[] for _ in range(6)]

    # Here we obtain a list of simulated interest rates under Hull-White
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
    sc = ofm.Altered_Cashflows([[] for _ in range(6)], prepay_rate, data)
    simulated_cashflows = ofm.Total_Altered_Cashflows(sc)
    return simulated_cashflows, interest_rates


# Ik heb even een aparte functie gemaakt om generate_cashflows te loopen, omdat dat even wat overzichtelijker was
# voor mezelf qua het cashflow generator script omschrijven tot een functie.
# Input: R = Aantal cashflow simulaties. Voor de rest zie generate_cashflows.
# Output: Een lijst van R lijsten met cashflows. Elke lijst met cashflows beslaat één simulatie.
def generate_multiple_cashflows(data, current_euribor, prepayment_model, alpha, sigma, n_steps, T, R):
    sim_cashflow_array = [[] for _ in range(R)]
    sim_interest_rate_array = [[] for _ in range(R)]
    for i in range(R):
        sim_cashflow_array[i], sim_interest_rate_array[i] = generate_cashflows(data, current_euribor, prepayment_model, alpha, sigma, n_steps, T)
    return sim_cashflow_array, sim_interest_rate_array


# A function to calculate the objective function for margin stability using just zero coupon bonds. This function is used for the objective function
# where we minimize the average MSE of multiple simulations. The minimization problem can be simplified by computing minimizing it per month,
# so by creating 120 smaller optimization problems. This function thus computes the average MSE for a single month over multiple simulations.
# Input: hedge_cashflow = the cashflow in this month resulting from the hedging portfolio, required_cashflow = the cashflow that would take place this 
# month if no prepayment would ever take place, sim_cashflows = the cashflows that take place in this month in the different simulations.
# Output: The computed MSE
def zcb_margin_objective(hedge_cashflow, required_cashflow, sim_cashflows):
    MSE = 0
    R = len(sim_cashflows)
    for i in range(R):
        MSE += (required_cashflow - sim_cashflows[i] - hedge_cashflow)**2
    return MSE/R


# This function minimizes the average MSE over R different simulations for all 120 months using just zero coupon bonds with the assumption we have bonds for every maturity.
# Input: desired_cashflows = a list of all 120 cash_flows as they would occur if no prepayment took place, 
# simulated_cashflows = a list of R lists, which all contain the 120 cashflows resulting from a single simulation.
# Output: A list of bond positions for all 120 maturities, that optimizes the hedge.
def zcb_margin_optimization(desired_cashflows, simulated_cashflows):
    t1 = process_time()
    result = []
    # For every time t create the correct input for monthly optimization
    for t in range(len(desired_cashflows)):
        required_cashflow = desired_cashflows[t]
        sim_cashflows = []
        # For every month we loop over every simulation to get the corresponding cahsflow for that month
        for i in range(len(simulated_cashflows)):
            sim_cashflows.append(simulated_cashflows[i][t])
        x0 = 10000
        # Minimize the objective function
        opt_monthly_bonds = minimize(zcb_margin_objective, x0, args=(required_cashflow, sim_cashflows))
        # Store the results
        result.append(opt_monthly_bonds.x[0])
    t2 = process_time()
    # Time the process and show its duration
    print('optimization took ', t2-t1, ' seconds in total')
    return result


# This function computes the optimal hedge portfolio consisting of only zero coupon bond for Floris' method, which results in creating bond positions
# equal to the average deviation from the simulations in comparison to the desired cashflows.
# Input and output: See zcp_margin_optimization.
def zcb_mean_margin_optimization(desired_cashflows, simulated_cashflows):
    result = []
    t1 = process_time()
    # optimize the hedge for every month
    for t in range(len(desired_cashflows)):
        required_cashflow = desired_cashflows[t]
        value = 0
        # comput the average deviation from the desired cashflow
        for i in range(len(simulated_cashflows)):
            value += required_cashflow - simulated_cashflows[i][t]
        value = value/len(simulated_cashflows)
        result.append(value)
    t2 = process_time()
    print('optimization took ', t2-t1, ' seconds in total')
    return result


# This function computes the value MSE for a given hedge portfolio consisting of only zcb.
# Input: positions = zcb positions of the hedgin portfolio, desired_values = the npv's we try to achieve,
# simulated_values = the npv's resulting from the simulated interest rates and prepayment rates for al R simulations,
# simulated_interest_rates = the simulated interest rates for all R simulations.
# Ouptput: The computed MSE
def zcb_value_objective(positions, desired_values, simulated_values, simulated_interest_rates):
    T = len(desired_values)
    R = len(simulated_interest_rates)
    hedge_values = []
    # Compute the hedge portfolio npv's under the different simulations
    for r in range(R):
        values = ofm.zcb_total_value(positions, simulated_interest_rates[r])
        hedge_values.append(values)
    value_MSE = 0
    # Compute the MSE
    for r in range(R):
        for t in range(T):
            value_MSE += (1/(R*T))*((desired_values[t] - simulated_values[r][t] - hedge_values[r][t])**2)
    return value_MSE


# This function optimizes a zcb hedge portfolio for margin stability.
# Input: See zcb_value_objective. Output: The optimal hedge portfolio for value stability.
def zcb_value_optimization(desired_values, simulated_interest_rates, simulated_cashflows):
    t1 = process_time()
    R = len(simulated_interest_rates)
    simulated_values = []
    for r in range(R):
        sim_val = ofm.Altered_Value(simulated_cashflows[r], simulated_interest_rates[r])
        simulated_values.append(sim_val)
    x0 = [10000 for _ in range(120)]
    opt_monthly_bonds = minimize(zcb_value_objective, x0, args=(desired_values, simulated_values, simulated_interest_rates))
    t2 = process_time()
    print('optimization took ', t2-t1, ' seconds in total')
    return opt_monthly_bonds.x


# This function computes the elsastic net type objective function for a hedge consisting og just zcb.
# Input: positions = the zcb positions in the hedge, desired_cashflows = the cashflows we want to achieve,
# simulated_cashflows = the simulated cashflows of all R simulations, desired_values = the npv's we want to achieve,
# simulated_values = the npv's of the mortgage portfolios under all R simulations, simulated_interest_rates = the simulated interest
# rates for all R simulations, alpha = the alpha in the elastic net objective function.
# Output: The MSE resulting from a given hedge portfolio for the elastic net objective function.
def elastic_zcb_objective(positions, desired_cashflows, simulated_cashflows, desired_values, simulated_values, simulated_interest_rates, alpha):
    MSE_value = zcb_value_objective(positions, desired_values, simulated_values, simulated_interest_rates)
    R = len(simulated_interest_rates)
    T = len(desired_cashflows)
    MSE_margin = 0
    for t in range(T):
        required_cashflow = desired_cashflows[t]
        sim_cashflows = []
        for r in range(R):
            sim_cashflows.append(simulated_cashflows[r][t])
        MSE_margin += zcb_margin_objective(positions[t], required_cashflow, sim_cashflows)
    MSE_elastic = alpha * MSE_margin + (1 - alpha) * MSE_value
    return MSE_elastic


# This function optimizes the elastic net objective function for solely zcb for a chosen alpha.
def elastic_zcb_optimization(desired_cashflows, simulated_cashflows, desired_values, simulated_interest_rates, alpha):
    t1 = process_time()
    R = len(simulated_interest_rates)
    simulated_values = []
    for r in range(R):
        sim_val = ofm.Altered_Value(simulated_cashflows[r], simulated_interest_rates[r])
        simulated_values.append(sim_val)
    x0 = [10000 for _ in range(120)]
    opt_monthly_bonds = minimize(elastic_zcb_objective, x0, args=(desired_cashflows, simulated_cashflows, desired_values, simulated_values, simulated_interest_rates, alpha))
    t2 = process_time()
    print('optimization took ', t2-t1, ' seconds in total')
    return opt_monthly_bonds.x


# A function that calculates the margin stability MSE for a hedge of swaptions.
# Input: deviating_cashflows = the not yet hedged difference between achieved cashflows and desired cashflows,
# interest_rates = a list of R sequences of simulated interest_rates, swaptions = a list of swaption objects (all have notional 1),
# positions = the position taken in the swaption. (has to be >= 0)
# Output: The computed MSE
def swaption_margin_objective(positions, deviating_cashflows, interest_rates, swaptions):
    value = 0
    s = len(swaption)
    for sequence in interest_rates:
        for swaption in range(s):
            temp = 0
            temp2 = 0
            # Compute the cashflows per simulation per swaption if the swaption is exercised
            possible_cashflows = h.Swaption.swaption_cashflows(swaptions[s], sequence)
            for t in range(120):
                # The MSE is computed both for the case where the swaption is excercised as well when it is not
                temp += (deviating_cashflows[t] - positions[s]*possible_cashflows[t])**2
                temp2 += deviating_cashflows[t]**2
            # If the MSE is smaller when exercised, the swaption is exercised, otherwise not
            if temp <= temp2:
                value += temp
            else:
                value += temp2
    return value


# This function optimizes a swaption hedge on margin stability for a given set of swaptions.
# Input: deviating_cashflows = the yet to be hedged difference between desired and achieved cashflows,
# interest_rates = a list of R sequences of simulated interest_rates, swaptions = a list of swaption objects (all have notional 1).
# Output: The optimal positions for a margin stability hedge.
def swaption_margin_optimization(deviating_cashflows, interest_rates, swaptions):
    t1 = process_time()
    s = len(swaptions)
    x0 = [0 for _ in s]
    opt_swaptions = minimize(swaption_margin_objective, x0, args=(deviating_cashflows, interest_rates, swaptions))
    t2 = process_time()
    print('optimization took ', t2-t1, ' seconds in total')
    return opt_swaptions


def swaption_value_objective(positions, deviating_cashflows, interest_rates, swaptions):
    value = 0
    s = len(swaption)
    for sequence in interest_rates:
        for swaption in range(s):
            temp = 0
            temp2 = 0
            # Compute the cashflows per simulation per swaption if the swaption is exercised
            possible_values = h.Swaption.swaption_value(swaptions[s], sequence)
            for t in range(120):
                # The MSE is computed both for the case where the swaption is excercised as well when it is not
                temp += (deviating_cashflows[t] - positions[s]*possible_values[t])**2
                temp2 += deviating_cashflows[t]**2
            # If the MSE is smaller when exercised, the swaption is exercised, otherwise not
            if temp <= temp2:
                value += temp
            else:
                value += temp2
    return value


def swaption_value_optimization(deviating_cashflows, interest_rates, swaptions):
    t1 = process_time()
    s = len(swaptions)
    x0 = [0 for _ in s]
    opt_swaptions = minimize(swaption_value_objective, x0, args=(deviating_cashflows, interest_rates, swaptions))
    t2 = process_time()
    print('optimization took ', t2-t1, ' seconds in total')
    return opt_swaptions


def swaption_elastic_objective(positions, deviating_cashflows, interest_rates, swaptions, alpha):
    MSE_margin = swaption_margin_objective(positions, deviating_cashflows, interest_rates)
    MSE_value = swaption_value_objective(positions, deviating_cashflows, interest_rates, swaptions)
    MSE_elastic = alpha * MSE_margin + (1 - alpha) * MSE_value
    return MSE_elastic


def swaption_elastic_optimization(deviating_cashflows, interest_rates, swaptions, alpha):
    t1 = process_time()
    s = len(swaptions)
    x0 = [0 for _ in s]
    opt_swaptions = minimize(swaption_elastic_objective, x0, args=(deviating_cashflows, interest_rates, swaptions, alpha))
    t2 = process_time()
    print('optimization took ', t2-t1, ' seconds in total')
    return opt_swaptions