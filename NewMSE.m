function [output] = NewMSE(parameters)
kappa = parameters(1);
eta = parameters(2);
data = [-0.0043 -0.0018 -0.0003 0.0025];
Rates = [0.01; 0.02; 0.03; 0.04; 0.05; 0.06; 0.07; 0.08; 0.09; 0.1];
Maturity = [datetime(2022,12,1) datetime(2023,12,1) datetime(2024,12,1) datetime(2025,12,1) datetime(2026,12,1) datetime(2027,12,1) datetime(2028,12,1) datetime(2029,12,1) datetime(2030,12,1) datetime(2031,12,1)];
StartTimes = [0; 0; 0; 0; 0; 0; 0; 0; 0; 0];
EndTimes = [1; 2; 3; 4; 5; 6; 7; 8; 9; 10];
RateSpec = intenvset('Rates', Rates, 'StartDates', datetime(2021,12,1), 'EndDates', Maturity, 'Compounding', 12, 'StartTimes', StartTimes, 'EndTimes', EndTimes);
ValuationDate = datetime(2021,12,1);
TimeSpec = hwtimespec(ValuationDate, Maturity);
VolSpec = hwvolspec(ValuationDate, Maturity, eta, datetime(2032,1,1), kappa);
HWTree = hwtree(VolSpec, RateSpec, TimeSpec);
n = length(data);
output = 0;
Maturities = [datetime(2022,12,1) datetime(2024,12,1) datetime(2026,12,1) datetime(2031,12,1)];
for i = 1:n
    LegRate = [data(i) 0];
    [Price,~,~] = swapbyhw(HWTree,LegRate,ValuationDate,Maturities(i));
    output = output + Price^2;
end
end