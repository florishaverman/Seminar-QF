from prepayment import loadINGData, probPrepayment
from interestRate import simulationHullWhite
import HullWhiteMethods as hw
import pickle  # To save logistic model, to avoid training each time.

# Mortgage information
data = loadINGData('Current Mortgage portfolio')
data = data.drop('Variable', axis=1)
margin = data.loc[4, 1]
notional = data.loc[0]
FIRP = data.loc[1]*12  # In months
coupon_rate = data.loc[2]

# Forward curve parameters used in theta
current_euribor = loadINGData('Current Euribor Swap Rates')
current_euribor = current_euribor.loc[:, 'Swap rate']
popt = hw.curve_parameters(current_euribor)

# Parameters as input for Hull-White
# Obtained from swaption data
alpha = 1  # = kappa
sigma = 1
r_zero = 1
delta = 100
T = 120


# Simulate cashflows large number of times
R = 1
prepayment_model = pickle.load(open('prepayment_model.sav', 'rb'))
# Store all simulated cashflows
sim_cashflows = []
for r in range(R):
    # Here we obtain a list of simulated interest rates under Hull-White
    # should theta vary over time?
    interest_rates = simulationHullWhite(alpha, sigma, popt, r_zero, delta, T)
    # Determine the swap rates up to last tenor


    # Here we determine the incentive for each period and for each mortgage
    cashflows = []
    for i in range(0, len(notional)):
        prepay_rate, cashflows_mortgage = [], []
        while FIRP[i] > 0 and notional[i] > 0:  # for FIRP:must include zero or not?
            curr_swap = 3  # fix this later, must go over time as well here
            ref_rate = curr_swap + margin
            incentive = coupon_rate[i] - ref_rate
            # Obtain prepayment rate from prepayment model
            prepay_rate_mortgage = probPrepayment(prepayment_model, incentive)
            prepay_rate.append(prepay_rate_mortgage)
            # Generate cashflow for each mortgage
            cashflows_mortgage.append(prepay_rate_mortgage * notional[i])

            # Here update notional, FIRP
            notional[i] = notional[i] - cashflows_mortgage[-1]
            FIRP[i] = FIRP[i] - 1
        # Add to all cashflows of this simulation
        cashflows.append(cashflows_mortgage)
    # Append this simulation run to all simulated cashflows
    sim_cashflows.append(cashflows)

print(sim_cashflows)

