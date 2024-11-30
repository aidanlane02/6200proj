import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

data = pd.read_csv(r'Data\TrainingData\GLMTraining.csv', delimiter=',')

#convert SAR from percent to decimal
data['SAR'] = data['SAR']/100

glm_data = data.drop(columns=['Year','Species']) 

#set limits to epsilon to avoid extreme value errors
epsilon = 1e-10
glm_data['SAR'] = glm_data['SAR'].clip(lower=epsilon, upper=1 - epsilon)

formula = 'SAR ~ PH + FTD + WTT + Transport'

model = smf.glm(formula=formula, data=glm_data, family=sm.families.Binomial())
result = model.fit()

# Print a summary of the model
print(result.summary())



#model 2 for only transported fish
glm_data_transport = glm_data[glm_data['Transport'] == True]
glm_data_transport = glm_data_transport.reset_index(drop=True)

formula_transport = 'SAR ~ PH * FTD + WTT'

model_transport = smf.glm(formula=formula_transport, data=glm_data_transport, family=sm.families.Binomial())
result_transport = model_transport.fit()

# Print a summary of the model
print(result_transport.summary())


#model 3 for only transported fish
glm_data_noTransport = glm_data[glm_data['Transport'] == False]
glm_data_noTransport = glm_data_noTransport.reset_index(drop=True)

formula_noTransport = 'SAR ~ PH * FTD + WTT'

model_noTransport = smf.glm(formula=formula_noTransport, data=glm_data_noTransport, family=sm.families.Binomial())
result_noTransport = model_noTransport.fit()

# Print a summary of the model
print(result_noTransport.summary())