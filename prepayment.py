#general tools
import numpy as np

import pandas as pd #for reading excel data file
from sklearn import linear_model # for logistic regression

import matplotlib.pyplot as plt #for plotting the data
import time # to time the functions
import pickle #To save logistic model, to avoid training each time. 
import platform #To check the system

print('hello world from Floris')

### Function to load the data from ING
### need to check if this works on a windows, otherwise we need to use if statements. Discuss!

def loadINGData(sheet_name):
    if (platform.system() == 'Darwin'):
        return pd.read_excel('data/DataING.xlsx', sheet_name=sheet_name) #Error in this line? Ask Floris
    else:
        return pd.read_excel('data\DataING.xlsx', sheet_name=sheet_name) #Error in this line? Ask Floris

### A function for rescaling the data.
def rescale(data,variable_name, scaling):
    temp = data[variable_name].to_numpy()
    return np.round_(temp/scaling)
 
def trainPrepaymentModel(filename, prepaymentSummary, rescaleSize = 10000):
    startTime = time.time()

    ### Rescale the variables to reduce the amount of data points 
    prepayed = rescale(prepaymentSummary,'Sum of Prepayed', rescaleSize)
    notPrepayed = rescale(prepaymentSummary,'Sum of not prepayed', rescaleSize)
    incentive = prepaymentSummary["Incentive"].to_numpy()

    ### spliting the prepayment data dependent variable into binary instead of continous variable. ###
    X = []
    y = []

    for i in range(len(incentive)):
        for j in range(int(prepayed[i])):
            X.append(incentive[i])
            y.append(1)
        for j in range(int(notPrepayed[i])):
            X.append(incentive[i])
            y.append(0)

    print(len(X))
    print(len(y))

    logr = linear_model.LogisticRegression(fit_intercept= True).fit(np.array(X).reshape(-1,1),np.array(y))
#
    endTime = time.time()
    print(f"Training took {round(endTime- startTime,1)} seconds")

    # save the model to disk
    pickle.dump(logr, open(filename, 'wb'))
    print(f"model is saved under the name {filename}")


### This function calculates the probability of prepayment for a given model and incentive
def probPrepayment(model,x):
    log_odds = model.coef_ * x + model.intercept_
    odds = np.exp(log_odds)
    probability = odds / (1 + odds)
    return(probability[0])

def printPrepaymentOverview(model, values, showScaterPlot = False, toPrint = False):
    if (toPrint): print('The prepayment level for echt level of incentive is')
    probabilities = probPrepayment(model, values)
    overview = []
    for i in range(len(values)):
        overview.append([values[i], probabilities[i]])
    if (toPrint): print(pd.DataFrame(data =overview))
    if (showScaterPlot):
        plt.scatter(values, probabilities)
        plt.show()

def main():
    ### Load the created pivot table.
    prepaymentSummary = loadINGData('Prepayment summary')

    ### This line can be used to train the model.
    #resize of 10 000 takes -+ 40 sec, resize 1000 takes -+ 15 min
    #trainPrepaymentModel('prepayment_model.sav', prepaymentSummary)

    ### Load the prepayment model from disk, so no need to retrain every time ###
    loaded_model = pickle.load(open('prepayment_model.sav', 'rb'))
    print(f"The coefficients of the model are {loaded_model.coef_}")
    print(f"The coefficients of the model are {loaded_model.intercept_}")

    #printPrepaymentOverview(incentives)
    values = []
    for i in range(50):
        values.append(-0.05 + i * 0.0025)
    printPrepaymentOverview(loaded_model, values, showScaterPlot = False, toPrint = False)

#main()

""" 
### this is all trash ###
plt.scatter(X, y)
plt.show()

#print(prepaymentData)
incentive = prepaymentData["Incentive"].to_numpy()
print(incentive)
ppRate = prepaymentData["Monthly pp rate"].to_numpy()
print(ppRate)

#spliting the prepayment data dependent variable into binary instead of continous variable.
plt.scatter(incentive, ppRate)
plt.show()


logr = linear_model.LogisticRegression()
logr.fit(incentive.reshape(-1,1),ppRate)
"""

print('prepayment.py is finished')