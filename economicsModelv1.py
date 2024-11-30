import numpy as np
import pandas as pd
from HydroModelv2 import hydroPowerList


#currently only works for single year I think
def cost(upTouple, downTouple, breachTouple, maxPowerTouple, baseEnergy, transportationCost, energyCost, breachCost):
    totCost = 0
    
    #cost of energy lost from hydropower
    newEnergy = sum(hydroPowerList(upTouple,downTouple,maxPowerTouple)['Total Energy (MWh)'])
    energyReplacementCost = (baseEnergy - newEnergy)*energyCost

    #cost of dam breaching
    totBreachCost = sum(breachTouple)*breachCost

    #cost of transportation
    #tbd

    totCost = energyReplacementCost + totBreachCost
    return totCost

