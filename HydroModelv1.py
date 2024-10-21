import numpy as np

def hydropower(vol, height, maxPower, efficiency = 0.9): #might adjust either efficiency or how height is calculated to match actual output
    #returns the amount of power generated in MW
    m3s = 28.316847*vol
    height_m = height*0.3048
    g = 9.81
    denWater = 997
    hrPerDay = 24
    power_W= m3s*height_m*denWater*g*efficiency
    power_MW = min(power_W/10**6,maxPower)

    if power_MW > maxPower:
        power_MW = maxPower
    elif power_MW < 0:
        power_MW = 0
        
    energy_MWh = power_MW * hrPerDay
    return(power_MW,energy_MWh)
