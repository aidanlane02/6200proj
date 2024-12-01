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

#find baseline energy production
baselineEnergy = (hydroPowerList(upTouple,downTouple,maxPowerTouple))
print(baselineEnergy)


#train model in this file
#region
import statsmodels.api as sm
import statsmodels.formula.api as smf

data = pd.read_csv(r'Data\TrainingData\GLMTraining.csv', delimiter=',')

#convert SAR from percent to decimal
data['SAR'] = data['SAR']/100

glm_data = data.drop(columns=['Year','Species']) 

#set limits to epsilon to avoid extreme value errors
epsilon = 1e-10
glm_data['SAR'] = glm_data['SAR'].clip(lower=epsilon, upper=1 - epsilon)

formula = 'SAR ~ PH + FTD + WTT + Transport * FTD'

model = smf.glm(formula=formula, data=glm_data, family=sm.families.Binomial())
result = model.fit()

#endregion



#idk how anything below works (it currently doesn't)
# Example: Precomputing dam effects for 16 combinations
import itertools

# List of dams
dams = ["Dam1", "Dam2", "Dam3", "Dam4"]  # Add actual dam names
combinations = list(itertools.product([0, 1], repeat=len(dams)))  # 0: not breached, 1: breached

dam_scenarios = []
for combo in combinations:
    # Simulate the effects of each dam breach combination
    breached = [dams[i] for i in range(len(dams)) if combo[i] == 1]
    dam_scenarios.append({
        "breached_dams": breached,
        # Placeholder: Adjust these based on your model logic
        "updated_dams_passed": calculate_dams_passed(breached),  
        "updated_water_speed": calculate_water_speed(breached)  
    })


from deap import base, creator, tools, algorithms
import random

# Define the problem for DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimize objective function
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, 0, S_max)  # Spill between 0 and S_max
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Define evaluation function
def evaluate(individual, sar_model, econ_model, dam_scenario):
    spill = individual[0]
    
    # Update SAR model with spill
    sar_result = sar_model(spill, dam_scenario["updated_water_speed"], dam_scenario["updated_dams_passed"])
    
    # Update economic model with spill
    econ_result = econ_model(spill, dam_scenario["breached_dams"])
    
    # Combine results into an objective value
    objective = combine_sar_and_econ(sar_result, econ_result)  # Define this based on your needs
    
    return (objective,)

toolbox.register("evaluate", evaluate, sar_model=trained_sar_model, econ_model=economic_model, dam_scenario=dam_scenarios[0])
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# Evolve a solution for each dam scenario
for scenario in dam_scenarios:
    # Update evaluation function for the current dam scenario
    toolbox.register("evaluate", evaluate, sar_model=trained_sar_model, econ_model=economic_model, dam_scenario=scenario)
    
    # Run the evolutionary algorithm
    population = toolbox.population(n=50)
    ngen = 100  # Number of generations
    cxpb = 0.5  # Crossover probability
    mutpb = 0.2  # Mutation probability
    
    algorithms.eaSimple(population, toolbox, cxpb, mutpb, ngen, verbose=True)
    
    # Find the best individual for this dam scenario
    best_ind = tools.selBest(population, k=1)[0]
    print(f"Best result for scenario {scenario['breached_dams']}: Spill = {best_ind[0]}, Objective = {best_ind.fitness.values[0]}")

def combine_sar_and_econ(sar_result, econ_result):
    # Weighted combination of fish SAR and economic model outputs
    w_sar = 0.7  # Weight for fish SAR
    w_econ = 0.3  # Weight for economic model
    return w_sar * sar_result + w_econ * econ_result
