import numpy as np
import pandas as pd

def SpillAdjuster(upTouple, downTouple, minSpill):
    newUpTouple = upTouple
    newDownTouple = downTouple

    for i in range(4):
        for j in range(len(upTouple['Date'])):
            upTouple[i]['Spill Percent (%)'][j] = minSpill
            downTouple[i]['Spill Percent (%)'][j] = minSpill
            upTouple[i]['Spill (kcfs)'][j] = upTouple[i]['Outflow (kcfs)'][j]*minSpill/100
            downTouple[i]['Spill (kcfs)'][j] = downTouple[i]['Outflow (kcfs)'][j]*minSpill/100


    return(newUpTouple,newDownTouple)