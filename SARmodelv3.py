import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from WTT import WTT

data = pd.read_csv(r'Data\TrainingData\GLMTraining.csv', delimiter=',')

#convert SAR from percent to decimal
data['SAR'] = data['SAR']/100

glm_data = data.drop(columns=['Year','Species']) 

#set limits to epsilon to avoid extreme value errors
epsilon = 1e-10
glm_data['SAR'] = glm_data['SAR'].clip(lower=epsilon, upper=1 - epsilon)

formula = 'SAR ~ PH + FTD + WTT + Transport * FTD'

model = smf.glm(formula=formula, data=glm_data, family=sm.families.Binomial())
result = model.fit()

# Print a summary of the model
#print(result.summary())


def SAR_model(downTouple,breachTouple, WTT=WTT): #downTouple and upTouple must be 1 year only

    FTD = 431.6*2

    WTTdays = WTT(breachTouple,downTouple)
    WTT = sum(WTTdays)/len(WTTdays)

    Transport = False

    PH = 16-sum(breachTouple)*2

    glm_evo = pd.DataFrame({'PH':PH, 'FTD':FTD, 'WTT':WTT, 'Transport':Transport})

    predicted_sar = result.predict(glm_evo)
    return(predicted_sar)
