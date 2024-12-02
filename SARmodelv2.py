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

formula = 'SAR ~ PH + FTD + WTT + Transport * FTD'

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


#model 3 for only non transported fish
glm_data_noTransport = glm_data[glm_data['Transport'] == False]
glm_data_noTransport = glm_data_noTransport.reset_index(drop=True)

formula_noTransport = 'SAR ~ PH * FTD + WTT'

model_noTransport = smf.glm(formula=formula_noTransport, data=glm_data_noTransport, family=sm.families.Binomial())
result_noTransport = model_noTransport.fit()

# Print a summary of the model
print(result_noTransport.summary())


#visualization of results
predicted_sar = result.predict(glm_data)
glm_data['Predicted SAR'] = predicted_sar

#convert SAR back
glm_data['SAR'] = glm_data['SAR']*100
glm_data['Predicted SAR'] = glm_data['Predicted SAR']*100

#export
glm_data.to_csv('Data\TrainingData\GLMTrainingResults.csv',index=False)

import matplotlib.pyplot as plt

# Separate data by Transported status
not_transported = glm_data[glm_data['Transport'] == 0]
transported = glm_data[glm_data['Transport'] == 1]

# Create the plot
plt.figure(figsize=(10, 6))

# Plot actual SAR
plt.scatter(
    not_transported['WTT'],
    not_transported['SAR'],
    color='blue', label='Actual SAR (Not Transported)', alpha=0.6
)
plt.scatter(
    transported['WTT'],
    transported['SAR'],
    color='orange', label='Actual SAR (Transported)', alpha=0.6
)

# Plot predicted SAR
plt.scatter(
    not_transported['WTT'],
    not_transported['Predicted SAR'],
    color='purple', label='Predicted SAR (Not Transported)', alpha=0.6, marker='x'
)
plt.scatter(
    transported['WTT'],
    transported['Predicted SAR'],
    color='yellow', label='Predicted SAR (Transported)', alpha=0.6, marker='x'
)

# Add labels and legend
plt.xlabel('WTT')
plt.ylabel('SAR')
plt.title('Actual vs. Predicted SAR by WTT')
plt.legend()
plt.show()