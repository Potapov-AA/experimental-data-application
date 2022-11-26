from accessify import private
from matplotlib import pyplot as plt
from sympy import *
import numpy as np
import math
from model import Model
from config import Config


class Processing():
    def __init__(self):
        self.model = Model()
        self.parametrs = Config()

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

    def AntiNoise(self, data=[0 for i in range(1000)], stepM=10):
        plt.figure(figsize=(15, 15))
        

        M = 1
        step = 0
        while step < 6:
            data = self.model.getNoise(
                Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                type=0
            )
            for m in range(M-1):
                data += self.model.getNoise(
                    Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    type=0
                )

            dataY = []
            for i in data:
                dataY.append(i/M)

            dataX = [i for i in range(len(dataY))]
            dataY = np.asarray(dataY)

            standardDeviation = round(np.std(dataY), 2)

            plt.subplot(4, 3, (7, 9))
            plt.plot(dataX, dataY)
            plt.title("Наложение всех шумов")

            plt.subplot(4, 3, step + 1)
            plt.plot(dataX, dataY)
            plt.title(f"M = {M} стандартное отклонение = {standardDeviation}")

            M *= stepM
            step += 1

        
        dataX = []
        dataYstd = []
        for m in range(1, 1000, stepM):
            data = self.model.getNoise(
                Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                N=int(self.parametrs.GetParametr("Parametrs", "N")),
                type=0
            )
            for i in range(m-1):
                data += self.model.getNoise(
                    Range=int(self.parametrs.GetParametr("Parametrs", "R")),
                    N=int(self.parametrs.GetParametr("Parametrs", "N")),
                    type=0
                )
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

        # plt.subplot(4, 3, (7, 9))
        # plt.plot(dataX, dataY)
        # plt.title("Наложение всех шумов")

        # N = len(data)

        # M = 10
        # lM = []
        # xt = []
        # while M <= N:
        #     lM.append(M)

        #     sum = 0
        #     for m in range(M):
        #         sum += data[m]
        #     sum = sum/M
        #     if sum < 0:
        #         sum *= -1
        #     xt.append(sum)

        #     M *= stepM

        # for i in range(len(xt)):
        #     dataNewY = []
        #     for j in data:
        #         if j > 0:
        #             dataNewY.append(j - xt[i])
        #         else:
        #             dataNewY.append(j + xt[i])
        #     plt.subplot(4, 3, i+1).patch.set_facecolor('black')
        #     plt.plot(dataX, dataNewY)
        #     plt.title(f"M = {lM[i]}")
        #     standardDeviation = round(np.std(dataNewY), 2)
        #     plt.text(10, -20, f"Стандартное отклонение {standardDeviation}", color = 'white',)
        #     plt.subplot(4, 3, (7, 9))
        #     plt.plot(dataX, dataNewY)

        # dataYstd = []
        # xtForStd = []

        # M = 10
        # while M <= N:
        #     lM.append(M)

        #     sum = 0
        #     for m in range(M):
        #         sum += data[m]
        #     sum = sum/M
        #     if sum < 0:
        #         sum *= -1
        #     xtForStd.append(sum)

        #     M += stepM

        # for i in range(len(xtForStd)):
        #     dataNewY = []
        #     for j in data:
        #         if j > 0:
        #             dataNewY.append(j - xtForStd[i])
        #         else:
        #             dataNewY.append(j + xtForStd[i])
        #     standardDeviation = round(np.std(dataNewY), 2)
        #     dataYstd.append(standardDeviation)

        # plt.subplot(4, 3, (10, 12))
        # plt.title(" зависимость изменения Стандартного отклонения")
        # plt.plot([i for i in range(len(dataYstd))], dataYstd)

        # plt.show()
