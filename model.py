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


    def drawCurrentData(self, data):
        '''
        Отображает текущие данные
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
        
    
    def drawShiftData(self, data=[i for i in range(1000)], shift=500, N1=0, N2=500):
        '''
        Отрисовывает смещеные переданные данные на указанном диапозоне
        Если диапазон не передан, то смещение идет по всем данным
        По умолчанию не отрисовывает графики
        data - смещаемые данные 
        shift - величина смещения
        N1 - индекс начала смещения
        N2 - индекс конца смещения
        '''
        shiftData = []
        if N1 != 0:
            shiftData += [i for i in data[0: N1]]

        shiftData += [i + shift for i in data[N1: N2]]

        if N2 != len(data):
            shiftData += [i for i in data[N2:]]

        plt.figure(figsize=(10, 10))
        plt.subplot(1, 2, 1)
        plt.grid(True)
        plt.plot([i for i in range(len(data))], data)
        plt.title("Начальные данные")

        plt.subplot(1, 2, 2)
        plt.grid(True)
        plt.plot([i for i in range(len(shiftData))], shiftData)
        plt.title("Смещенные данные")
        plt.show()

    def getShiftData(self, data=[i for i in range(1000)], shift=500, N1=0, N2=500):
        '''
        Возвращает смещеные переданные данные на указанном диапозоне
        Если диапазон не передан, то смещение идет по всем данным
        По умолчанию не отрисовывает графики
        data - смещаемые данные 
        shift - величина смещения
        N1 - индекс начала смещения
        N2 - индекс конца смещения
        '''
        shiftData = []
        if N1 != 0:
            shiftData += [i for i in data[0: N1]]

        shiftData += [i + shift for i in data[N1: N2]]

        if N2 != len(data) - 1:
            shiftData += [i for i in data[N2:]]

        return shiftData

    def drawImpulseNoise(self, data=[0 for i in range(1000)], R=1000, Rs=900):
        '''
        Выводит импульс на переданных данных
        data = передаваемые данные
        R = максимальное значение импульса
        Rs = минимальное значение импульса
        '''
        dataX = [i for i in range(len(data))]

        M = randint(len(data) * 0.005, len(data)*0.01+1)

        impulseList = []

        for i in range(M):
            number = randint(0, len(data) + 1)
            impulseList.append(number)

        dataY = []
        for i in dataX:
            if i in impulseList:
                sign = math.pow(-1, randint(1, 3))
                y = randint(R-Rs, R+Rs+1) * sign
                dataY.append(y)
            else:
                dataY.append(data[i])

        plt.figure(figsize=(10, 10))
        plt.grid(True)
        plt.plot(dataX, dataY)
        plt.title("Импульсы")
        plt.show()

    def getImpulseNoise(self, data=[0 for i in range(1000)], R=1000, Rs=900):
        dataX = [i for i in range(len(data))]

        M = randint(len(data) * 0.005, len(data)*0.01+1)

        impulseList = []

        for i in range(M):
            number = randint(0, len(data) + 1)
            impulseList.append(number)

        dataY = []
        for i in dataX:
            if i in impulseList:
                sign = math.pow(-1, randint(1, 3))
                y = randint(R-Rs, R+Rs+1) * sign
                dataY.append(y)
            else:
                dataY.append(data[i])

        return np.asarray(dataY)

    

    def drawHarms(self, N = 200, A0 = 5, f0 = 10, dt = 0.001, step = 250):
        '''
        Множество графиков гармонического процесса с повышением f0 по 50
        '''
        datasX = [0] * 4
        datasY = [0] * 4
        
        
        for i in range(4):            
            datasX[i] = [i * dt for i in range(N)]
            datasY[i] = [A0 * math.sin(2 * math.pi * f0 * dt * k) for k in range(N)]
            f0 += step
        
        
        _, (axs) = plt.subplots(2, 2)
        plt.grid(True)
        axs[0, 0].plot(datasX[0], datasY[0])
        axs[0, 1].plot(datasX[1], datasY[1])
        axs[1, 0].plot(datasX[2], datasY[2])
        axs[1, 1].plot(datasX[3], datasY[3])
        
        for flat in axs.flat:
            flat.set(xlabel="X", ylabel="Y")
            flat.label_outer()

        plt.show()
   
    def draw3In1Harm(self, N = 1000, A0 = 100, A1 = 50, A2 = 25, f0 = 4, f1 = 1, f2 = 20, dt = 0.001):
        '''
        Сумма нескольких гармоник на одном графике
        '''
        harm = [
            A0 * math.sin(2 * math.pi * f0 * dt * k)
            + A1 * math.sin(2 * math.pi * f1 * dt * k)
            + A2 * math.sin(2 * math.pi * f2 * dt * k)
            for k in range(N)
        ]

        plt.figure(figsize=(10, 10))
        plt.grid(True)
        plt.plot([i * dt for i in range(N)], harm)
        plt.title("harm")
        plt.show()
    
    def getHarm(self, N = 1000, A0 = 10, f0 = 10, dt = 0.01, thetta = 0):
        '''
        Возвращает данные гармонического процесса
        '''
        dataY = [A0 * math.sin(2 * math.pi * f0 * dt * k + thetta) for k in range(N)]

        return dataY
    
    def getDefaultHarm(self):
        N = int(self.parametrs.GetParametr("Parametrs", "N"))
        A0=float(self.parametrs.GetParametr("Parametrs", "A0"))
        f0=float(self.parametrs.GetParametr("Parametrs", "f0"))
        dt=float(self.parametrs.GetParametr("Parametrs", "dt"))
        thetta=float(self.parametrs.GetParametr("Parametrs", "thetta"))
        
        data = [A0 * math.sin(2 * math.pi * f0 * dt * k + thetta) for k in range(N)]
        
        return data
    
    def getPolyHarm(self, N = 1000, A0 = 100, A1 = 50, A2 = 25, f0 = 4, f1 = 1, f2 = 20, dt = 0.001):
        '''
        Возвращает данные полигармонического процесса
        '''
        dataY = [
            A0 * math.sin(2 * math.pi * f0 * dt * k)
            + A1 * math.sin(2 * math.pi * f1 * dt * k)
            + A2 * math.sin(2 * math.pi * f2 * dt * k)
            for k in range(N)
        ]
        
        return dataY
    
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


    @private
    def __calculateMyRandomNoise(self, seed, Range, N):
        '''
        Расчитывает значения по оси Y по функции с помощью линейного конгруэнтный генератора псевдослучайных чисел
        '''
        
