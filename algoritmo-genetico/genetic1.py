import math
import random as rd
import pandas as pd

#Constantes
P = 2
sig = 2
L = 100
N = 1000
I = 500
T = 100
best = 100000
oldBest = 10000000
globalBest = 10000000
gen = 0
maxGen = 1000
bestX = [0, 0]

#obj solution, x é o vetor de decisão e fitness é o fitness calculado para o vetor
class solution:
    def __init__(self, x):
        self.x = x
        self.mutate()
        self.check_lim()
        self.fitness = self.fit(x)
        
    def fit(self, x):
        x1 = x[0]
        x2 = x[1]
        fitness = self.f() * self.check_restritions(x)
        return fitness

    #checando as restrições g1, g2, e g3, cada uma delas adiciona um peso no fitness final caso não seja satisfeita
    def check_restritions(self, x):
        x1 = x[0]
        x2 = x[1]
        multiplier = 0
        if(not (self.g1() <= 0 )):
            multiplier = multiplier + 1000000
        if(not (self.g2() <= 0) ):
            multiplier = multiplier + 1000000
        if(not (self.g3() <= 0) ):
            multiplier = multiplier + 1000000
        if(multiplier == 0):
            multiplier = 1
        return multiplier

    def mutate(self):
        if(rd.uniform(0, 1) > 0.98):
            for i in range(2):
                u = rd.uniform(0, 1)
                pert = 0.1 * ((2*u) - 1)
                self.x[i] = self.x[i] + pert
    
    def check_lim(self):
        for i in range(2):
            if(self.x[i] <= 0):
                self.x[i] = 0.00001
            elif(self.x[i] > 1):
                self.x[i] = 1

    def g1 (self):
        return ((((math.sqrt(2) * self.x[0] + self.x[1])/(math.sqrt(2)*(self.x[0]**2) + (2*self.x[0]*self.x[1]))) * P) - sig)

    def g2 (self):
        return ((((self.x[1])/(math.sqrt(2)*(self.x[0]**2) + (2*self.x[0]*self.x[1]))) * P) - sig)

    def g3 (self):
        return ((((1)/(math.sqrt(2)*(self.x[1]) + self.x[0])) * P) - sig)

    def f(self):
        return ((2 * (math.sqrt(2) * self.x[0]) + self.x[1]) * L)


#Gera umindividuo aleatório de acordo com os limites do problema
def generate(lim):
    l = []
    for i in range (2):
        x = rd.uniform(lim[0], lim[1])
        l.append(x)
    return l

#Gera uma população de tamanho n aleatoriamente de acordo com o limites do problema
def generate_population(n):
    r = []
    for i in range(n):
        r.append(solution(generate([0,1])))
    return r

#Cruzamento para uma nova geração
def breed_generation(pop):
    global gen
    gen = gen + 1
    pop.sort(key=lambda x: x.fitness, reverse=False)
    pop = pop [0:int(N/2)]
    breeded_generation = pop[0:T]
    for i in range(N - T):
        p = []
        p.append(select(pop))
        p.append(select(pop))
        if(p[0].fitness > p[1].fitness):
            breeded_generation.append(test_breed(p[1],p[0]))
        else:
            breeded_generation.append(test_breed(p[0],p[1]))
        p.clear()
    return breeded_generation

#selecao por torneio com n=3
def select(pop):
    selection = []
    selection.append(rd.choice(pop))
    selection.append(rd.choice(pop))
    selection.append(rd.choice(pop))
    selection.sort(key=lambda x: x.fitness, reverse=False)
    return selection[0]

def test_breed(parent1, parent2):
    global best, oldBest, globalBest, bestX
    x = []
    if(parent1.x[0] < parent2.x[0]):
        x.append(rd.uniform(parent1.x[0], parent2.x[0]))
    else:
        x.append(rd.uniform(parent2.x[0], parent1.x[0]))
    if(parent1.x[1] < parent2.x[1]):
        x.append(rd.uniform(parent1.x[1], parent2.x[1]))
    else:
        x.append(rd.uniform(parent2.x[1], parent1.x[1]))
    child = solution(x)
    if(child.fitness < best):
        oldBest = best
        best = child.fitness
        if(best < globalBest):
            globalBest = best
            bestX = child.x
    return child

#Cruzamento linear
def breed(parent1, parent2):
    global best, oldBest, globalBest, bestX
    child = solution([parent1.x[0], parent2.x[1]])
    if(child.fitness < best):
        oldBest = best
        best = child.fitness
        if(best < globalBest):
            globalBest = best
            bestX = child.x
    return child

best = 100000
oldBest = 1000000
pop = generate_population(N)
best_genetic_list  = []
for i in range(I):
    best = 100000
    oldBest = 1000000
    gen = 0
    pop = generate_population(N)
    while ((oldBest - best) > 0.00001 and maxGen > gen):
        pop = breed_generation(pop)
    best_genetic_list.append(best)
    print(best)
min  = solution([0.7886751284,  0.4082483080])
print(min.fitness)
print()
print(bestX)

best_genetic_series = pd.Series(best_genetic_list)

print(best_genetic_series.describe())