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
data = MortgageDataS1;
vol = 0.3;
alpha = 0.3;
y1 = MSE(HWTree, vol, alpha, data, ValuationDate, VolDates, Maturities);
y2 = MSE(HWTree, 0.301, alpha, data, ValuationDate, VolDates, Maturities);
y3 = MSE(HWTree, vol, 0.301, data, ValuationDate, VolDates, Maturities);
g1 = (y2-y1)/0.001;
g2 = (y3-y1)/0.001;
while g1^2 + g2^2 > 500
    step = 0.00001;
    while step >= 0.00000125
        vol2 = vol-step*g1;
        alpha2 = alpha-step*g2;
        if MSE(HWTree, vol2, alpha2, data, ValuationDate, VolDates, Maturities) < y1
            y1 = MSE(HWTree, vol2, alpha2, data, ValuationDate, VolDates, Maturities);
            vol = vol2;
            alpha = alpha2;
            step = 0;
        else
            step = step/2;
        end
    end
    y2 = MSE(HWTree, vol+0.001, alpha, data, ValuationDate, VolDates, Maturities);
    y3 = MSE(HWTree, vol, alpha+0.001, data, ValuationDate, VolDates, Maturities);
    g1 = (y2-y1)/0.001;
    g2 = (y3-y1)/0.001;
end
