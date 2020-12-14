import math
import random as rd
import pandas as pd

#Constantes
N = 1000
T = 100
mutation = 0.55
maxGen = 40
select_i = 5

I = 50

class solution:
    def __init__(self, x):
        self.x = x
        self.mutate()
        self.check_lim()
        self.fitness = self.fit(x)
    def fit(self, x):
        fitness = self.f() * self.check_restritions(x)
        return fitness

    #checando as restrições g1, g2, e g3, cada uma delas adiciona um peso no fitness final caso não seja satisfeita
    def check_restritions(self, x):
        peso = 1
        if(not (self.g1() <= 0 )):
            peso = peso + 10000000000
        if(not (self.g2() <= 0) ):
            peso = peso + 10000000000
        if(not (self.g3() <= 0) ):
            peso = peso + 10000000000 
        if(not (self.g4() <= 0) ):
            peso = peso + 10000000000
        return peso

    def mutate(self):
        u = rd.uniform(0, 1)
        for i in range(4):
            if(rd.uniform(0, 1) > mutation):
                if(i < 2):
                    self.x[i] = self.x[i] + rd.randint(-5, 5)
                else:
                    pert = u * (190) * ((2*u) - 1)
                    self.x[i] = self.x[i] + pert
    
    def check_lim(self):
        for i in range(4):
            if(i < 2):
                if(self.x[i] <= 0):
                    self.x[i] = 1
                elif(self.x[i] > 1600):
                    self.x[i] = 1600
            else:
                if(self.x[i] <= 10):
                    self.x[i] = 10
                elif(self.x[i] > 200):
                    self.x[i] = 200
    
    def g1 (self):
        return (-(self.x[0]*0.0625) + 0.0193*self.x[2])

    def g2 (self):
        return (-(self.x[1]*0.0625) + 0.00954*self.x[2])

    def g3 (self):
        return ((-(math.pi*(self.x[2]**2)*self.x[3]) - (4/3)*math.pi*(self.x[2]**3)) + 1296000)

    def g4 (self):
        return (self.x[3] - 240)

    def f(self):
        return (0.6224*(self.x[0]*0.0625)*self.x[2]*self.x[3] + 1.7781*(self.x[1]*0.0625)*(self.x[2]**2) + 3.1661*((self.x[0]*0.0625)**2)*self.x[3]+19.84*((self.x[0]*0.0625)**2)*self.x[2])


def generate():
    l = []
    x1 = rd.randint(1, 1601)
    l.append(x1)
    x2 = rd.randint(1, 1601)
    l.append(x2)
    x3 = rd.uniform(10, 200)
    l.append(x3)
    x4 = rd.uniform(10, 200)
    l.append(x4)
    return l

#Gera uma população de tamanho n aleatoriamente de acordo com o limites do problema
def generate_population(n):
    r = []
    for i in range(n):
        r.append(solution(generate()))
    return r

#Cruzamento para uma nova geração
def breed_generation(pop):
    global gen
    gen = gen + 1
    pop.sort(key=lambda x: x.fitness, reverse=False)
    breeded_generation = pop[0:T]
    for i in range(N - T):
        p = []
        p.append(select(pop))
        p.append(select(pop))
        breeded_generation.append(breed(p[0],p[1]))
        p.clear()
    return breeded_generation

#selecao por torneio com n=3
def select(pop):
    selection = []
    for i in range(select_i):
        selection.append(rd.choice(pop))
    selection.sort(key=lambda x: x.fitness, reverse=False)
    return selection[0]

#Cruzamento linear
def breed(parent1, parent2):
    global best, oldBest, bestx
    child = solution(set_genes(parent1, parent2))
    if(child.fitness < best):
        oldBest = best
        best = child.fitness
        bestx  = child.x
    return child

def set_genes(p1, p2):
    np1 = 0
    np2 = 0
    genes = []
    for i in range(4):
        if(rd.uniform(0, 1) >= 0.5):
            np1 = np1 + 1
            if (np1 >= 2):
                genes.append(p2.x[i])
                np2 = np2 + 1
            else:
                genes.append(p1.x[i])            
        else:
            np2 = np2 + 1
            if (np2 >= 2):
                genes.append(p1.x[i])
                np1 = np1 + 1
            else:
                genes.append(p2.x[i])
    return genes

def g1 (x):
    return (-(x[0]*0.0625) + 0.0193*x[2])
def g2 (x):
    return (-(x[1]*0.0625) + 0.00954*x[2])
def g3 (x):
    return ((-(math.pi*(x[2]**2)*x[3]) - (4/3)*math.pi*(x[2]**3)) + 1296000)
def g4 (x):
    return (x[3] - 240)

best = 100000000
oldBest = 10000000000
globalBest = 10000000000
globalBestx = [0,0,0,0]
gen = 0
bestx = [0, 0]
best_genetic_list  = []
for i in range(I):
    best = 100000000
    oldBest = 1000000000
    gen = 0
    pop = generate_population(N)
    while (maxGen > gen):
        pop = breed_generation(pop)
        if(best < globalBest):
            globalBest = best
            globalBestx = bestx
    best_genetic_list.append(best)
    print(best)


best_genetic_series = pd.Series(best_genetic_list)

print(best_genetic_series.describe())

print(best)
print(bestx)
