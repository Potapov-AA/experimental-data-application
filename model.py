from random import randint
import random
from matplotlib import pyplot as plt
import numpy as np
import math
import time
import PIL.Image as pil

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
    
    def drawSoundData(self, data):
        '''
        Отображает текущие звуковые данные
        '''
        dataY = data["data"]
        dataX = np.arange(0,data["nframes"])/data["framerate"]
        
        time = round(data["nframes"]/data["framerate"], 2)
        framerate = data["framerate"]
        nchannels = data["nchannels"]
        sampwidth = data["sampwidth"]
        
        if nchannels == 2:
            plt.figure(figsize=(10,10)) 
            plt.subplot(2,1,1) 
            plt.plot(dataX, dataY[0])
            plt.title(f"Текущий звуковой файл. Частота: {framerate}. Длительность: {time}. Кол-во каналов: {nchannels}")
            plt.subplot(2,1,2) 
            plt.plot(dataX, dataY[1], c='r')        
            plt.xlabel("time")
        else:
            plt.figure(figsize=(10,10)) 
            plt.plot(dataX, dataY)
            plt.title(f"Текущий звуковой файл. Частота: {framerate}. Длительность: {time}. Кол-во каналов: {nchannels}, {sampwidth}")   
            plt.xlabel("time")
        
        plt.show()
    
    
    def drawImageData(self, dataImage):
        try:
            if(len(dataImage[0][0]) > 1):
                dataImage = dataImage.astype('uint8')
        except:
            pass
        image = pil.fromarray(dataImage)
        
        
        size_w = image.size[0]
        size_h = image.size[1]
        plt.figure(figsize=(6,6))
        plt.title(f"Размеры изображения: {size_w}x{size_h}")
        plt.imshow(image)
        plt.axis("off")
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
            if draw:
                plt.plot(dataX, dataY)
                plt.title("Экспонентный восходящий график")
        elif type == 1:
            dataY = np.asarray([beta * self.e ** (alpha * i) for i in range(N)])
            if draw:
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
        
    
    def sumGraph(self, data1, data2, draw=False):
        '''
        Сложение двух данных
        '''
        dataX = [i for i in range(len(data1))]
        dataY = [data1[i] + data2[i] for i in range(len(data1))]
        
        if draw:
            plt.figure(figsize=(10,10))
            
            plt.subplot(2, 2, 1)
            plt.grid(True)
            plt.plot(dataX, data1)
            
            plt.subplot(2, 2, 2)
            plt.grid(True)
            plt.plot(dataX, data2)
            
            plt.subplot(2, 2, (3, 4))
            plt.grid(True)
            plt.plot(dataX, dataY)
            
            plt.show()
        
        return dataY

    def multiGraph(self, data1, data2, draw=False):
        '''
        Перемножение двух данных
        '''
        dataX = [i for i in range(len(data1))]
        dataY = [data1[i] * data2[i] for i in range(len(data1))]
        
        if draw:
            plt.figure(figsize=(10,10))
            
            plt.subplot(2, 2, 1)
            plt.grid(True)
            plt.plot(dataX, data1)
            
            plt.subplot(2, 2, 2)
            plt.grid(True)
            plt.plot(dataX, data2)
            
            plt.subplot(2, 2, (3, 4))
            plt.grid(True)
            plt.plot(dataX, dataY)
            
            plt.show()
        
        return dataY
    
    
    def cardiograma(self, draw=False):
        data = self.multiGraph(self.exponentaGraph(), self.sinGraph())
        N = len(data)
        M = 200
        dataX = [i * 0.005 for i in range(N)]
        
        max = np.max(data)
        data = [i / max * 120 for i in data]
        
        
        
        impulse = 1
        dataImpulse = []
        for i in range(N):
            if i % M == 0 and i != 0:
                dataImpulse.append(impulse)
            else:
                dataImpulse.append(0)
        
        
        dataCardio = []
        for k in range(N+M):
            yk = 0
            for m in range(M):
                try:
                    yk += dataImpulse[k-m] * data[m]
                except:
                    pass
            dataCardio.append(yk)
        
        if draw:
            plt.figure(figsize=(10, 10))
            plt.title("Кардиограмма")
            plt.grid(True)
            plt.plot(dataX, dataCardio[0:N])
            
            plt.show()
        
        return dataCardio
    
    # Метод зашумления изображения шумом типа "соль и перец"
    def ToSolidAndPeaper(self, dataImage, n):
        height = dataImage.shape[0]
        width = dataImage.shape[1]
        
        for h in range(height):
            noisePixel = random.sample(list(np.arange(width)), n)
            for i in range(n):
                dataImage[h, noisePixel[i]] = 0 if random.randint(0, 1) else 255
        
        return dataImage

    def ToRandomNoise(self, dataImage, scale):
        height = dataImage.shape[0]
        width = dataImage.shape[1]
        
        length = int(np.ceil(np.abs(width)))
        
        for h in range(height):
            dataY = np.array([int(random.uniform(-scale, scale)) for _ in range(0, length)])
            dataImage[h] += dataY
            
        return dataImage
            