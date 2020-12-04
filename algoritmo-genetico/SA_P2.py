import random as rd
import pandas as pd
import math

#constantes do algoritmo
final_temp = .1
beta = 0.005

P = 2
sig = 2
L = 100
I = 50

def quality_1(vars):
    x = vars[0]
    y = vars[1]
    return ((-(y+47)*math.sin(math.sqrt(abs((x/2) + (y + 47))))) - (x * math.sin(math.sqrt(abs(x- (y+47))))))

def quality_2(vars):
    x = vars[0]
    y = vars[1]
    return (-0.0001 * ((abs(math.sin(x) * math.sin(y)*math.exp(abs(100-((math.sqrt(((x**2)+(y**2)))/math.pi)))))+1)**0.1))

def g1 (x):
    return (-x[0]*0.0625 + 0.0193*x[2])
def g2 (x):
    return (-(x[1]*0.0625) + 0.00954*x[2])
def g3 (x):
    return ((-(math.pi*(x[2]**2)*x[3]) - (4/3)*math.pi*(x[2]**3)) + 1296000)
def g4 (x):
    return (x[3] - 240)
def f(x):
    return (0.6224*x[0]*0.0625*x[2]*x[3] + 1.7781*(x[1]*0.0625)*(x[2]**2) + 3.1661*((x[0]*0.0625)**2)*x[3]+19.84*((x[0]*0.0625)**2)*x[2]) * check_restritions(x)

def check_restritions(x):
    peso = 1
    if(not (g1(x) <= 0 )):
        peso = peso + 10000000
    if(not (g2(x) <= 0) ):
        peso = peso + 10000000
    if(not (g3(x) <= 0) ):
        peso = peso + 10000000
    if(not (g4(x) <= 0) ):
        peso = peso + 10000000
    return peso

def init(lwrLim, uprLim):
    l = []
    for i in range (len(lwrLim)):
        if(i < 2):
            x = rd.randint(lwrLim[i], uprLim[i])
        else:
            x = rd.uniform(lwrLim[i], uprLim[i])
        l.append(x)
    return l

def adjust(vars, lwrLim, uprLim):
    temp_vars = vars.copy()
    for _ in range(1):
        i = rd.randint(0, len(temp_vars)-1)
        noiselim = (uprLim[i] - lwrLim[i]) * 0.5
        if(i < 2):
            noise = rd.randint(int(-noiselim), int(noiselim) + 1)
        else:
            noise = rd.uniform(-noiselim, noiselim)
        tmp_var = temp_vars[i] + noise
        while(tmp_var <= lwrLim[i] or tmp_var >= uprLim[i] ):
            if(i < 2):
                noise = rd.randint(int(-noiselim), int(noiselim) + 1)
            else:
                noise = rd.uniform(-noiselim, noiselim)
            tmp_var = temp_vars[i] + noise
        temp_vars[i] = tmp_var
    return temp_vars

def simulated_annealing(lwrLim, uprLim, quality = f):
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
for i in range(50):
    solution = simulated_annealing([0, 0, 10, 10], [1600, 1600, 200, 200], f)
    if(i == 0):
        best = solution
    else:
        if(f(solution) < f(best)):
            best = solution
    solutionsList.append(solution)
    resultList.append(f(solution))

resultSeries = pd.Series(resultList)
print("1:")
print(resultSeries.describe())
print('variaveis de decisão da melhor solução: ', best)
