from accessify import private
from matplotlib import pyplot as plt
from sympy import *
import numpy as np
import math


class Processing():
    def __init__(self): pass
    
    def antiShift(self, data = [i for i in range(1000)]):
        
        fig, ax = plt.subplots(4, figsize=(10, 6))
        
        ax[0].scatter(x=[i for i in range(len(data))], y=data)
        
        ax[1].plot([i for i in range(len(data))], data)
        dataAntiShoft = [i - np.mean(data) for i in data]
        ax[2].plot([i for i in range(len(dataAntiShoft))], dataAntiShoft, color = "red")

        ax[3].plot([i for i in range(len(data))], data)
        ax[3].plot([i for i in range(len(dataAntiShoft))], dataAntiShoft, color = "red")
        
        plt.show()
    
    def antiSpike(self, data = [i for i in range(1000)]):
        
        fig, ax = plt.subplots(3, figsize=(10, 6))
        
        ax[0].plot([i for i in range(len(data))], data)
        
        dataAntiSpike = []
        dataAntiSpike.append(data[0])
        for i in range(1, len(data)-1):
            dataAntiSpike.append((data[i-1]+data[i+1])/2)
        dataAntiSpike.append(data[-1])
        
        ax[1].plot([i for i in range(len(dataAntiSpike))], dataAntiSpike, color = "red")
        
        ax[2].plot([i for i in range(len(data))], data)
        ax[2].plot([i for i in range(len(dataAntiSpike))], dataAntiSpike, color = "red")
        
        plt.show()
    
    def antiTrendLinear(self, a, b, A0, f0, dt, thetta, N):
        x = Symbol('x')
        y = (x*a+b) + A0 * sin(2 * math.pi * f0 * dt * x + thetta)
        y = y.diff(x)
        
        dataAntiTrendLiner = []
        for i in range(N):
            dataAntiTrendLiner.append(y.subs(x, i))
        
        fig, ax = plt.subplots(figsize = (10, 8))
        ax.plot([i for i in range(N)], dataAntiTrendLiner)
        
        plt.show()
    
    def getAntiTrendLinear(self, a, b, A0, f0, dt, thetta, N):
        x = Symbol('x')
        y = (x*a+b) + A0 * sin(2 * math.pi * f0 * dt * x + thetta)
        y = y.diff(x)
        
        dataAntiTrendLiner = []
        for i in range(N):
            dataAntiTrendLiner.append(y.subs(x, i))
        
        return dataAntiTrendLiner
    
    def antiTrendNonLinear(self, data, W):
        moveARGs = []
        
        
        for w in W:
            moveARG = []
            i = 0
            while i < len(data) - w + 1:
                window = data[i: i + w]
                moveARG.append(round(sum(window) / w, 2))
                i += 1
            moveARGs.append(moveARG)
        
        fig, ax = plt.subplots(3, figsize = (10, 8))
        
        for i in range(3):
            dataAntiTrendNonLinear = []
            for j in range(len(moveARGs[i])):
                dataAntiTrendNonLinear.append(data[j] - moveARGs[i][j])
            ax[i].plot([i for i in range(len(dataAntiTrendNonLinear))], dataAntiTrendNonLinear)
        
        plt.show()
    
    def getAntiTrendNonLinear(self, data, W):
        moveARGs = []
        
        
        for w in W:
            moveARG = []
            i = 0
            while i < len(data) - w + 1:
                window = data[i: i + w]
                moveARG.append(round(sum(window) / w, 2))
                i += 1
            moveARGs.append(moveARG)
        
        return moveARGs