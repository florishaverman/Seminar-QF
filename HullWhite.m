load deriv.mat;
ValuationDate = datetime(2004,1,1);
VolDates = [datetime(2004,31,12) datetime(2005,31,12) datetime(2006,31,12) datetime(2007,31,12), datetime(2008,31,12) datetime(2009,31,12)];
%VolCurve = 10;
%AlphaDates = VolDates;
%AlphaCurve = 10;
%VolSpec = hwvolspec(ValuationDate,VolDates,VolCurve,AlphaDates,AlphaCurve);
%NewTree = hwtree(VolSpec, HWTree.RateSpec, HWTree.TimeSpec);
%LegRate = [data(1) 0];
Maturities = [datetime(2006,1,1) datetime(2008,1,1) datetime(2010,1,1)];
%[Price,~,~] = swapbyhw(NewTree,LegRate,ValuationDate,Maturity)
func = @(parameters)MSE(HWTree, parameters, data, ValuationDate, VolDates, Maturities);
a = fmincon(func, [0.1 0.2], [-1 0; 0 -1], [0 0]);

