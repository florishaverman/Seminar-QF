function [output] = MSE(HWTree, parameters, data, ValuationDate, VolDates, Maturities)
vol = parameters(1);
alpha = parameters(2);
output = 0;
n = length(Maturities);
VolCurve = vol;
AlphaCurve = alpha;
VolSpec = hwvolspec(ValuationDate,VolDates,VolCurve,VolDates,AlphaCurve);
NewTree = hwtree(VolSpec, HWTree.RateSpec, HWTree.TimeSpec);
for i = 1:n
    LegRate = [data(i+1) 0];
    [Price,~,~] = swapbyhw(NewTree,LegRate,ValuationDate,Maturities(i));
    output = output + Price^2;
end
end
