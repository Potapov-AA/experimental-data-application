from random import randint
from accessify import private
from matplotlib import pyplot as plt
import numpy as np
import math
import time
from config import Config



class Model:
    def __init__(self):
        self.e = np.e
        self.parametrs = Config()


    def drawData(self, data):
        '''
        Отображает переданные данные
        '''
        dataX = [i for i in range(len(data))]
        dataY = data
        
        plt.figure(figsize=(10, 10))
        plt.grid(True)
        
        plt.title("Текущие данные")
        plt.plot(dataX, dataY)
        
        plt.show()
    
    def drawCurrentSoundData(self, data):
        '''
        Отображает текущие звуковые данные
        '''
        dataY = data["data"]
        dataX = np.arange(0,data["nframes"])/data["framerate"]
        
        time = round(data["nframes"]/data["framerate"], 2)
        framerate = data["framerate"]
        nchannels = data["nchannels"]
        
        plt.figure(figsize=(10,10)) 
        plt.subplot(2,1,1) 
        plt.plot(dataX, dataY[0])
        plt.title(f"Текущий звуковой файл. Частота: {framerate}. Длительность: {time}. Кол-во каналов: {nchannels}")
        plt.subplot(2,1,2) 
        plt.plot(dataX, dataY[1], c='r')        
        plt.xlabel("time")
        plt.show()
    
    
    def linerGraph(self, type=0, draw=False):
        '''
        Линейный график
        '''
        if draw:
            plt.figure(figsize=(10, 10))
            plt.grid(True)
        
        a=float(self.parametrs.GetParametr("Parametrs", "a"))
        b=float(self.parametrs.GetParametr("Parametrs", "b"))
        N=int(self.parametrs.GetParametr("Parametrs", "N"))
        
        dataX = np.asarray([i for i in range(N)], dtype=float)
        
        if type == 0:
            dataY = np.asarray([i*a+b for i in range(N)], dtype=float)
            if draw:
                plt.plot(dataX, dataY)
                plt.title("Линейный восходящий график")
        elif type == 1:
            dataY = -np.asarray([i*a+b for i in range(N)], dtype=float)
            if draw:
                plt.plot(dataX, dataY)
                plt.title("Линейный низходящий график")
        
        if draw:
            plt.show()
            
        return dataY

    def exponentaGraph(self, type=0, draw=False):
        '''
        График экспоненты
        '''
        if draw:
            plt.figure(figsize=(10, 10))
            plt.grid(True)
        
        alpha=float(self.parametrs.GetParametr("Parametrs", "alpha"))
        beta=float(self.parametrs.GetParametr("Parametrs", "beta"))
        N=int(self.parametrs.GetParametr("Parametrs", "N"))
        
        dataX = np.asarray([i for i in range(N)], dtype=float)
        
        if type == 0:
            dataY = np.asarray([beta * self.e ** (-alpha * i) for i in range(N)])
            plt.plot(dataX, dataY)
            plt.title("Экспонентный восходящий график")
        elif type == 1:
            dataY = np.asarray([beta * self.e ** (alpha * i) for i in range(N)])
            plt.plot(dataX, dataY)
            plt.title("Экспонентный низходящий график")
        
        if draw:
            plt.show()
            
        return dataY

    def sinGraph(self, draw=False):
        '''
        График синусойды
        '''
        A0=float(self.parametrs.GetParametr("Parametrs", "A0"))
        f0=float(self.parametrs.GetParametr("Parametrs", "f0"))
        dt=float(self.parametrs.GetParametr("Parametrs", "dt"))
        thetta=float(self.parametrs.GetParametr("Parametrs", "thetta"))
        N=int(self.parametrs.GetParametr("Parametrs", "N"))
        
        dataX = np.asarray([i * dt for i in range(N)])
        dataY = np.asarray([A0 * math.sin(2 * math.pi * f0 * dt * k + thetta) for k in range(N)])

        if draw:
            plt.figure(figsize=(10, 10))
            plt.grid(True)
            plt.plot(dataX, dataY)
            plt.title("Синусойда")
            plt.show()

        return dataY
    
    def drawSinWithStep(self):
        '''
        Графики синусойды с повышением f0 с указанным шагом
        '''
        A0=float(self.parametrs.GetParametr("Parametrs", "A0"))
        f0=float(self.parametrs.GetParametr("Parametrs", "f0"))
        dt=float(self.parametrs.GetParametr("Parametrs", "dt"))
        N=int(self.parametrs.GetParametr("Parametrs", "N"))
        step = int(self.parametrs.GetParametr("Parametrs", "step"))
        
        plt.figure(figsize=(10, 10))
        
        dataX = np.asarray([i * dt for i in range(N)])
        
        for i in range(4):
            plt.subplot(2, 2, i+1)
            plt.grid(True)
            
            dataY = np.asarray([A0 * math.sin(2 * math.pi * f0 * dt * k) for k in range(N)])
            f0 += step

            plt.plot(dataX, dataY)
        
        plt.show()
    
          
    def sinSumGraph(self, draw=False):
        '''
        Сумма трех синусойд на одном графике
        '''
        A0=float(self.parametrs.GetParametr("Parametrs", "A0"))
        A1=float(self.parametrs.GetParametr("Parametrs", "A1"))
        A2=float(self.parametrs.GetParametr("Parametrs", "A2"))
        f0=float(self.parametrs.GetParametr("Parametrs", "f0"))
        f1=float(self.parametrs.GetParametr("Parametrs", "f1"))
        f2=float(self.parametrs.GetParametr("Parametrs", "f2"))
        dt=float(self.parametrs.GetParametr("Parametrs", "dt"))
        N=int(self.parametrs.GetParametr("Parametrs", "N"))
        
        dataX = [i * dt for i in range(N)]
        dataY = [
            A0 * math.sin(2 * math.pi * f0 * dt * k)
            + A1 * math.sin(2 * math.pi * f1 * dt * k)
            + A2 * math.sin(2 * math.pi * f2 * dt * k)
            for k in range(N)
        ]
        if draw:
            plt.figure(figsize=(10, 10))
            plt.grid(True)
            plt.plot(dataX, dataY)
            plt.title("Сумма трех синусойд")
            plt.show()

        return dataY
          

    def defaultNoise(self, draw=False):
        '''
        Шум на основе встроенного ПСЧ
        '''
        Range=float(self.parametrs.GetParametr("Parametrs", "R"))
        N=int(self.parametrs.GetParametr("Parametrs", "N"))
        
        dataX = np.asarray([i for i in range(N)])
        dataY = np.asarray(np.random.randint(-Range, Range, N))

        if draw:
            plt.figure(figsize=(10, 10))
            plt.grid(True)
            plt.plot(dataX, dataY)
            plt.title("Шум на основе встроенного ПСЧ")
            plt.show()
        
        return dataY

    def lineKonNoise(self, draw=False):
        '''
        Шум на основе встроенного линейного конгруэнтного ПСЧ
        '''
        Range=float(self.parametrs.GetParametr("Parametrs", "R"))
        N=int(self.parametrs.GetParametr("Parametrs", "N"))
        
        seed = time.time()
        m = 32768
        a = 29
        c = 47
        r = [0 for i in range(N)]

        r[0] = math.ceil(seed)
        for i in range(1, N):
            r[i] = math.ceil(math.fmod((a*r[i-1]+c), m))

        dataY = []

        for i in r:
            j = 0
            while i > Range:
                i /= 3
                j += 1

            i = round(i)

            if j % 2 == 1:
                i *= -1

            dataY.append(i)

        dataX = np.asarray([i for i in range(N)])
        dataY = np.asarray(dataY)

        if draw:
            plt.figure(figsize=(10, 10))
            plt.grid(True)
            plt.plot(dataX, dataY)
            plt.title("Шум на основе встроенного линейного конгруэнтного ПСЧ")
            plt.show()
        
        return dataY
        
    
    def shiftData(self, data, draw=False):
        '''
        Создает смещение на переданных данных в указанном диапозоне
        '''
        try:
            shift=float(self.parametrs.GetParametr("Parametrs", "Shift"))
            N1=int(self.parametrs.GetParametr("Parametrs", "ShiftFrom"))
            N2=int(self.parametrs.GetParametr("Parametrs", "ShiftTo"))
            
            
            dataShiftY = []
            if N1 != 0:
                for i in range(N1):
                    dataShiftY.append(data[i])

            for i in range(N1, N2):
                dataShiftY.append(data[i]+shift)

            if N2 != len(data):
                for i in range(N2, len(data)):
                    dataShiftY.append(data[i])

            dataX = [i for i in range(len(data))]
            dataDefultY = data
            
            if draw:
                plt.figure(figsize=(10, 10))
                plt.subplot(1, 2, 1)
                plt.grid(True)
                plt.plot(dataX, dataDefultY)
                plt.title("Начальные данные")

                plt.subplot(1, 2, 2)
                plt.grid(True)
                plt.plot(dataX, dataShiftY)
                plt.title("Смещенные данные")
                plt.show()

            dataShiftY = np.asarray(dataShiftY)
            
            return dataShiftY
        except:
            print("Передан пустой массив данных")
        
    def impulseData(self, data, draw=False):
        '''
        Создает импульсы на переданных данных
        '''
        try:
            maxR=int(self.parametrs.GetParametr("Parametrs", "R2"))
            minR=int(self.parametrs.GetParametr("Parametrs", "R1"))
                    
            dataX = [i for i in range(len(data))]

            M = randint(len(data) * 0.005, len(data)*0.01+1)

            impulseList = []

            for i in range(M):
                number = randint(0, len(data) + 1)
                impulseList.append(number)

            dataDefultY = data
            dataImpulseY = []
            for i in dataX:
                if i in impulseList:
                    sign = math.pow(-1, randint(1, 3))
                    y = randint(maxR-minR, maxR+minR+1) * sign
                    dataImpulseY.append(y)
                else:
                    dataImpulseY.append(data[i])

            if draw:
                plt.figure(figsize=(10, 10))
                
                plt.subplot(1, 2, 1)
                plt.grid(True)
                plt.plot(dataX, dataDefultY)
                plt.title("Начальные данные")
                
                plt.subplot(1, 2, 2)
                plt.grid(True)
                plt.plot(dataX, dataImpulseY)
                plt.title("Данные с импульсами")
                
                plt.show()    
            
            dataImpulseY = np.asarray(dataImpulseY)
            
            return dataImpulseY
        except:
            print("Передан пустой массив данных")
        
    

    

    

    

    
   
    
    def addModel(self, data1 = [i for i in range(1000)], data2 = [-i for i in range(1000)]):
        N = len(data1)
        dataSum = [data1[i] + data2[i] for i in range(N)]
        
        fig, ax = plt.subplots(3, figsize = (10, 8))
        ax[0].plot([i for i in range(N)], data1)
        ax[1].plot([i for i in range(N)], data2)
        ax[2].plot([i for i in range(N)], dataSum)
        
        plt.show()
    
    def getSumModel(self, data1 = [i for i in range(1000)], data2 = [-i for i in range(1000)]):
        N = len(data1)
        return [data1[i] + data2[i] for i in range(N)]
    
    def getSumHarmNoise(self):
        data = self.getDefaultNoise() + self.getDefaultHarm()
        return data
    
    def drawMultiModel(self, data1, data2):
        N = len(data1)
        data = [data1[i] * data2[i] for i in range(N)]
        dataX = [i for i in range(N)]
        
        plt.figure(figsize=(10,10))
        plt.grid(True)
        
        plt.subplot(3, 1, 1)
        plt.title("data1")
        plt.plot(dataX, data1)
        
        plt.subplot(3, 1, 2)
        plt.title("data2")
        plt.plot(dataX, data2)
        
        plt.subplot(3, 1, 3)
        plt.title("Multi data")
        plt.plot(dataX, data)
        
        plt.show()
    
    def getMultModel(self, data1, data2):
        N = len(data1)
        return [data1[i] * data2[i] for i in range(N)]
     
    def Fourier(self, data = [0 for i in range(1000)], N = 1000, L = 0):
        if L != 0:
            data = [i for i in data[0:N-L]]
            data += [0 for i in range(L)]
        
        dataY = []
        for n in range(N):
            Re = 0
            for k in range(N):
                Re += data[k]*np.cos((2 * np.pi * n * k)/N)
            Re /= N
            
            Lm = 0
            for k in range(N):
                Lm += data[k]*np.sin((2 * np.pi * n * k)/N)
            Lm /= N
            dataY.append(np.sqrt(np.square(Re) + np.square(Lm)))
        
        dataY = np.asarray(dataY)
        
        return dataY
    
    def Cardiograma(self):
        data = self.getMultModel(self.getDefaultExponentaTrend(), self.getDefaultHarm())
        N = len(data)
        M = 200
        dataX = [i * 0.005 for i in range(N)]
        
        max = np.max(data)
        data = [i / max * 120 for i in data]
        
        plt.figure(figsize=(15, 10))
        
        plt.subplot(3, 1, 1)
        plt.title("Мульти экспонента-гармоника")
        plt.grid(True)
        plt.plot(dataX, data) 
        
        
        impulse = 1
        dataImpulse = []
        for i in range(N):
            if i % M == 0 and i != 0:
                dataImpulse.append(impulse)
            else:
                dataImpulse.append(0)
        
        plt.subplot(3, 1, 2)
        plt.title("Импульсы")
        plt.grid(True)
        plt.plot(dataX, dataImpulse)
        
        dataCardio = []
        for k in range(N+M):
            yk = 0
            for m in range(M):
                try:
                    yk += dataImpulse[k-m] * data[m]
                except:
                    pass
            dataCardio.append(yk)
        
        plt.subplot(3, 1, 3)
        plt.title("Кардиограмма")
        plt.grid(True)
        plt.plot(dataX, dataCardio[0:N])
        
        plt.show()