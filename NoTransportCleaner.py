import pandas as pd
import numpy as np

#import dataset
uncleanSnake = pd.read_csv(r'Data\TrainingData\DataClearners\SnakeSarNoTransport.csv')

#drop unimportant columns
uncleanSnake = uncleanSnake.drop(columns=['RearCode','RaceCode','JuvPop','SARwoJacks','SARwoJacks_LCI','SARwoJacks_UCI','SARwJacks_LCI','SARwJacks_UCI'])

#create decision variable columns
damPasses = [] #need to decide on 2 way or 1 way
dists = []

#assign powerhouse passage events and preliminary distances
for i in range(len(uncleanSnake['MigrYr'])): 
    if uncleanSnake['SAR_Reach'][i]=='Bonneville Dam to Bonneville Dam':
        damPasses.append(2)
        dists.append(146.1*2)
    elif uncleanSnake['SAR_Reach'][i]=='John Day Dam to Bonneville Dam':
        damPasses.append(4)
        dists.append(215.6+146.1)
    elif uncleanSnake['SAR_Reach'][i]=='Lower Granite Dam to Bonneville Dam':
        damPasses.append(9)
        dists.append(431.6+146.1)
    elif uncleanSnake['SAR_Reach'][i]=='Lower Granite Dam to Lower Granite Dam':
        damPasses.append(16)
        dists.append(431.6*2)
    elif uncleanSnake['SAR_Reach'][i]=='Lower Monumental Dam to Bonneville Dam':
        damPasses.append(7)
        dists.append(366+146.1)
    elif uncleanSnake['SAR_Reach'][i]=='Lower Monumental Dam to Lower Monumental Dam':
        damPasses.append(12)
        dists.append(366*2)
    elif uncleanSnake['SAR_Reach'][i]=='McNary Dam to Bonneville Dam':
        damPasses.append(5)
        dists.append(292+146.1)
    elif uncleanSnake['SAR_Reach'][i]=='McNary Dam to McNary Dam':
        damPasses.append(8)
        dists.append(292*2)
    elif uncleanSnake['SAR_Reach'][i]=='Release Site to Bonneville Dam':
        damPasses.append(1)
        dists.append(146.1)
    else:
        damPasses.append(-1)
        dists.append(-1)

#adjust distances for start location
for i in range(len(uncleanSnake['MigrYr'])): #unused for now
    if uncleanSnake['GroupDescription'][i]=='Asotin River Wild Steelhead':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Clearwater River Wild Spring Chinook':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Clearwater River Wild Steelhead A-Run':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Deschutes River Wild Fall Chinook':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Deschutes River Wild Steelhead':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Grande Ronde River Wild Spring Chinook':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Grande Ronde River Wild Steelhead A-Run':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Hanford Reach Wild Fall Chinook':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Imnaha River Wild Steelhead A-Run':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Imnaha River Wild Summer Chinook':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='John Day River Wild Spring Chinook':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='John Day River Wild Steelhead':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Middle Fork Salmon River Wild Spring_Summer Chinook':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Salmon River Wild Steelhead A-Run':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Snake River Wild Fall Chinook':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Snake River Wild Spring_Summer Chinook':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Snake River Wild Steelhead Aggregate':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Snake River Wild Steelhead A-Run':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Snake River Wild Steelhead B-Run':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='South Fork Salmon River Wild Spring_Summer Chinook':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Tucannon River Wild Spring Chinook':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Tucannon River Wild Summer Steelhead':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Umatilla River Wild Steelhead':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Upper Salmon River Wild Spring_Summer Chinook':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Yakima River Wild Spring Chinook':
        dists[i] = dists[i] + 0
    elif uncleanSnake['GroupDescription'][i]=='Yakima River Wild Steelhead':
        dists[i] = dists[i] + 0
    else:
        dists[i] = -1

#add values to array
uncleanSnake['PH'] = damPasses
uncleanSnake['FTD'] = dists
uncleanSnake['Transport'] = np.full(len(uncleanSnake['GroupDescription']),False)

#remove group discription and reach
uncleanSnake = uncleanSnake.drop(columns=['GroupDescription','SAR_Reach'])

#rename columns
cleanSnake = uncleanSnake.rename(columns={"MigrYr": "Year", "SARwJacks": "SAR", "SpeciesCode": "Species"})

print(cleanSnake)




#import dataset
uncleanColumbia = pd.read_csv(r'Data\TrainingData\DataClearners\ColumbiaSarNoTransport.csv')

#drop unimportant columns
uncleanColumbia = uncleanColumbia.drop(columns=['RearCode','RaceCode','JuvPop','SARwoJacks','SARwoJacks_LCI','SARwoJacks_UCI','SARwJacks_LCI','SARwJacks_UCI'])

#create decision variable columns
damPasses = [] #need to decide on 2 way or 1 way
dists = []

#assign powerhouse passage events and preliminary distances
for i in range(len(uncleanColumbia['MigrYr'])):
    if uncleanColumbia['SAR_Reach'][i]=='Bonneville Dam to Bonneville Dam':
        damPasses.append(2)
        dists.append(146.1*2)
    elif uncleanColumbia['SAR_Reach'][i]=='John Day Dam to Bonneville Dam':
        damPasses.append(4)
        dists.append(215.6+146.1)
    elif uncleanColumbia['SAR_Reach'][i]=='McNary Dam to Bonneville Dam':
        damPasses.append(5)
        dists.append(292+146.1)
    elif uncleanColumbia['SAR_Reach'][i]=='McNary Dam to McNary Dam':
        damPasses.append(8)
        dists.append(292*2)
    elif uncleanColumbia['SAR_Reach'][i]=='Release Site to Bonneville Dam':
        damPasses.append(1)
        dists.append(146.1)
    else: #error catching
        damPasses.append(-1)
        dists.append(-1)

#adjust distances for start location
for i in range(len(uncleanColumbia['MigrYr'])): #unused for now
    if uncleanColumbia['GroupDescription'][i]=='Deschutes River Wild Fall Chinook':
        dists[i] = dists[i] + 0
    elif uncleanColumbia['GroupDescription'][i]=='Deschutes River Wild Steelhead':
        dists[i] = dists[i] + 0
    elif uncleanColumbia['GroupDescription'][i]=='Hanford Reach Wild Fall Chinook':
        dists[i] = dists[i] + 0
    elif uncleanColumbia['GroupDescription'][i]=='John Day River Wild Spring Chinook':
        dists[i] = dists[i] + 0
    elif uncleanColumbia['GroupDescription'][i]=='John Day River Wild Steelhead':
        dists[i] = dists[i] + 0
    elif uncleanColumbia['GroupDescription'][i]=='Umatilla River Wild Steelhead':
        dists[i] = dists[i] + 0
    elif uncleanColumbia['GroupDescription'][i]=='Yakima River Wild Spring Chinook':
        dists[i] = dists[i] + 0
    elif uncleanColumbia['GroupDescription'][i]=='Yakima River Wild Steelhead':
        dists[i] = dists[i] + 0
    else:
        dists[i] = -1

#add values to array
uncleanColumbia['PH'] = damPasses
uncleanColumbia['FTD'] = dists
uncleanColumbia['Transport'] = np.full(len(uncleanColumbia['GroupDescription']),False)

#remove group discription and reach
uncleanColumbia = uncleanColumbia.drop(columns=['GroupDescription','SAR_Reach'])

#rename columns
cleanColumbia = uncleanColumbia.rename(columns={"MigrYr": "Year", "SARwJacks": "SAR", "SpeciesCode": "Species"})

print(cleanColumbia)

cleanSnake.to_csv('Data\TrainingData\SnakeTraining.csv', index=False)
cleanColumbia.to_csv('Data\TrainingData\ColumbiaTraining.csv',index=False)