#general tools
import numpy as np

import pandas as pd #for reading excel data file
from sklearn import linear_model # for logistic regression

import matplotlib.pyplot as plt #for plotting the data
import time # to time the functions
import pickle #To save logistic model, to avoid training each time. 



print('hello world from floris')

### Function to load the data
def loadINGData(sheet_name):
    return pd.read_excel('data/DataING.xlsx', sheet_name=sheet_name)

# A bit of data reformating 
prepaymentData = loadINGData('Prepayment data')
data = prepaymentData.to_numpy()
#print(prepaymentData)

prepaymentSummary = loadINGData('Prepayment summary')
#print(prepaymentSummary)

def rescale(variable_name, scaling):
    temp = prepaymentSummary[variable_name].to_numpy()
    return np.round_(temp/scaling)
    
prepayed = rescale('Sum of Prepayed', 10000)
notPrepayed = rescale('Sum of not prepayed', 10000)
incentive = prepaymentSummary["Incentive"].to_numpy()

#print(prepayed)
#print(notPrepayed)

def trainPrepaymentModel(filename):
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

    startTime = time.time()
    logr = linear_model.LogisticRegression()
    logr.fit(np.array(X).reshape(-1,1),np.array(y))

    endTime = time.time()
    print(f"Traing took {round(endTime- startTime,1)} seconds")

    # save the model to disk
    pickle.dump(logr, open(filename, 'wb'))
    print(f"model is saved under the name {filename}")
#trainPrepaymentModel('prepayment_model.sav')


# load the model from disk
loaded_model = pickle.load(open('prepayment_model.sav', 'rb'))
print(loaded_model.coef_)

def logit2prob(logr,x):
  log_odds = logr.coef_ * x + logr.intercept_
  odds = np.exp(log_odds)
  probability = odds / (1 + odds)
  return(probability)

print(logit2prob(loaded_model, incentive))



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



print('done')