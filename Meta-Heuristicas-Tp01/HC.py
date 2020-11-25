import random as rd
import pandas as pd
import math

#constantes da função
iLimit = 1000 + 10
nLimit = 100


exLimit = 30


def quality_2(vars):
    x = vars[0]
    y = vars[1]
    return ((-(y+47)*math.sin(math.sqrt(abs((x/2) + (y + 47))))) - (x * math.sin(math.sqrt(abs(x- (y+47))))))

def quality_1(vars):
    x = vars[0]
    return x**2

def adjust(vars, lwrLim, uprLim, n_repeated):
    temp_vars = vars.copy()
    for _ in range(1):
        i = rd.randint(0, len(temp_vars)-1)
        ratio = (iLimit - n_repeated) / 10
        noiselim = (uprLim[i] - lwrLim[i]) / ratio
        noise = rd.uniform(-noiselim, noiselim)
        tmp_var = temp_vars[i] + noise
        while(tmp_var <= lwrLim[i] or tmp_var >= uprLim[i] ):
            noise = rd.uniform(-noiselim, noiselim)
            tmp_var = temp_vars[i] + noise
        temp_vars[i] = tmp_var
    return temp_vars

def init(lwrLim, uprLim):
    l = []
    for i in range (len(lwrLim)):
        x = rd.uniform(lwrLim[i], uprLim[i])
        l.append(x)
    return l

def compare(r, s):
    x = r - s
    return x < 0

def hc(lwrLim, uprLim, quality = quality_2):
    s_decision = init(lwrLim, uprLim)
    s_solution = 0
    i = 0
    while i < iLimit - 10:
        r_decision = adjust(s_decision, lwrLim, uprLim, i)
        s_solution = quality(s_decision)
        r_solution = quality(r_decision)
        if compare(r_solution, s_solution):
            s_solution = r_solution
            s_decision = r_decision
            i = 0
        else:
            i = i + 1
    return s_solution

def sahc(lwrLim, uprLim, quality = quality_2):
    s_decision = init(lwrLim, uprLim)
    s_solution = 0
    i = 0
    while i < iLimit - 10:
        r_decision = adjust(s_decision, lwrLim, uprLim, i)
        s_solution = quality(s_decision)
        r_solution = quality(r_decision)
        for j in range(nLimit-1):
            w_decision = adjust(s_decision, lwrLim, uprLim, 200)
            w_solution = quality(w_decision)
            if compare(w_solution, r_solution):
                r_solution = w_solution
                r_decision = w_decision
        if compare(r_solution, s_solution):
            s_solution = r_solution
            s_decision = r_decision
            i = 0
        else:
            i = i + 1
    return s_solution

#1
resulthcList  = []
resultsahcList  = []
for i in range(exLimit):
    resulthcList.append(hc([-10], [10], quality_1))
    resultsahcList.append(sahc([-10], [10], quality_1))

resultHcSeries = pd.Series(resulthcList)
resultSahcSeries = pd.Series(resultsahcList)
print("HC:")
print(resultHcSeries.describe())
print("SAHC:")
print(resultSahcSeries.describe())

#2
resulthcList  = []
resultsahcList  = []
for i in range(exLimit):
    resulthcList.append(hc([-512, -512], [512, 512]))
    resultsahcList.append(sahc([-512, -512], [512, 512]))

resultHcSeries = pd.Series(resulthcList)
resultSahcSeries = pd.Series(resultsahcList)
print("HC:")
print(resultHcSeries.describe())
print("SAHC:")
print(resultSahcSeries.describe())

#3
resulthcList  = []
resultsahcList  = []
for i in range(exLimit):
    resulthcList.append(hc([511, 404], [512, 405]))
    resultsahcList.append(sahc([511, 404], [512, 405]))

resultHcSeries = pd.Series(resulthcList)
resultSahcSeries = pd.Series(resultsahcList)
print("HC:")
print(resultHcSeries.describe())
print("SAHC:")
print(resultSahcSeries.describe())