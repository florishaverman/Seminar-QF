from prepayment import loadINGData, probPrepayment
from interestRate import simulationHullWhite
from Objective_Function_Methods import Altered_Cashflows
import HullWhiteMethods as hw
import pickle  # To save logistic model, to avoid training each time.

# Mortgage information
data = loadINGData('Current Mortgage portfolio')
data = data.drop('Variable', axis=1)
data.loc[1] = data.loc[1] * 12  # In months
margin = data.loc[4, 1]
notional = data.loc[0].tolist()
FIRP = data.loc[1].tolist()  # In months
coupon_rate = data.loc[2].tolist()

# Forward curve parameters used in theta
current_euribor = loadINGData('Current Euribor Swap Rates')
current_euribor = current_euribor.loc[:, 'Swap rate']
popt = hw.curve_parameters(current_euribor)

# Parameters as input for Hull-White
# Obtained from swaption data
alpha = 1.5  # = kappa
sigma = 0.2633
r_zero = current_euribor[0]
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
    tenor = T
    prepay_rate = [[] for _ in range(6)]
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
                prepay_rate[i].append(prepay_rate_mortgage)
        # Update FIRP and tenor
        FIRP[:] = [f - 1 for f in FIRP]
        tenor -= 1

    # Generate simulated cashflows based on prepayment rate
    sc = Altered_Cashflows([[] for _ in range(6)], prepay_rate, data)
    sim_cashflows.append(sc)
print(sim_cashflows)

