import numpy as np
import pandas as pd
from WTT import WTT

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

graniteDown = pd.read_csv(r'Data\TrainingData\GraniteDownTraining.csv', delimiter=',')
gooseDown = pd.read_csv(r'Data\TrainingData\GooseDownTraining.csv', delimiter=',')
monumentalDown = pd.read_csv(r'Data\TrainingData\MonumentalDownTraining.csv', delimiter=',')
iceDown = pd.read_csv(r'Data\TrainingData\IceDownTraining.csv', delimiter=',')


#find WTT days for all years
graniteBreach = False
gooseBreach = False
monumentalBreach = False
iceBreach = False
breachTouple = [graniteBreach,gooseBreach,monumentalBreach,iceBreach]
spillPerTouple = [graniteDown['Spill Percent (%)'],gooseDown['Spill Percent (%)'],monumentalDown['Spill Percent (%)'],iceDown['Spill Percent (%)']]
WTTdays = WTT(breachTouple,spillPerTouple)

startRow = 1826 #replace with iceDown.loc[iceDown['Date'] == '1/1/2000'], idk why its not working
yearAverage = []
for y in range(20):
    sum = 0
    for d in range(365):
        sum += WTTdays[startRow+y*365+d]
    yearAverage.append(sum/365)
doubleWTT = np.tile(yearAverage,2) #I used snake river WTT as a proxy for both columbia river WTT and total WTT


sar = [10.77,3.86,3.78,2.77,3.14,1.85,2.06,4.33,5.51,6.77,3.55,0.9,3.13,4.18,3.81,3.54,2.11,0.76,2.12,1.38, #years 2000-2019 from McNary
       2.6,1.81,1.14,0.34,0.68,0.29,0.84,1.16,3.58,1.93,0.92,0.42,1.48,1.54,0.61,0.28,0.44,0.25,0.54,0.79] #years 2000-2019 from granite

ph = [4,8]
phRep = np.repeat(ph,20) #number of powerhouse passage events, aka the number of dams between data location and the ocean

damDist = [145,277]
damDistRep = np.repeat(damDist,20) #distance the fish need to swim to get to the ocean, distance between dams was easiest to find so thats what these numbers are but I will find
                                    #actual distance when I have time. For hatchery fish we can also use distance to hatchery but they would have to be in a different model fit
                                    #because we don't know how far upstream the non-hatchery fish spawn



#everything below is for linear regression
X = np.column_stack((np.array(doubleWTT),np.array(phRep),np.array(damDistRep)))
Y = np.array(sar)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, Y_train)

Y_pred = model.predict(X_test)

# Model coefficients
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# Performance metrics
print("Mean Squared Error:", mean_squared_error(Y_test, Y_pred))
print("R^2 Score:", r2_score(Y_test, Y_pred))



#everything here would be fit into a neat function and output the coefficients and intercept. Hopefully it will also be able to take fish transportation into account although I
#do not yet know exactly how that part would work. If we want the randomness variables like we say, we would have to make out evolutionary model also stochastic. We have to decide
#exactly how we want to do that part.