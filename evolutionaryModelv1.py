import numpy as np
import pandas as pd
from HydroModelv2 import hydroPowerList
from MinSpillAdjuster import SpillAdjuster
from HydroFlowAdjustment import flowAdjustment
from WTT import WTT
from SARmodelv3 import SAR_model
from economicsModelv1 import cost
import copy

#SETUP FOR EA
#set up testing data
graniteUpTraining = pd.read_csv(r'Data\TrainingData\GraniteUpTraining.csv', delimiter=',')
graniteDownTraining = pd.read_csv(r'Data\TrainingData\GraniteDownTraining.csv', delimiter=',')
gooseUpTraining = pd.read_csv(r'Data\TrainingData\GraniteUpTraining.csv', delimiter=',')
gooseDownTraining = pd.read_csv(r'Data\TrainingData\GooseDownTraining.csv', delimiter=',')
monumentalUpTraining = pd.read_csv(r'Data\TrainingData\MonumentalUpTraining.csv', delimiter=',')
monumentalDownTraining = pd.read_csv(r'Data\TrainingData\MonumentalDownTraining.csv', delimiter=',')
iceUpTraining = pd.read_csv(r'Data\TrainingData\IceUpTraining.csv', delimiter=',')
iceDownTraining = pd.read_csv(r'Data\TrainingData\IceDownTraining.csv', delimiter=',')
upTouple = [graniteUpTraining,gooseUpTraining,monumentalUpTraining,iceUpTraining]
downTouple = [graniteDownTraining,gooseDownTraining,monumentalDownTraining,iceDownTraining]

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



#EA
#choose data year for evaluation
def dataYear(upTouple,downTouple,year):
    filtered_downTouple = []
    filtered_upTouple = []
    for i in range(4):
        upTouple[i]['Date'] = pd.to_datetime(upTouple[i]['Date'])
        downTouple[i]['Date'] = pd.to_datetime(downTouple[i]['Date'])
        newUp = upTouple[i][upTouple[i]['Date'].dt.year==year]
        newDown = downTouple[i][downTouple[i]['Date'].dt.year==year]
        newUp = newUp.reset_index(drop=True)
        newDown = newDown.reset_index(drop=True)
        filtered_downTouple.append(newDown)
        filtered_upTouple.append(newUp)
    return(filtered_upTouple,filtered_downTouple)

year = 2019 #can change
(upTouple,downTouple) = dataYear(upTouple,downTouple,year)

#find baseline energy production
baselineEnergy = sum(hydroPowerList(upTouple,downTouple,maxPowerTouple)['Total Energy (MWh)'])

#idk how anything below works (it currently doesn't)
import itertools
from deap import base, creator, tools, algorithms
import random
import matplotlib.pyplot as plt
from functools import partial


# Define multi-objective fitness
creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))  # Minimize both SAR and Economic Impact
creator.create("Individual", list, fitness=creator.FitnessMulti)

# Toolbox
toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, 0, 100)  # Spill range: 0 to 100
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selNSGA2)

pd.options.mode.chained_assignment = None  #turn off warnings so I can find errors

# Define dynamic evaluation function
def evaluate(individual, breachTouple, upTouple, downTouple, maxPowerTouple, baselineEnergy, sar_model, econ_model):
    minSpill = individual[0]  # min spill value

    # Adjust touples for spill and breach
    (newUpTouple, newDownTouple) = SpillAdjuster(copy.deepcopy(upTouple), copy.deepcopy(downTouple), minSpill)
    (newUpTouple, newDownTouple) = flowAdjustment(newUpTouple, newDownTouple, breachTouple)

    # Evaluate SAR model
    sar_result = sar_model(newDownTouple, breachTouple)
    # Evaluate economic model
    econ_result = econ_model(newUpTouple, newDownTouple, breachTouple, maxPowerTouple, baselineEnergy)
    
    # Return fitness as a tuple, ensuring it's hashable
    return (sar_result.item(), econ_result)

#copy code for NSGA2 because it can't be imported
def run_nsga2(breachTouple, upTouple, downTouple, maxPowerTouple, baselineEnergy, sar_model, econ_model):
    # Dynamically adapt the evaluation function
    eval_func = partial(
        evaluate,
        breachTouple=breachTouple,
        upTouple=upTouple,
        downTouple=downTouple,
        maxPowerTouple=maxPowerTouple,
        baselineEnergy=baselineEnergy,
        sar_model=sar_model,
        econ_model=econ_model
    )
    toolbox.register("evaluate", eval_func)

    # Create population
    population = toolbox.population(n=5) #change for speed

    # Run NSGA-II
    algorithms.eaMuPlusLambda(
        population=population,
        toolbox=toolbox,
        mu=5, #change for speed
        lambda_=10, #change for speed
        cxpb=0.65,
        mutpb=0.25,
        ngen=3, #change for speed
        stats=None,
        halloffame=None,
        verbose=False,
    )

    # Extract Pareto front
    pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]
    return pareto_front

# Dam Breach Scenarios
dams = ["LGR", "LGS", "LMN", "ICE"]
combinations = list(itertools.product([0, 1], repeat=len(dams)))  # All dam breach combinations

# Run NSGA-II for each scenario
pareto_results = []
for scenario in combinations:
    dams_destroyed = [dams[i] for i in range(len(dams)) if scenario[i] == 1]
    pareto_front = run_nsga2(scenario, upTouple, downTouple, maxPowerTouple, baselineEnergy, SAR_model, cost)

    pareto_results.append({
        "scenario": dams_destroyed,
        "pareto_front": [(ind[0], ind.fitness.values) for ind in pareto_front]
    })

# Visualize Pareto Fronts
print(pareto_results[0]['pareto_front'])

'''
for result in pareto_results:
    scenario = result["scenario"]
    pareto_front = result["pareto_front"]

    sar_values = [fitness[0] for _, fitness in pareto_front]
    econ_values = [fitness[1] for _, fitness in pareto_front]

    plt.figure(figsize=(8, 6))
    plt.scatter(econ_values, sar_values, label=f"Scenario {scenario}")
    plt.title(f"Pareto Front - Scenario {scenario}")
    plt.xlabel("Economic Impact")
    plt.ylabel("SAR")
    plt.legend()
    plt.grid()
    plt.show()
    '''