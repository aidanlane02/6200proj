import numpy as np
import pandas as pd
from HydroModelv2 import hydroPowerList
from freightModel import freightCost
pd.options.mode.chained_assignment = None  # Turn off the warning
#currently only works for single year I think
def cost(upTouple, downTouple, breachTouple, maxPowerTouple, baseEnergy, energyCost = 75, breachCost = 28504053.66):
    totCost = 0
    
    #cost of energy lost from hydropower
    newEnergy = sum(hydroPowerList(upTouple,downTouple,maxPowerTouple)['Total Energy (MWh)'])
    energyReplacementCost = (baseEnergy - newEnergy)*energyCost #energy cost comes from LCOE of onshore wind. Eastern Washington is considered a viable location for onshore wind 
                                                                #but wind velocities are lower than places like the great planes so I used the upper end of the range as a safe
                                                                #estimate ($23/MWh - $75/MWh)
    #cost of dam breaching
    totBreachCost = sum(breachTouple)*breachCost*0.09 #annualization of the costs over the next 32 years (useful life) with a WACC of 8.3%

    #cost of transportation
    transportCost = freightCost(breachTouple)

    totCost = energyReplacementCost + totBreachCost + transportCost
    return totCost

