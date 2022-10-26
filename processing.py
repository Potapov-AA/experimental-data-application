from accessify import private
from matplotlib import pyplot as plt
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