import numpy as np

def flowAdjustment(upTouple, downTouple, breachTouple):
    newUpTouple = upTouple
    newDownTouple = downTouple

    #checks for first 3 dams breached, does not yet take into account lag time for water between dams
    for i in range(3):
        if breachTouple[i]:
            newUpTouple[i+1]['Inflow (kcfs)'] = newUpTouple[i+1]['Inflow (kcfs)'] + newUpTouple[i]['Inflow (kcfs)'] - newUpTouple[i]['Outflow (kcfs)'] - newUpTouple[i]['Spill (kcfs)']
            newDownTouple[i+1]['Inflow (kcfs)'] = newUpTouple[i+1]['Inflow (kcfs)'] + newUpTouple[i]['Inflow (kcfs)'] - newUpTouple[i]['Outflow (kcfs)'] - newUpTouple[i]['Spill (kcfs)']
            newUpTouple[i]['Outflow (kcfs)'] = newUpTouple[i]['Inflow (kcfs)']
            newDownTouple[i]['Outflow (kcfs)'] = newUpTouple[i]['Inflow (kcfs)']
            newDownTouple[i]['Tailwater Elevation (ft)'] = newUpTouple[i]['Elevation (ft)']

    #check for dam 4 being breached (different scenario because there is no next dam to update)
    if breachTouple[4]:
        newUpTouple[4]['Outflow (kcfs)'] = newUpTouple[4]['Inflow (kcfs)']
        newDownTouple[4]['Outflow (kcfs)'] = newUpTouple[4]['Inflow (kcfs)']
        newDownTouple[4]['Tailwater Elevation (ft)'] = newUpTouple[4]['Elevation (ft)']


    return(newUpTouple,newDownTouple)