library(readxl)
library(xlsx)

# link to page with color names to use in plots
#https://r-graph-gallery.com/42-colors-names.html

path = "/Users/anneduivenvoorden/Documents/Msc Quantitative Finance/Seminar Financial Case Studies/Seminar-QF/Data"
desired_cf = read_excel(paste(path, "/SimulatedCFnRates.xlsx", sep = ""), sheet = 'Desired CF')
sim_cf = read_excel(paste(path, "/SimulatedCFnRates.xlsx", sep = ""), sheet = 'Simulated CF')
hedge_margin = read_excel(paste(path, "/zcb margin hedge.xlsx", sep = ""), sheet = 1)
hedge_value = read_excel(paste(path, "/zcb value hedge.xlsx", sep = ""), sheet = 1)

desired_cf = desired_cf[,2]
sim_cf = sim_cf[,2:101]
hedge_margin = hedge_margin[,2]
hedge_value = hedge_value[,2]

# PREP FOR PLOT
desired_cf = as.numeric(unlist(desired_cf))
hedge_margin = as.numeric(unlist(hedge_margin))
hedge_value = as.numeric(unlist(hedge_value))
# list with months
m = c(1:120)
# basic plot with only simulated and desired CF
plot(NULL, xlim=c(0,120), ylim=c(0,800000), yaxt="n", ylab="Cash flow x €1000", 
     xaxt="n", xlab="Month")
# fix axis
axis(side = 2, at = c(0, 200000, 400000, 600000, 800000), labels = c(0, 200, 400, 600, 800))
xax = rep(1, 60)
for(i in 1:60){
  xax[i] = i*2
}
axis(side = 1, at = xax)
# plot simulated CF
for(i in 1:100){
  curr_sim = as.numeric(unlist(sim_cf[,i]))
  points(m, curr_sim, pch = 5, col = 'azure3', asp = 1)
}
# plot desired CF
lines(m, desired_cf, type = 'l', col = 'black', lwd = 1)
# plot hedge
lines(m, hedge_value, type = 'l', col = 'blue3', lwd = 2)
lines(m, hedge_margin, type = 'l', col = 'darkgreen', lwd = 2)
legend("topright", legend = c("Cash flow w/o prepayments", "Cash flow of margin hedge", 
                              "Cash flow of value hedge", "Simulated cash flows"),
       col = c("black", "darkgreen", "blue3", "azure3"), lty=1:2, cex = 0.8)

# zoomed in plot
plot(NULL, xlim=c(0,120), ylim=c(-30000,42000), yaxt="n", ylab="Cash flow", 
     xaxt="n", xlab="Month")
# fix axis
axis(side = 2, at = c(-20000,-10000, 0, 10000, 20000, 30000, 40000))
xax = rep(1, 60)
for(i in 1:60){
  xax[i] = i*2
}
axis(side = 1, at = xax)
# plot simulated CF
for(i in 1:100){
  curr_sim = as.numeric(unlist(sim_cf[,i]))
  points(m, curr_sim, pch = 5, col = 'azure3', asp = 1)
}
# plot desired CF
lines(m, desired_cf, type = 'l', col = 'black', lwd = 1)
# plot hedge
lines(m, hedge_value, type = 'l', col = 'blue3', lwd = 2)
lines(m, hedge_margin, type = 'l', col = 'darkgreen', lwd = 2)
legend("bottomright", legend = c("Cash flow w/o prepayments", "Cash flow of margin hedge", 
                                 "Cash flow of value hedge", "Simulated cash flows"),
       col = c("black", "darkgreen", "blue3", "azure3"), lty=1:2, cex = 0.8)

