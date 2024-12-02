import numpy as np
import pandas as pd
import copy

def SpillAdjuster(up, down, minSpill):
    newUpTouple = [df.copy() for df in up]
    newDownTouple = [df.copy() for df in down]

    for i in range(4):
        for j in range(len(up[0]['Date'])):
            if up[i].loc[j,'Spill Percent (%)'] < minSpill:
                newUpTouple[i].loc[j,'Spill Percent (%)'] = minSpill
                newDownTouple[i].loc[j,'Spill Percent (%)'] = minSpill
                newUpTouple[i].loc[j,'Spill (kcfs)'] = up[i].loc[j,'Outflow (kcfs)']*minSpill/100
                newDownTouple[i].loc[j,'Spill (kcfs)'] = down[i].loc[j,'Outflow (kcfs)']*minSpill/100


    return(newUpTouple,newDownTouple)