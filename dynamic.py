import Hedge_Quinten as hq
import Objective_Function_Methods as ofm
import hedging as h


def rebalance_boolean(t, desired_cashflows, simulated_cashflows, desired_values, simulated_values, simulated_rates, alpha, zcb_positions, swaption_positions, swaptions, factor):
    desired_cash = [desired_cashflows[i] for i in range(t, 120)]
    desired_val = [desired_values[i] for i in range(t,120)]
    simulated_cash = [[] for _ in range(100)]
    simulated_val = [[] for _ in range(100)]
    sim_rates = [[] for _ in range(100)]
    for j in range(100):
        simulated_cash.append([simulated_cashflows[j][i] for i in range(t, 120)])
        simulated_val.append([simulated_values[j][i] for i in range(t, 120)])
        sim_rates.append([simulated_rates[j][i] for i in range(t, 120)])
    margin_difference = ofm.compute_margin_differences(desired_cash, simulated_cash, zcb_positions)
    value_difference = ofm.compute_value_differences(simulated_cash, sim_rates, desired_val, zcb_positions)
    MSE = hq.swaption_elastic_objective(swaption_positions, margin_difference, value_difference, sim_rates, swaptions, alpha, factor)
    if MSE > 100000000:
        return True
    else:
        return False
    

def run_dynamic_hedge(desired_cashflows, simulated_cashflows, desired_values, simulated_values, simulated_rates, alpha, swaptions):
    zcb_hedges = []
    swaption_hedges = []
    times = [0]
    zcb_optimal = hq.zcb_margin_optimization(desired_cashflows, simulated_cashflows)
    differences = ofm.compute_margin_differences(desired_cashflows, simulated_cashflows, zcb_optimal)
    swaption_optimal = hq.swaption_margin_optimization(differences, simulated_rates, swaptions, zcb_optimal)
    zcb_hedges.append(zcb_optimal)
    swaption_hedges.append(swaption_optimal)
    for t in range(1, 120):
        if rebalance_boolean(t, desired_cashflows, simulated_cashflows, desired_values, simulated_values, simulated_rates, alpha, zcb_hedges[-1], swaption_hedges[-1], swaptions, 1):
            desired_cash = [desired_cashflows[i] for i in range(t, 120)]
            desired_val = [desired_values[i] for i in range(t,120)]
            simulated_cash = [[] for _ in range(100)]
            simulated_val = [[] for _ in range(100)]
            sim_rates = [[] for _ in range(100)]
            for j in range(100):
                simulated_cash.append([simulated_cashflows[j][i] for i in range(t, 120)])
                simulated_val.append([simulated_values[j][i] for i in range(t, 120)])
                sim_rates.append([simulated_rates[j][i] for i in range(t, 120)])
            zcb_optimal = hq.zcb_margin_optimization(desired_cash, simulated_cash)
            differences = ofm.compute_margin_differences(desired_cash, simulated_cash, zcb_optimal)
            swaption_optimal = hq.swaption_margin_optimization(differences, sim_rates, swaptions, zcb_optimal)
            zcb_hedges.append(zcb_optimal)
            swaption_hedges.append(swaption_optimal)
            times.append(t)
    return zcb_hedges, swaption_hedges, times

    
    