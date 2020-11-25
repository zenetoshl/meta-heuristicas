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
    return ((2*(math.sqrt(2) * x1) + x2)*L)

def init():
    l = []
    for i in range (2):
        x = rd.uniform(0, 1)
        l.append(x)
    return l

def check_restritions(x):
    x1 = x[0]
    x2 = x[1]
    print("g1")
    print(g1(x1, x2))
    print("g2")
    print(g2(x1, x2))
    print("g3")
    print(g3(x1, x2))
    print("f")
    print(f(x1, x2))
    return (g1(x1, x2) <= 0 and g2(x1, x2) <= 0  and g3(x1, x2) <= 0)

print(check_restritions([0.7886751284, 0.4082483080]))
x = init()
print(x)