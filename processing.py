from accessify import private
from matplotlib import pyplot as plt
from sympy import *
import numpy as np
import math
from model import Model
from config import Config
from analysis import Analysis


class Processing():
    def __init__(self):
        self.model = Model()
        self.parametrs = Config()
        self.analysis = Analysis()

    def antiShift(self, data=[i for i in range(1000)]):

        fig, ax = plt.subplots(4, figsize=(10, 6))

        ax[0].scatter(x=[i for i in range(len(data))], y=data)

        ax[1].plot([i for i in range(len(data))], data)
        dataAntiShoft = [i - np.mean(data) for i in data]
        ax[2].plot([i for i in range(len(dataAntiShoft))],
                   dataAntiShoft, color="red")

        ax[3].plot([i for i in range(len(data))], data)
        ax[3].plot([i for i in range(len(dataAntiShoft))],
                   dataAntiShoft, color="red")

        plt.show()

    def antiSpike(self, min, max, data=[i for i in range(1000)]):

        fig, ax = plt.subplots(3, figsize=(10, 6))

        ax[0].plot([i for i in range(len(data))], data)

        dataAntiSpike = []
        dataAntiSpike.append(data[0])
        for i in range(1, len(data)-1):
            if data[i] > max or data[i] < min:
                dataAntiSpike.append((data[i-1]+data[i+1])/2)
            else:
                dataAntiSpike.append((data[i]))
        dataAntiSpike.append(data[-1])

        ax[1].plot([i for i in range(len(dataAntiSpike))],
                   dataAntiSpike, color="red")

        ax[2].plot([i for i in range(len(data))], data)
        ax[2].plot([i for i in range(len(dataAntiSpike))],
                   dataAntiSpike, color="red")

        plt.show()

    def antiTrendLinear(self, a, b, A0, f0, dt, thetta, N):
        x = Symbol('x')
        y = (x*a+b) + A0 * sin(2 * math.pi * f0 * dt * x + thetta)
        y = y.diff(x)

        dataAntiTrendLiner = []
        for i in range(N):
            dataAntiTrendLiner.append(y.subs(x, i))

        fig, ax = plt.subplots(figsize=(10, 8))
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

        fig, ax = plt.subplots(3, figsize=(10, 8))

        for i in range(3):
            dataAntiTrendNonLinear = []
            for j in range(len(moveARGs[i])):
                dataAntiTrendNonLinear.append(data[j] - moveARGs[i][j])
            ax[i].plot([i for i in range(len(dataAntiTrendNonLinear))],
                       dataAntiTrendNonLinear)

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

    def AntiNoise(self, function, stepM=10):
        plt.figure(figsize=(15, 15))
        
        M = 2
        step = 0
        while step < 6:
            data = function()
            for m in range(M-1):
                data += function()
            
            dataY = []
            for i in data:
                dataY.append(i/M)
            dataY = np.asarray(dataY)
            
            dataX = [i for i in range(len(dataY))]
            
            standardDeviation = round(np.std(dataY), 2)
            
            plt.subplot(4, 3, (7, 9))
            plt.grid(True)
            plt.plot(dataX, dataY)
            plt.title("Наложение всех шумов")

            plt.subplot(4, 3, step + 1)
            plt.grid(True)
            plt.plot(dataX, dataY)
            plt.title(f"M = {M} стандартное отклонение = {standardDeviation}")

            M *= stepM
            step += 1
        
        dataX = []
        dataYstd = []
        for m in range(1, 1000, stepM):
            data = function()
            for i in range(m-1):
                data += function()
            dataY = []
            for i in data:
                dataY.append(i/m)
            standardDeviation = round(np.std(dataY), 4)
            dataX.append(m)
            dataYstd.append(standardDeviation)
            plt.subplot(4, 3, (10, 12))
            plt.plot(dataX, dataYstd)
            plt.title("Изменение стандартного отклонения")
            
        plt.show()
    
    def lpf(self, draw = False):
        fc1=float(self.parametrs.GetParametr("Parametrs", "fc"))
        fc2=float(self.parametrs.GetParametr("Parametrs", "fc1"))
        fc3=float(self.parametrs.GetParametr("Parametrs", "fc2"))
        fc = [fc1, fc2, fc3]
        m = int(self.parametrs.GetParametr("Parametrs", "m for lpf"))
        dt = float(self.parametrs.GetParametr("Parametrs", "dt"))
        
        # rectangular part weights
        D = [0.35577019, 0.2436983, 0.07211497, 0.00630165]
        result = []
        
        if draw:
            plt.figure(figsize=(10,10))
        
        for f in range(len(fc)):
            lpw = []
            fact = 2 * fc[f] * dt
            lpw.append(fact)
            
            arg = np.pi * fact
            
            for i in range(1, m+1):
                lpw.append(np.sin(arg*i) / (np.pi*i))
            
            # trapezoid smoothing at the end
            lpw[m] /= 2
            
            # P310 smoothing window
            sumg = lpw[0]
            for i in range(1, m+1):
                sum = D[0]
                arg = np.pi * i / m
                for k in range(1, 4):
                    sum += 2 * D[k] * np.cos(arg * k)
                lpw[i] *= sum
                sumg += 2 * lpw[i]
            
            for i in range(m+1):
                lpw[i] /= sumg
            
            
            
            
            reverseLPW = lpw[::-1]
            simetricLPW = reverseLPW + lpw
            result.append(simetricLPW)
            
            if draw:
                plt.subplot(2,3,f+1)
                plt.title(f"ФНЧ fc = {fc[f]}")
                plt.plot([i for i in range(len(lpw))], lpw)
                
                plt.subplot(2,3,f+4)
                plt.plot([i for i in range(len(simetricLPW))], simetricLPW)
            
        if draw:
            plt.show()
        
        return result   
    
    
    def hpf(self, draw=False):
        m = int(self.parametrs.GetParametr("Parametrs", "m for lpf"))
        llpw = self.lpf()
        loper = 2*m+1
        
        if draw:
            plt.figure(figsize=(10,10))
        
        i = 1
        result = []
        for lpw in llpw:
            hpw = []
            for k in range(loper+1):
                if k == m:
                    hpw.append(1 - lpw[k])
                else:
                    hpw.append(-lpw[k])
            if draw:
                plt.subplot(1,3,i)
                plt.plot([i for i in range(len(hpw))], hpw)
            i += 1
            result.append(hpw)
        
        if draw:
            plt.show()
        
        return result
        
    def bpf(self, draw = False):
        m = int(self.parametrs.GetParametr("Parametrs", "m for lpf"))
        lpw = self.lpf()
        lpw1 = lpw[1]
        lpw2 = lpw[2]
        loper = 2*m+1
        bpw = []
        
        for k in range(loper+1):
            bpw.append(lpw2[k]-lpw1[k])
        if draw:
            plt.figure(figsize=(10,10))
            plt.title("Полосовой фильтр ПФ")
            plt.plot([i for i in range(len(bpw))], bpw)
            plt.show()
        
        return bpw
    
    def bsf(self, draw = False):
        m = int(self.parametrs.GetParametr("Parametrs", "m for lpf"))
        lpw = self.lpf()
        lpw1 = lpw[1]
        lpw2 = lpw[2]
        loper = 2*m+1
        bsw = []
        
        for k in range(loper+1):
            if k == m:
                bsw.append(1 + lpw1[k] - lpw2[k])
            else:
                bsw.append(lpw1[k] - lpw2[k])
        if draw:
            plt.figure(figsize=(10,10))
            plt.title("Режекторный фильтр РФ")
            plt.plot([i for i in range(len(bsw))], bsw)
            plt.show()    

        return bsw
        
    def FilterFourier(self):
        m = int(self.parametrs.GetParametr("Parametrs", "m for lpf"))
        
        lpw = self.lpf()[0]
        hpw = self.hpf()[0]
        bpw = self.bpf()
        bsw = self.bsf()
        
        loper = 2 * m + 1
        
        plt.figure(figsize=(10, 10))
        
        lpwFourier = self.analysis.getSpectrFourier(lpw)
        dataX = [i for i in range(len(lpwFourier))]
        dataY = [i * loper for i in lpwFourier]
        
        plt.subplot(2, 2, 1)
        plt.title("LPF")
        plt.plot(dataX, dataY)
        
        
        hpwFourier = self.analysis.getSpectrFourier(hpw)
        dataX = [i for i in range(len(hpwFourier))]
        dataY = [i * loper for i in hpwFourier]
        
        plt.subplot(2, 2, 2)
        plt.title("HPF")
        plt.plot(dataX, dataY)
        
        
        bpwFourier = self.analysis.getSpectrFourier(bpw)
        dataX = [i for i in range(len(bpwFourier))]
        dataY = [i * loper for i in bpwFourier]
        
        plt.subplot(2, 2, 3)
        plt.title("BPF")
        plt.plot(dataX, dataY)
        
        
        bswFourier = self.analysis.getSpectrFourier(bsw)
        dataX = [i for i in range(len(bswFourier))]
        dataY = [i * loper for i in bswFourier]
        
        plt.subplot(2, 2, 4)
        plt.title("BSF")
        plt.plot(dataX, dataY)
        
        plt.show()
        