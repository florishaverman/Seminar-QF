library(readxl)
library(xlsx)

# link to page with color names to use in plots
#https://r-graph-gallery.com/42-colors-names.html

path = "/Users/anneduivenvoorden/Documents/Msc Quantitative Finance/Seminar Financial Case Studies/Seminar-QF/Data"
desired_cf = read_excel(paste(path, "/SimulatedCFnRates.xlsx", sep = ""), sheet = 'Desired CF')
sim_cf = read_excel(paste(path, "/SimulatedCFnRates.xlsx", sep = ""), sheet = 'Simulated CF')
hedge = read_excel(paste(path, "/zcb margin hedge.xlsx", sep = ""), sheet = 1)

desired_cf = desired_cf[,2]
sim_cf = sim_cf[,2:101]
hedge = hedge[,2]

# PREP FOR PLOT
desired_cf = as.numeric(unlist(desired_cf))
hedge = as.numeric(unlist(hedge))
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
lines(m, desired_cf, type = 'l', col = 'black')
# plot hedge
lines(m, hedge, type = 'l', col = 'darkgreen')

