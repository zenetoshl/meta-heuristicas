import math
import random as rd

#Constants
P = 2
sig = 2
L = 100

def g1 (x1, x2, x3, x4):
    return (-x1 + 0.0193*x3)

def g2 (x1, x2, x3, x4):
    return (-x2 + 0.00954*x3)

def g3 (x1, x2, x3, x4):
    return ((-(math.pi*(x3**2)*x4) - (4/3)*math.pi*(x3**3)) + 1296000)
    
def g4 (x1, x2, x3, x4):
    return (x4 - 240)

def f(x1, x2, x3, x4):
    return (0.6224*x1*x3*x4 + 1.7781*x2*(x3**2) + 3.1661*(x1**2)*x4+19.84*(x1**2)*x3)

def init():
    l = []
    x1 = rd.uniform(0, 100)
    l.append(x1)
    x2 = rd.uniform(0, 100)
    l.append(x2)
    x3 = rd.uniform(10, 200)
    l.append(x3)
    x4 = rd.uniform(10, 200)
    l.append(x4)
    return l

def check_restritions(x):
    x1 = x[0]
    x2 = x[1]
    x3 = x[2]
    x4 = x[3]
    print("g1")
    print(g1(x1, x2, x3, x4))
    print("g2")
    print(g2(x1, x2, x3, x4))
    print("g3")
    print(g3(x1, x2, x3, x4))
    print("g4")
    print(g4(x1, x2, x3, x4))
    print('f')
    print(f(x1, x2, x3, x4))
    return (g1(x1, x2, x3, x4) <= 0 and g2(x1, x2, x3, x4) <= 0  and g3(x1, x2, x3, x4) <= 0 and g4(x1, x2, x3, x4) <= 0)

print(check_restritions([0.812500,  0.437500,  42.09844539, 176.63659855]))
x = init()
print(x)
