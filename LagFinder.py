import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from HydroModelv1 import hydropower


iceUp = pd.read_csv(r'Data\IceHarborForebay.csv', delimiter=',')
iceDown = pd.read_csv(r'Data\IceHarborTailwater.csv', delimiter=',')
gooseUp = pd.read_csv(r'Data\LittleGooseForebay.csv', delimiter=',')
gooseDown = pd.read_csv(r'Data\LittleGooseTailwater.csv', delimiter=',')
graniteUp = pd.read_csv(r'Data\LowerGraniteForebay.csv', delimiter=',')
graniteDown = pd.read_csv(r'Data\LowerGraniteTailwater.csv', delimiter=',')
monumentalUp = pd.read_csv(r'Data\LowerMonumentalForebay.csv', delimiter=',')
monumentalDown = pd.read_csv(r'Data\LowerMonumentalTailwater.csv', delimiter=',')


#compute  cross correlation
granite_goose_corr = np.correlate(graniteDown['Outflow (kcfs)'][485:525] - np.mean(graniteDown['Outflow (kcfs)'][485:525]), gooseUp['Inflow (kcfs)'][485:525] - np.mean(gooseUp['Inflow (kcfs)'][485:525]), mode='full')
goose_monumental_corr = np.correlate(gooseDown['Outflow (kcfs)'] - np.mean(gooseDown['Outflow (kcfs)']), monumentalUp['Inflow (kcfs)'] - np.mean(monumentalUp['Inflow (kcfs)']), mode='full')
monumental_ice_corr = np.correlate(monumentalDown['Outflow (kcfs)'] - np.mean(monumentalDown['Outflow (kcfs)']), iceUp['Inflow (kcfs)'] - np.mean(iceUp['Inflow (kcfs)']), mode='full')

#lags
lags = np.arange(-len(graniteDown['Outflow (kcfs)'][485:525]) + 1, len(gooseUp['Inflow (kcfs)'][485:525])) 

#normalize
granite_goose_corr = granite_goose_corr/np.max(np.abs(granite_goose_corr))
goose_monumental_corr = goose_monumental_corr/np.max(np.abs(goose_monumental_corr))
monumental_ice_corr = monumental_ice_corr/np.max(np.abs(monumental_ice_corr))

#2nd plot for shorter timespan
plt.figure(figsize=(12, 6))
plt.plot(lags, granite_goose_corr, color='blue')
plt.title('Cross-Correlogram of monumental outflow vs. ice harbor inflow')
plt.xlabel('Lag (days)')
plt.ylabel('Cross-Correlation')
plt.grid()
plt.xlim([0, 40]) #unsure if negative lag is relevant/possible
plt.show()