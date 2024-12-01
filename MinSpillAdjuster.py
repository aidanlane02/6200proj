import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # Turn off the warning
def SpillAdjuster(upTouple, downTouple, minSpill):
    newUpTouple = upTouple
    newDownTouple = downTouple

    for i in range(4):
        for j in range(len(upTouple[0]['Date'])):
            upTouple[i].loc[j,'Spill Percent (%)'] = minSpill
            downTouple[i].loc[j,'Spill Percent (%)'] = minSpill
            upTouple[i].loc[j,'Spill (kcfs)'] = upTouple[i].loc[j,'Outflow (kcfs)']*minSpill/100
            downTouple[i].loc[j,'Spill (kcfs)'] = downTouple[i].loc[j,'Outflow (kcfs)']*minSpill/100


    return(newUpTouple,newDownTouple)