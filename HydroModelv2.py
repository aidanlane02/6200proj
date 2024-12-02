import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # Turn off the warning
def hydropower(vol, height, maxPower, efficiency = 0.8): #efficiency of 0.8 lines up best with the actual dam power output
    #returns the amount of power generated in MW
    m3s = 28.316847*vol
    height_m = height*0.3048
    g = 9.81
    denWater = 997
    power_W= m3s*height_m*denWater*g*efficiency
    power_MW = min(power_W/10**6,maxPower)

    #ensure power falls within range 0-maxPower
    if power_MW > maxPower:
        power_MW = maxPower
    elif power_MW < 0:
        power_MW = 0
        
    return(power_MW)


def hydroPowerList(up, down, maxPower):
    #initialize arrays
    out = pd.DataFrame({'Date': down[0]['Date']})
    granitePow = []
    goosePow = []
    monumentalPow = []
    icePow = []
    totPow = []

    for d in range(len(out['Date'])):
        granitePow.append(hydropower((up[0].loc[d,'Outflow (kcfs)']-up[0].loc[d,'Spill (kcfs)']), up[0].loc[d,'Elevation (ft)'] - down[0].loc[d,'Tailwater Elevation (ft)'], maxPower[0]))
        goosePow.append(hydropower((up[1].loc[d,'Outflow (kcfs)']-up[1].loc[d,'Spill (kcfs)']), up[1].loc[d,'Elevation (ft)'] - down[1].loc[d,'Tailwater Elevation (ft)'], maxPower[1]))
        monumentalPow.append(hydropower((up[2].loc[d,'Outflow (kcfs)']-up[2].loc[d,'Spill (kcfs)']), up[2].loc[d,'Elevation (ft)'] - down[2].loc[d,'Tailwater Elevation (ft)'], maxPower[2]))
        icePow.append(hydropower((up[3].loc[d,'Outflow (kcfs)']-up[3].loc[d,'Spill (kcfs)']), up[3].loc[d,'Elevation (ft)'] - down[3].loc[d,'Tailwater Elevation (ft)'], maxPower[3]))
        totPow.append(granitePow[d] + goosePow[d] + monumentalPow[d] + icePow[d])

    totEnergy = [p * 24 for p in totPow]


    
    out.loc[:,'Lower Granite Power (MW)'] = granitePow
    out.loc[:,'Little Goose Power (MW)'] = goosePow
    out.loc[:,'Lower Monumental Power (MW)'] = monumentalPow
    out.loc[:,'Ice Harbor Power (MW)'] = icePow
    out.loc[:,'Total Power (MW)'] = totPow
    out.loc[:,'Total Energy (MWh)'] = totEnergy
    return out