import numpy as np
from scipy.stats import norm
import evaluation

# Define the Hull-White model parameters
mean_reversion_speed = 0.1
volatility = 0.2
initial_rate = 0.05
time_horizon = 1
num_time_steps = 100
dt = time_horizon / num_time_steps
risk_free_rate = 0.02

# Generate the Brownian motion increments
dw = np.random.normal(0, np.sqrt(dt), num_time_steps)

# Define the time grid
t = np.linspace(0, time_horizon, num_time_steps+1)

# Initialize the interest rate array
r = np.zeros(num_time_steps+1)
r[0] = initial_rate

# Compute the interest rate path using the Euler-Maruyama method
for i in range(num_time_steps):
    r[i+1] = r[i] + mean_reversion_speed * (initial_rate - r[i]) * dt + \
             volatility * np.sqrt(r[i]) * dw[i] - \
             0.5 * volatility**2 * r[i] * dt
    
# Compute the discount factor path
discount_factors = np.exp(-risk_free_rate * t)

# Generate a simulated short rate path using the Hull-White model
short_rate_path = np.zeros(num_time_steps+1)
short_rate_path[0] = initial_rate

for i in range(1, num_time_steps+1):
    drift = mean_reversion_speed * (initial_rate - short_rate_path[i-1]) * dt
    vol = volatility * np.sqrt(short_rate_path[i-1]) * np.sqrt(dt)
    diffusion = vol * norm.rvs(size=1)
    short_rate_path[i] = short_rate_path[i-1] + drift + diffusion
    
# Compute the discount factor path for the simulated short rate path
simulated_discount_factors = np.exp(-short_rate_path * t)

# Compute the present value of a bond with face value 1 and maturity time_horizon
bond_price = np.sum(discount_factors * r) * dt

# Compute the present value of a bond with face value 1 and maturity time_horizon for the simulated short rate path
simulated_bond_price = np.sum(simulated_discount_factors * r) * dt

print("The present value of a bond with face value 1 and maturity {} is {:.4f}".format(time_horizon, bond_price))
print("The simulated present value of a bond with face value 1 and maturity {} is {:.4f}".format(time_horizon, simulated_bond_price))
