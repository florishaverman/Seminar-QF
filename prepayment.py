# general tools
import numpy as np
import math
import pandas as pd  # for reading excel data file
from sklearn import linear_model  # for logistic regression

import matplotlib.pyplot as plt  # for plotting the data
import time  # to time the functions
import pickle  # To save logistic model, to avoid training each time.
import platform  # To check the system

"""
This file contains functions gegarding the prepayment model.
It can be used to train a prepayment model using trainPrepaymentModel()
The function getPrepaymentModel( fileName) returns a prepayment model, prepayment_model.sav can be used as file name
The function probPrepayment(model, incentive) returns the probabilty of prepayment for a given model and incentive level. 

@author: Floris
"""





### Function to load the data from ING
### need to check if this works on a windows, otherwise we need to use if statements. Discuss!
def loadINGData(sheet_name):
    if (platform.system() == 'Darwin'):
        return pd.read_excel('data/DataING.xlsx', sheet_name=sheet_name)  # Error in this line? Ask Floris
    else:
        return pd.read_excel('data\DataING.xlsx', sheet_name=sheet_name)  # Error in this line? Ask Floris


### A function for rescaling the data.
def rescale(data, variable_name, scaling):
    temp = data[variable_name].to_numpy()
    return np.round_(temp / scaling)

"""
This function is used to train a prepayment model.
filename: is the name underwhich the trained model is stored.
prepaymentSummary: The summerized version of prepayments. Here the prepayed and not prepayed amounts are calculated and grouped by incentive level. 
rescaleSize: The amount of money for which a data point is made, the default in 10000, although 1000 is also already been done.
"""
def trainPrepaymentModel(filename, prepaymentSummary, rescaleSize=10000):
    startTime = time.time()

    ### Rescale the variables to reduce the amount of data points 
    prepayed = rescale(prepaymentSummary, 'Sum of Prepayed', rescaleSize)
    notPrepayed = rescale(prepaymentSummary, 'Sum of not prepayed', rescaleSize)
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

    logr = linear_model.LogisticRegression(fit_intercept= True).fit(np.array(X).reshape(-1,1),np.array(y))
    
    endTime = time.time()
    print(f"Training took {round(endTime- startTime,1)} seconds")


    # save the model to disk
    pickle.dump(logr, open(filename, 'wb'))
    print(f"model is saved under the name {filename}")


""" 
This function calculates the probability of prepayment for a given model and incentive
model: A trained prepayment model, can be obtained by getPrepaymentModel()
incentive: a level of incentive
"""
def probPrepayment(model, incentive):
    log_odds = model.coef_ * incentive + model.intercept_
    odds = np.exp(log_odds)
    probability = odds / (1 + odds)
    return probability[0]

""" 
This fuction returns a trained prepayment model
fileName: There are different trained model, the default is stored in prepayment_model.sav
"""
def getPrepaymentModel(fileName):
     return pickle.load(open(fileName, 'rb'))

#Not a main function, mainly used for testing during building
def printPrepaymentOverview(model, values, showScaterPlot=False, toPrint=False):
    if (toPrint): print('The prepayment level for echt level of incentive is')
    probabilities = probPrepayment(model, values)
    overview = []
    for i in range(len(values)):
        overview.append([values[i], probabilities[i]])
    if (toPrint): print(pd.DataFrame(data=overview))
    if (showScaterPlot):
        plt.scatter(values, probabilities)
        plt.show()

def plotPrepaymentModel(model):
    beta0 = model.intercept_[0]
    beta1 = model.coef_[0][0]
    print(beta0)
    print(beta1)
    
    # Creating vectors X and Y
    x = np.linspace(-0.05, 0.25, 100)
    y = 1 / (1 + np.exp(-1 * ( beta0 + beta1 * x) ))
    # y =  (1 + math.exp(-1 * ( beta0 + beta1 * x) ))
    
    # fig = plt.figure(figsize = (10, 5))
    # Create the plot
    plt.plot(x, y)
    plt.xlabel("Incentive")
    plt.ylabel("Prepayment rate")
    
    # Show the plot
    plt.show()

def plotPrepaymentData(data):
    incentive = np.array(data["Incentive"])
    ppRate = np.array(data["Monthly pp rate"])
    
    # fig = plt.figure(figsize = (10, 5))
    # Create the plot
    plt.plot(incentive, ppRate, 'o')
    plt.xlabel("Incentive")
    plt.ylabel("Prepayment rate")
    
    # Show the plot
    plt.show()

def main():
    print('hello world from Floris')
    ### Load the created pivot table.
    # prepaymentSummary = loadINGData('Prepayment data')
    # plotPrepaymentData(prepaymentSummary)

    ### This line can be used to train the model.
    # resize of 10 000 takes -+ 40 sec, resize 1000 takes -+ 15 min
    # trainPrepaymentModel('prepayment_model.sav', prepaymentSummary)

    ### Load the prepayment model from disk, so no need to retrain every time ###
    loaded_model = pickle.load(open('prepayment_model.sav', 'rb'))
    plotPrepaymentModel(loaded_model)

    # print(f"The coefficients of the model are {loaded_model.coef_}")
    # print(f"The coefficients of the model are {loaded_model.intercept_}")

    # # printPrepaymentOverview(incentives)
    # values = []
    # for i in range(50):
    #     values.append(-0.05 + i * 0.0025)
    # printPrepaymentOverview(loaded_model, values, showScaterPlot=False, toPrint=False)
    print('prepayment.py is finished')

# main()

