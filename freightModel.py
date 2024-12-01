import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # Turn off the warning
def freightCost(breachTouple):
    AtoCL = 197.80+74.7 #Almota to Cascade Locks distance
    LtoCL = AtoCL+35.3 #Lewiston to Cascade Locks distance
    unitCost = 0.071 #$/ton mile

    LewistonCost = 21.56 #$/ton
    AlmotaCost = 20.66 #$/ton
    DallesCost = 14.22 #$/ton, this is cascade locks

    yearlyWeight = 3508730

    extraCost = 0

    if(breachTouple[0]):
        extraUnitCost = DallesCost-LewistonCost+LtoCL*unitCost
        extraCost = extraUnitCost*yearlyWeight
    elif(breachTouple[1],breachTouple[2],breachTouple[3]):
        extraUnitCost = DallesCost-2*LewistonCost+AlmotaCost+LtoCL*unitCost
        extraCost = extraUnitCost*yearlyWeight
    else:
        extraUnitCost = 0
        extraCost = extraUnitCost*yearlyWeight

    return(extraCost)
