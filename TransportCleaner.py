import pandas as pd
import numpy as np

#import dataset
uncleanTransport = pd.read_csv(r'Data\TrainingData\DataClearners\SnakeSarTransport.csv')

#create decision variable columns
damPasses = [] #need to decide on 2 way or 1 way
dists = []

for i in range(len(uncleanTransport['Year'])):
    if uncleanTransport['Location'][i]=='TLGR':
        damPasses.append(8)
        dists.append(146.1+431)
    elif uncleanTransport['Location'][i]=='TLGS':
        damPasses.append(9)
        dists.append(146.1+431+37)
    elif uncleanTransport['Location'][i]=='TLMN':
        damPasses.append(10)
        dists.append(146.1+431+65.6)


#add values to array
uncleanTransport['PH'] = damPasses
uncleanTransport['FTD'] = dists
uncleanTransport['Transport'] = np.full(len(uncleanTransport['Year']),True)

#remove group discription and reach
uncleanTransport = uncleanTransport.drop(columns=['Adults','Location'])

cleanTransport = uncleanTransport.dropna()

print(cleanTransport)

cleanTransport.to_csv('Data\TrainingData\TransportTraining.csv', index=False)