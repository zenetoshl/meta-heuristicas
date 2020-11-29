import math
import random as rd
import pandas as pd

#Constantes
P = 2
sig = 2
L = 100
N = 10000
I = 20
T = 100
best = 10000000
bestx = [0, 0, 0, 0]
oldBest = 1000000000
gen = 0
maxGen = 4000

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
        multiplier = 1
        if(not (self.g1() <= 0 )):
            multiplier = multiplier + 10000000000
        if(not (self.g2() <= 0) ):
            multiplier = multiplier + 10000000000
        if(not (self.g3() <= 0) ):
            multiplier = multiplier + 10000000000
        if(not (self.g4() <= 0) ):
            multiplier = multiplier + 10000000000
        return multiplier

    def mutate(self):
        alpha = 500/(gen + 1)
        if (alpha < 0.80):
            alpha = 0.80
        elif (gen == 0):
            alpha = 1
        else:
            alpha = 0.99
            for i in range(4):
                if(rd.uniform(0, 1) > alpha):
                    u = rd.uniform(0, 1)
                    if(i < 2):
                        pert = 0.2 * (1600) * ((2*u) - 1)
                        self.x[i] = self.x[i] + int(pert)
                    else:
                        pert = 0.2 * (190) * ((2*u) - 1)
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
    pop = pop [0:int(N/2)]
    breeded_generation = pop[0:T]
    for i in range(N - T):
        p = []
        p.append(select(pop))
        p.append(select(pop))
        breeded_generation.append(test_breed(p[0],p[1]))
        p.clear()
    return breeded_generation

#selecao por torneio com n=3
def select(pop):
    selection = []
    selection.append(rd.choice(pop))
    selection.append(rd.choice(pop))
    selection.append(rd.choice(pop))
    selection.append(rd.choice(pop))
    selection.append(rd.choice(pop))
    selection.append(rd.choice(pop))
    selection.append(rd.choice(pop))
    selection.append(rd.choice(pop))
    selection.append(rd.choice(pop))
    selection.append(rd.choice(pop))
    selection.sort(key=lambda x: x.fitness, reverse=False)
    return selection[0]

def test_breed(parent1, parent2):
    global best, oldBest, bestx
    x = []
    if(parent1.x[0] < parent2.x[0]):
        x.append(rd.randint(parent1.x[0], parent2.x[0] + 1))
    else:
        x.append(rd.randint(parent2.x[0], parent1.x[0] + 1))
    if(parent1.x[1] < parent2.x[1]):
        x.append(rd.randint(parent1.x[1], parent2.x[1] + 1))
    else:
        x.append(rd.randint(parent2.x[1], parent1.x[1] + 1))
    if(parent1.x[2] < parent2.x[2]):
        x.append(rd.uniform(parent1.x[2], parent2.x[2]))
    else:
        x.append(rd.uniform(parent2.x[2], parent1.x[2]))
    if(parent1.x[3] < parent2.x[3]):
        x.append(rd.uniform(parent1.x[3], parent2.x[3]))
    else:
        x.append(rd.uniform(parent2.x[3], parent1.x[3]))
    child = solution(x)
    if(child.fitness < best):
        oldBest = best
        best = child.fitness
        bestx  = child.x
    return child

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

# [0.8419575940040076, 0.415492898727734, 43.42255673512729, 161.0265340906853]
#optimal = solution([0.7980460278996793, 0.3999700397384842, 41.1834968073384, 188.37597974493167])
#print(optimal.fitness)

best = 10000000
bestx = [0, 0, 0, 0]
oldBest = 1000000000
best_genetic_list  = []
for i in range(I):
    best = 10000000
    bestx = [0, 0, 0, 0]
    oldBest = 1000000000
    gen = 0
    pop = generate_population(N)
    while ((oldBest - best) > 0.0001 and maxGen > gen):
        pop = breed_generation(pop)
    best_genetic_list.append(best)
    print(bestx)
    print(best)

best_genetic_series = pd.Series(best_genetic_list)

print(best_genetic_series.describe())
