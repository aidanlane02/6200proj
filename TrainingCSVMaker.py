import numpy as np
import pandas as pd
from WTT import WTT

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
dates = graniteDown['Date']
WTTdays = WTT(breachTouple,spillPerTouple)


#create WTT dataframe
WTTdataframe = pd.DataFrame({'Date': dates,'WTT': WTTdays})

#convert date to date format
WTTdataframe['Date'] = pd.to_datetime(WTTdataframe['Date'])

#calculate yearly averages
WTTdataframe['Year'] = WTTdataframe['Date'].dt.year
averageWTT = WTTdataframe.groupby('Year', as_index=False)['WTT'].mean()

cleanSnake = pd.read_csv(r'Data\TrainingData\SnakeTraining.csv')
cleanColumbia = pd.read_csv(r'Data\TrainingData\ColumbiaTraining.csv')
cleanTransport = pd.read_csv(r'Data\TrainingData\TransportTraining.csv')

#combine datasets
SARcombined = pd.concat([cleanSnake, cleanColumbia, cleanTransport], ignore_index=True)

#merge with water
GLMTraining = pd.merge(SARcombined, averageWTT, on="Year", how="left")

#drop values where years don't match
GLMTraining = GLMTraining.dropna()

GLMTraining.to_csv('Data\TrainingData\GLMTraining.csv',index=False)