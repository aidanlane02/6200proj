import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from HydroModelv1 import hydropower
from HydroFlowAdjustment import flowAdjustment
from WTT import WTT


graniteUp = pd.read_csv(r'Data\LowerGraniteForebay.csv', delimiter=',')
graniteDown = pd.read_csv(r'Data\LowerGraniteTailwater.csv', delimiter=',')
gooseUp = pd.read_csv(r'Data\LittleGooseForebay.csv', delimiter=',')
gooseDown = pd.read_csv(r'Data\LittleGooseTailwater.csv', delimiter=',')
monumentalUp = pd.read_csv(r'Data\LowerMonumentalForebay.csv', delimiter=',')
monumentalDown = pd.read_csv(r'Data\LowerMonumentalTailwater.csv', delimiter=',')
iceUp = pd.read_csv(r'Data\IceHarborForebay.csv', delimiter=',')
iceDown = pd.read_csv(r'Data\IceHarborTailwater.csv', delimiter=',')
upTouple = [graniteUp,gooseUp,monumentalUp,iceUp]
downTouple = [graniteDown,gooseDown,monumentalDown,iceDown]


#DAM BREACH STATUS
graniteBreach = False
gooseBreach = False
monumentalBreach = False
iceBreach = False
breachTouple = [graniteBreach,gooseBreach,monumentalBreach,iceBreach]


graniteCap = 810
gooseCap = 810
monumentalCap = 810
iceCap = 603

hydropowerVec = np.vectorize(hydropower)
granitePower, graniteEnergy = hydropowerVec((graniteUp['Outflow (kcfs)']-graniteUp['Spill (kcfs)']).tolist(), graniteUp['Elevation (ft)'] - graniteDown['Tailwater Elevation (ft)'], graniteCap)
goosePower, gooseEnergy = hydropowerVec((gooseUp['Outflow (kcfs)']-gooseUp['Spill (kcfs)']).tolist(), gooseUp['Elevation (ft)'] - gooseDown['Tailwater Elevation (ft)'], gooseCap)
monumentalPower, monumentalEnergy = hydropowerVec((monumentalUp['Outflow (kcfs)']-monumentalUp['Spill (kcfs)']).tolist(), monumentalUp['Elevation (ft)'] - monumentalDown['Tailwater Elevation (ft)'], monumentalCap)
icePower, iceEnergy = hydropowerVec((iceUp['Outflow (kcfs)']-iceUp['Spill (kcfs)']).tolist(), iceUp['Elevation (ft)'] - iceDown['Tailwater Elevation (ft)'], iceCap)

#sum total power (don't need to take into account if dam is breached because water height differential will be 0)
totPower = granitePower + goosePower + monumentalPower + icePower
totEnergy = graniteEnergy + gooseEnergy + monumentalEnergy + iceEnergy

#adjust flows
upTouple,downTouple = flowAdjustment(upTouple,downTouple,breachTouple)


#WTT model in vector format (can also be done using average over a year)
spillPerTouple = [graniteDown['Spill Percent (%)'],gooseDown['Spill Percent (%)'],monumentalDown['Spill Percent (%)'],iceDown['Spill Percent (%)']]
WTTdays = WTT(breachTouple,spillPerTouple)
print(min(WTTdays))
print(max(WTTdays))

"""
#POWER GRAPHING
time = pd.date_range(start='2022-01-01', end='2023-12-31', freq='D')
power_series = pd.Series(totPower, index=time)
energy_series = pd.Series(totEnergy, index=time)

#time period averages
monthly_power_avg = power_series.resample('M').mean()

#graph
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(time, energy_series, label='Energy (MWh)', color='r', marker=None)
ax1.set_xlabel('Time')
ax1.set_ylabel('Energy (MWh)', color='r')
ax1.tick_params(axis='y', labelcolor='r')

ax2 = ax1.twinx()
ax2.plot(monthly_power_avg.index, monthly_power_avg, label='Monthly Average Power (MW)', color='b', marker=None)
ax2.set_ylabel('Monthly Average Power (MW)', color='b')
ax2.tick_params(axis='y', labelcolor='b')

plt.title('Power and Energy over Time with Little Goose Breached')
plt.grid(True)
fig.autofmt_xdate()
plt.show()
"""

'''
#FLOW GRAPHING
flow = upTouple[3]['Inflow (kcfs)']
time = pd.date_range(start='2022-01-01', end='2023-12-31', freq='D')
#graph
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(time, flow, label='Inflow (kcfs)', color='r')
ax1.set_xlabel('Time')
ax1.set_ylabel('Inflow (kcfs)', color='r')
ax1.tick_params(axis='y', labelcolor='r')

plt.title('Inflow at Ice Harbor with all dams normal')
plt.grid(True)
fig.autofmt_xdate()
plt.show()
'''     