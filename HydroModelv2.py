import numpy as np
import pandas as pd

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


def hydroPowerList(upTouple, downTouple, maxPowerTouple):
    #initialize arrays
    out = downTouple['Date']
    granitePow = []
    goosePow = []
    monumentalPow = []
    icePow = []

    for d in range(len(out)):
        granitePow.append(hydropower((upTouple[0]['Outflow (kcfs)'][d]-upTouple[0]['Spill (kcfs)'][d]), upTouple[0]['Elevation (ft)'][d] - downTouple[0]['Tailwater Elevation (ft)'][d], maxPowerTouple[0]))
        goosePow.append(hydropower((upTouple[1]['Outflow (kcfs)'][d]-upTouple[1]['Spill (kcfs)'])[d], upTouple[1]['Elevation (ft)'][d] - downTouple[1]['Tailwater Elevation (ft)'][d], maxPowerTouple[1]))
        monumentalPow.append(hydropower((upTouple[2]['Outflow (kcfs)'][d]-upTouple[2]['Spill (kcfs)'][d]), upTouple[2]['Elevation (ft)'][d] - downTouple[2]['Tailwater Elevation (ft)'][d], maxPowerTouple[2]))
        icePow.append(hydropower((upTouple[3]['Outflow (kcfs)'][d]-upTouple[3]['Spill (kcfs)'][d]), upTouple[3]['Elevation (ft)'][d] - downTouple[3]['Tailwater Elevation (ft)'][d], maxPowerTouple[3]))

    totPow = granitePow + goosePow + monumentalPow + icePow
    totEnergy = totPow * 24

    out['Lower Granite Power (MW)'] = granitePow
    out['Little Goose Power (MW)'] = goosePow
    out['Lower Monumental Power (MW)'] = monumentalPow
    out['Ice Harbor Power (MW)'] = icePow
    out['Total Power (MW)'] = totPow
    out['Total Energy (MWh)'] = totEnergy
    return out