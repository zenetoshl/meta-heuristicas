import random as rd
import pandas as pd
import math

#constantes do algoritmo
final_temp = .1
beta = 0.005

def quality_1(vars):
    x = vars[0]
    y = vars[1]
    return ((-(y+47)*math.sin(math.sqrt(abs((x/2) + (y + 47))))) - (x * math.sin(math.sqrt(abs(x- (y+47))))))

def quality_2(vars):
    x = vars[0]
    y = vars[1]
    return (-0.0001 * ((abs(math.sin(x) * math.sin(y)*math.exp(abs(100-((math.sqrt(((x**2)+(y**2)))/math.pi)))))+1)**0.1))

def init(lwrLim, uprLim):
    l = []
    for i in range (len(lwrLim)):
        x = rd.uniform(lwrLim[i], uprLim[i])
        l.append(x)
    return l

def adjust(vars, lwrLim, uprLim):
    temp_vars = vars.copy()
    for _ in range(1):
        i = rd.randint(0, len(temp_vars)-1)
        ratio = 1 / 100
        noiselim = (uprLim[i] - lwrLim[i]) / ratio
        noise = rd.uniform(-noiselim, noiselim)
        tmp_var = temp_vars[i] + noise
        while(tmp_var <= lwrLim[i] or tmp_var >= uprLim[i] ):
            noise = rd.uniform(-noiselim, noiselim)
            tmp_var = temp_vars[i] + noise
        temp_vars[i] = tmp_var
    return temp_vars

def simulated_annealing(lwrLim, uprLim, quality = quality_1):
    initial_temp = 90  
    current_temp = initial_temp
    current_state = init(lwrLim, uprLim)
    solution = current_state

    while current_temp > final_temp:
        newSolution = adjust(solution, lwrLim, uprLim)
        cost_diff = quality(solution) - quality(newSolution)

        if cost_diff > 0:
            solution = newSolution
        else:
            if rd.uniform(0, 1) < math.exp(cost_diff / current_temp):
                solution = newSolution
        current_temp = current_temp/(1 + (beta*current_temp))
    return solution

resultList  = []
solutionsList = []
best = 0
for i in range(30):
    solution = simulated_annealing([-512, -512], [512, 512], quality_1)
    if(i == 0):
        best = solution
    else:
        if(quality_2(solution) < quality_2(best)):
            best = solution
    solutionsList.append(solution)
    resultList.append(quality_1(solution))

resultSeries = pd.Series(resultList)
print("1:")
print(resultSeries.describe())
print('variaveis de decisão da melhor solução: ', best)

resultList  = []
solutionsList = []
best = 0
for i in range(30):
    solution = simulated_annealing([-10, -10], [10, 10], quality_2)
    if(i == 0):
        best = solution
    else:
        if(quality_2(solution) < quality_2(best)):
            best = solution
    solutionsList.append(solution)
    resultList.append(quality_2(solution))

resultSeries = pd.Series(resultList)
print("2:")
print(resultSeries.describe())
print('variaveis de decisão da melhor solução: ', best)