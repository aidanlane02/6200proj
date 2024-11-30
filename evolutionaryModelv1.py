import numpy as np
import pandas as pd
from HydroModelv2 import hydroPowerList
from HydroModelv2 import hydroPowerList
from MinSpillAdjuster import SpillAdjuster
from HydroFlowAdjustment import flowAdjustment
from WTT import WTT

#set up testing data
graniteUp = pd.read_csv(r'Data\LowerGraniteForebay.csv', delimiter=',')
graniteDown = pd.read_csv(r'Data\LowerGraniteTailwater.csv', delimiter=',')
gooseUp = pd.read_csv(r'Data\LittleGooseForebay.csv', delimiter=',')
gooseDown = pd.read_csv(r'Data\LittleGooseTailwater.csv', delimiter=',')
monumentalUp = pd.read_csv(r'Data\LowerMonumentalForebay.csv', delimiter=',')
monumentalDown = pd.read_csv(r'Data\LowerMonumentalTailwater.csv', delimiter=',')
iceUp = pd.read_csv(r'Data\IceHarborForebay.csv', delimiter=',')
iceDown = pd.read_csv(r'Data\IceHarborTailwater.csv', delimiter=',')
upTouple = [graniteUp,gooseUp,monumentalUp,iceUp]
downTouple = [graniteDown,gooseDown,monumentalDown,iceDown]

#DAM BREACH STATUS
graniteBreach = False
gooseBreach = False
monumentalBreach = False
iceBreach = False
breachTouple = [graniteBreach,gooseBreach,monumentalBreach,iceBreach] #will change for the 16 scenarios

#dam power capacities
graniteCap = 810
gooseCap = 810
monumentalCap = 810
iceCap = 603
maxPowerTouple = [graniteCap,gooseCap,monumentalCap,iceCap]

#random values for decision variables
minSpill = np.random()*100 #might lower max spill range



#find baseline energy production
baselineEnergy = sum(hydroPowerList(upTouple,downTouple,maxPowerTouple)['Total Energy (MWh)'])


#impliment evolutionary algorithm