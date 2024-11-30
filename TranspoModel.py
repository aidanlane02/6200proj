AtoCL = 197.80+74.7                 # miles
LtoCL = AtoCL+35.3                  # miles
cost2015 = 5.1/100                  # dollars per ton mile https://www.cbo.gov/sites/default/files/114th-congress-2015-2016/workingpaper/50049-Freight_Transport_Working_Paper-2.pdf
cost2024 = 0.071                    # dollars per ton mile with inflation
internalV = 12.025*2.352*2.393      # 12.025m long x 2.352m wide x 2.393m high, m^3
waterDensity = 999.85               # kg/m^3 at 45 degrees fahrenheit
weight = waterDensity*internalV+3750    # 3,750 is the empty weight in kg
maxweight = 26300
availableV = (maxweight-3750)/waterDensity
#print(availableV)
gallontometer3 = 0.0037854118
GalperSalmon = 70
MperSalmon = GalperSalmon*gallontometer3
#print(MperSalmon)
#print(availableV/MperSalmon)
dailyLiG = 631                      # Salmon to be transported each day
dailyLoG = 743                      # Salmon to be transported each day
requiredVLoGBreached = MperSalmon*dailyLoG
requiredVLoGNotBreached = MperSalmon*dailyLiG

requiredCarsLoGBreached = requiredVLoGBreached/availableV
requiredCarsLoGNotBreached = requiredVLoGNotBreached/availableV

WeightLoGBreached = requiredCarsLoGBreached*maxweight           #kg
WeightLoGNotBreached = requiredCarsLoGNotBreached*maxweight     #kg

costDailyLoGBreached = WeightLoGBreached*LtoCL*cost2024
costDailyLoGNotBreached = WeightLoGNotBreached*AtoCL*cost2024

print(costDailyLoGBreached)
print(costDailyLoGNotBreached) 