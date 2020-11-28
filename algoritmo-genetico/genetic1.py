import math
import random as rd

#Constants
P = 2
sig = 2
L = 100

def g1 (x1, x2):
    return ((((math.sqrt(2) * x1 + x2)/(math.sqrt(2)*(x1**2) + (2*x1*x2))) * P) - sig)

def g2 (x1, x2):
    return ((((x2)/(math.sqrt(2)*(x1**2) + (2*x1*x2))) * P) - sig)

def g3 (x1, x2):
    return ((((1)/(math.sqrt(2)*(x2) + x1)) * P) - sig)

def f(x1, x2):
    return ((2 * (math.sqrt(2) * x1) + x2) * L)

class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart


def init():
    l = []
    for i in range (2):
        x = rd.uniform(0, 1)
        l.append(x)
    return l

def check_restritions(x):
    x1 = x[0]
    x2 = x[1]
    return (g1(x1, x2) <= 0 and g2(x1, x2) <= 0  and g3(x1, x2) <= 0)

def fit(x):
    x1 = x[0]
    x2 = x[1]
    fitness = f(x1, x2)
    if(not check_restritions(x)):
        fitness = fitness * 1.5
    return fitness


def generate_population(n):
    r = []
    for i in range(n):
        r.append(init())
    return r

x = generate_population(1000)
for item in x:
    print(fit(item))