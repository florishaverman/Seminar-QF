import QuantLib as ql
import matplotlib.pyplot as plt
import numpy as np
# matplotlib inline

sigma = 0.1
a = 0.1
timestep = 360
length = 30 # in years
forward_rate = 0.05

vasicek = ql.Vasicek(0.05, 0.1, 0.05, 0.01, 0.0)


print('hello world')
print(vasicek.discountBond(0, 1))


day_count = ql.Thirty360()
todays_date = ql.Date(15, 1, 2015)
ql.Settings.instance().evaluationDate = todays_date
spot_curve = ql.FlatForward(todays_date, ql.QuoteHandle(ql.SimpleQuote(forward_rate)), day_count)
spot_curve_handle = ql.YieldTermStructureHandle(spot_curve)
hw_process = ql.HullWhiteProcess(spot_curve_handle, a, sigma)
rng = ql.GaussianRandomSequenceGenerator(ql.UniformRandomSequenceGenerator(timestep, ql.UniformRandomGenerator()))
seq = ql.GaussianPathGenerator(hw_process, length, timestep, rng, False)