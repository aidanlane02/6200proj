import numpy as np
import pandas as pd
from HydroModelv2 import hydroPowerList
from freightModel import freightCost

#currently only works for single year I think
def cost(upTouple, downTouple, breachTouple, maxPowerTouple, baseEnergy, energyCost = 0.0667, breachCost = 28504053.66):
    totCost = 0
    
    #cost of energy lost from hydropower
    newEnergy = sum(hydroPowerList(upTouple,downTouple,maxPowerTouple)['Total Energy (MWh)'])
    energyReplacementCost = (baseEnergy - newEnergy)*energyCost

    #cost of dam breaching
    totBreachCost = sum(breachTouple)*breachCost

    #cost of transportation
    transportCost = freightCost(breachTouple)

    totCost = energyReplacementCost + totBreachCost + transportCost
    return totCost

