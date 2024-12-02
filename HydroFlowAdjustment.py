import numpy as np
import copy

def flowAdjustment(upTouple, downTouple, breachTouple):
    newUpTouple = copy.deepcopy(upTouple)
    newDownTouple = copy.deepcopy(downTouple)

    #checks for first 3 dams breached, does not yet take into account lag time for water between dams
    for i in range(3):
        if breachTouple[i]:
            newUpTouple[i+1]['Inflow (kcfs)'] = newUpTouple[i+1]['Inflow (kcfs)'] + newUpTouple[i]['Inflow (kcfs)'] - newUpTouple[i]['Outflow (kcfs)'] 
            newDownTouple[i+1]['Inflow (kcfs)'] = newUpTouple[i+1]['Inflow (kcfs)'] + newUpTouple[i]['Inflow (kcfs)'] - newUpTouple[i]['Outflow (kcfs)'] 
            newUpTouple[i]['Outflow (kcfs)'] = newUpTouple[i]['Inflow (kcfs)']
            newDownTouple[i]['Outflow (kcfs)'] = newUpTouple[i]['Inflow (kcfs)']
            newUpTouple[i]['Elevation (ft)'] = newDownTouple[i]['Tailwater Elevation (ft)']

    #check for dam 4 being breached (different scenario because there is no next dam to update)
    if breachTouple[3]:
        newUpTouple[3]['Outflow (kcfs)'] = newUpTouple[3]['Inflow (kcfs)']
        newDownTouple[3]['Outflow (kcfs)'] = newUpTouple[3]['Inflow (kcfs)']
        newUpTouple[3]['Elevation (ft)'] = newDownTouple[3]['Tailwater Elevation (ft)']

    return(newUpTouple,newDownTouple)