from matplotlib import pyplot as plt
from sympy import *
from scipy.stats import norm
import numpy as np
import math
import PIL.Image as pil

from model import Model
from config import Config
from analysis import Analysis


class Processing():
    def __init__(self):
        self.model = Model()
        self.parametrs = Config()
        self.analysis = Analysis()

    
    def antiShift(self, data, draw=False):
        '''
        Убирает смещение по всей длине данных, вычислением среднего
        '''
        dataX = [i for i in range(len(data))]
        
        meanValue = np.mean(data)
        
        dataDefaultY = data
        dataAntiShiftY = [i - meanValue for i in data]
        
        if draw:
            plt.figure(figsize=(10,10))
            
            plt.subplot(2, 2, 1)
            plt.grid(True)
            plt.plot(dataX, dataDefaultY)
            
            plt.subplot(2, 2, 2)
            plt.grid(True)
            plt.plot(dataX, dataAntiShiftY, c="red")
            
            plt.subplot(2, 2, (3, 4))
            plt.grid(True)
            plt.plot(dataX, dataDefaultY)
            plt.plot(dataX, dataAntiShiftY, c="red")
            
            plt.show()
        
        return dataAntiShiftY
    
    def antiSpike(self, data, draw=False):
        '''
        Убирает импульсы на данных, поиском истинного максимума и минимума
        '''
        dataX = [i for i in range(len(data))]
        dataDefaultY = data
        
        sortData = sorted(data)
        
        meanIndex = int(len(data)/2)
        
        maxValue = 0
        for i in range(meanIndex, len(sortData)):
            if i + 1 != len(sortData):
                if sortData[i] >=0:
                    tempValue = sortData[i + 1] - sortData[i]
                elif sortData[i] < 0:
                    if sortData[i+1] >= 0:
                        tempValue = sortData[i + 1] + sortData[i]
                    elif sortData[i + 1] < 0:
                        tempValue = sortData[i + 1] - sortData[i]    
                        
                if tempValue > 50:
                    maxValue = sortData[i]
                    break
        
        minValue = 0
        for i in range(meanIndex, -1, -1):
            if i - 1 != -1:
                if sortData[i] < 0:
                    tempValue = sortData[i] - sortData[i - 1]
                elif sortData[i] >= 0:
                    if sortData[i - 1] >=0:
                        tempValue = sortData[i] - sortData[i - 1]
                    elif sortData[i - 1] < 0:
                        tempValue = sortData[i] + sortData[i - 1]  
                if tempValue > 50 or tempValue < -50:
                    minValue = sortData[i]
                    break
           
        dataAntiSpikeY = []
        dataAntiSpikeY.append(data[0])
        
        for i in range(1, len(data)-1):
            if data[i] > maxValue or data[i] < minValue:
                dataAntiSpikeY.append((data[i-1]+data[i+1])/2)
            else:
                dataAntiSpikeY.append((data[i]))
        dataAntiSpikeY.append(data[-1])

        
        if draw:
            plt.figure(figsize=(10,10))
            
            plt.subplot(2, 2, 1)
            plt.grid(True)
            plt.plot(dataX, dataDefaultY)
            
            plt.subplot(2, 2, 2)
            plt.grid(True)
            plt.plot(dataX, dataAntiSpikeY, c="red")
            
            plt.subplot(2, 2, (3, 4))
            plt.grid(True)
            plt.plot(dataX, dataDefaultY)
            plt.plot(dataX, dataAntiSpikeY, c="red")
            
            plt.show()
        
        return dataAntiSpikeY
    
    
    def antiTrendLinear(self, draw=False):
        '''
        Убирает линейный тренд на синусойде
        '''
        a=float(self.parametrs.GetParametr("Parametrs", "a"))
        b=float(self.parametrs.GetParametr("Parametrs", "b"))
        A0=float(self.parametrs.GetParametr("Parametrs", "A0"))
        f0=float(self.parametrs.GetParametr("Parametrs", "f0"))
        dt=float(self.parametrs.GetParametr("Parametrs", "dt"))
        thetta=float(self.parametrs.GetParametr("Parametrs", "thetta"))
        N=int(self.parametrs.GetParametr("Parametrs", "N"))
        
        
        x = Symbol('x')
        y = (x*a+b) + A0 * sin(2 * math.pi * f0 * dt * x + thetta)
        y = y.diff(x)

        dataX = [i for i in range(N)]
        dataY = [(i*a+b) + A0 * sin(2 * math.pi * f0 * dt * i + thetta) for i in range(N)]
        
        dataAntiTrendLinerY = []
        for i in range(N):
            dataAntiTrendLinerY.append(y.subs(x, i))

        if draw:
            plt.figure(figsize=(10, 10))
            
            plt.subplot(2, 1, 1)
            plt.grid(True)
            plt.plot(dataX, dataY)
            
            plt.subplot(2, 1 , 2)
            plt.grid(True)
            plt.plot(dataX, dataAntiTrendLinerY)
            
            plt.show()
        
        return dataAntiTrendLinerY
        
    def antiTrendNonLinear(self, data, draw=False):
        '''
        убирает нелинейный тренд на разных окнах
        '''
        W=[
            int(self.parametrs.GetParametr("Parametrs", "W1")),
            int(self.parametrs.GetParametr("Parametrs", "W2")),
            int(self.parametrs.GetParametr("Parametrs", "W3"))
        ]    
        
        moveARGs = []

        for w in W:
            moveARG = []
            i = 0
            while i < len(data) - w + 1:
                window = data[i: i + w]
                moveARG.append(round(sum(window) / w, 2))
                i += 1
            moveARGs.append(moveARG)

        
        if draw:
            fig, ax = plt.subplots(3, figsize=(10, 8))

            for i in range(3):
                dataAntiTrendNonLinear = []
                for j in range(len(moveARGs[i])):
                    dataAntiTrendNonLinear.append(data[j] - moveARGs[i][j])
                ax[i].plot([i for i in range(len(dataAntiTrendNonLinear))],
                        dataAntiTrendNonLinear)

            plt.show()
    
    
    def antiNoise(self, function):
        stepM=int(self.parametrs.GetParametr("Parametrs", "stepM"))
        
        plt.figure(figsize=(15,15))
        
        
        M = 1
        step = 0
        
        dataStdY = []
        
        while step < 5:
            data = function()
            for m in range(M-1):
                data += function()
            
            dataY = []
            for i in data:
                dataY.append(i/M)
            dataY = np.asarray(dataY)
            
            dataX = [i for i in range(len(dataY))]
            
            standardDeviation = round(np.std(dataY), 2)
            dataStdY.append(standardDeviation)
            
            plt.subplot(5, 2, (7, 8))
            plt.grid(True)
            plt.plot(dataX, dataY)
            plt.title("Наложение всех шумов")

            if step + 1 != 5:    
                plt.subplot(5, 2, step + 1)
                plt.grid(True)
                plt.plot(dataX, dataY)
                plt.title(f"M = {M} стандартное отклонение = {standardDeviation}")
            else:
                plt.subplot(5, 2, (5, 6))
                plt.grid(True)
                plt.plot(dataX, dataY, c="green")
                plt.title(f"M = {M} стандартное отклонение = {standardDeviation}")

            M *= stepM
            step += 1
        
        dataStdX = [i for i in range(len(dataStdY))]
        
        plt.subplot(5, 2, (9, 10))
        plt.grid(True)
        plt.plot(dataStdX, dataStdY)
            
        plt.show()
    
    
    def lpf(self, draw = False):
        '''
        ФНЧ
        '''
        fc1=float(self.parametrs.GetParametr("Parametrs", "fc"))
        fc2=float(self.parametrs.GetParametr("Parametrs", "fc1"))
        fc3=float(self.parametrs.GetParametr("Parametrs", "fc2"))
        fc = [fc1, fc2, fc3]
        m = int(self.parametrs.GetParametr("Parametrs", "m for lpf"))
        #dt = float(self.parametrs.GetParametr("Parametrs", "dt"))
        dt = 1/22100
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
            simetricLPW = reverseLPW + lpw[1::]
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
            for k in range(loper):
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
        
        for k in range(loper):
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
        
        for k in range(loper):
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
        
    def filterFourier(self):
        m = int(self.parametrs.GetParametr("Parametrs", "m for lpf"))
        
        lpw = self.lpf()[0]
        hpw = self.NewHPF()[0]
        bpw = self.bpf()
        bsw = self.bsf()
        
        loper = 2 * m + 1
        
        plt.figure(figsize=(10, 10))
        
        lpwFourier = self.analysis.spectrFourier(lpw)
        dataX = [i for i in range(len(lpwFourier))]
        dataY = [i * loper for i in lpwFourier]
        N = len(lpwFourier)
        
        plt.subplot(2, 2, 1)
        plt.title("LPF")
        plt.plot(dataX[0:int(N/2)], dataY[0:int(N/2)])
        
        
        hpwFourier = self.analysis.spectrFourier(hpw)
        dataX = [i for i in range(len(hpwFourier))]
        dataY = [i * loper for i in hpwFourier]
        N = len(hpwFourier)
        
        plt.subplot(2, 2, 2)
        plt.title("HPF")
        plt.plot(dataX[0:int(N/2)], dataY[0:int(N/2)])
        
        
        bpwFourier = self.analysis.spectrFourier(bpw)
        dataX = [i for i in range(len(bpwFourier))]
        dataY = [i * loper for i in bpwFourier]
        N = len(bpwFourier)
        
        plt.subplot(2, 2, 3)
        plt.title("BPF")
        plt.plot(dataX[0:int(N/2)], dataY[0:int(N/2)])
        
        
        bswFourier = self.analysis.spectrFourier(bsw)
        dataX = [i for i in range(len(bswFourier))]
        dataY = [i * loper for i in bswFourier]
        N = len(bswFourier)
        
        plt.subplot(2, 2, 4)
        plt.title("BSF")
        plt.plot(dataX[0:int(N/2)], dataY[0:int(N/2)])
        
        plt.show()
    

    def useFilter(self, data, filter = 0, sound = False):
        lpw = self.lpf()[0]
        hpw = self.NewHPF()[0]
        bpw = self.bpf()
        bsw = self.bsf()
        
        filters = [lpw, hpw, bpw, bsw]
        
        currentFilter = filters[filter]
        
        filterData = []
        M = 200
        N = len(data)
        for k in range(N+M):
            yk = 0
            for m in range(M):
                try:
                    yk += data[k-m] * currentFilter[m]
                except:
                    pass
            filterData.append(yk)
        
        filterData = np.asarray(filterData)
        
        self.model.drawData(filterData)
        
        if sound:
            self.analysis.spectrFourierForAudio(filterData, rate=22100, draw=True)
    
    
    def newStressedSyllable(self, data):
        c1=float(self.parametrs.GetParametr("Parametrs", "c1")) 
        c2=float(self.parametrs.GetParametr("Parametrs", "c2"))
        n1=int(float(self.parametrs.GetParametr("Parametrs", "n1")) * data["framerate"])
        n2=int(float(self.parametrs.GetParametr("Parametrs", "n2")) * data["framerate"])
        n3=int(float(self.parametrs.GetParametr("Parametrs", "n3")) * data["framerate"])
        n4=int(float(self.parametrs.GetParametr("Parametrs", "n4")) * data["framerate"])
        
        
        
        N = data["nframes"]
        oldData = data["data"]
        
        dataForMulti = [0 for i in range(0, n1)]
        dataForMulti += [c1 for i in range(n1, n2+1)]
        dataForMulti += [0 for i in range(n2+1, n3)]
        dataForMulti += [c2 for i in range(n3, n4+1)]
        dataForMulti += [0 for i in range(n4+1, N)]
        
        newData = self.model.multiGraph(oldData, dataForMulti)
        
        result = dict()
        result["nchannels"] = data["nchannels"]
        result["framerate"] = data["framerate"]
        result["nframes"] = data["nframes"]
        result["compname"] = data["compname"]
        result["sampwidth"] = data["sampwidth"]
        result["data"] = np.asarray(newData, dtype=np.short)
        
        
        plt.figure(figsize=(10, 10))
        plt.subplot(2, 1, 1)
        plt.plot(oldData)
        
        plt.subplot(2, 1, 2)
        plt.plot(newData)
        
        plt.show()
        
        return(result)
    
    
    # Обратный Фурье
    # Пометка. Решить все ту же проблему с универсальностью изображения (как вариант надо будет сделать проверку в классе на то находится ли изображение в сером диапозоне)
    def InverseFurie(self, dataImage, mode = 1):
        newDataImage = np.empty((dataImage.shape[0], dataImage.shape[1]))
        
        for h in range(dataImage.shape[0]):
            for w in range(dataImage.shape[1]):
                try:
                    newDataImage[h, w] = dataImage[h, w]
                except:
                    newDataImage[h, w] = dataImage[h, w, 0]
        
        N = 1000  # количество значений в входном сигнале
        M = 200  # количество значений в функции h
        step = 1  # шаг по умолчанию
        dt = 0.005  # шаг дискретизации

        A = 10  # тестовая амплитуда гармонического процесса
        f = 4   # тестовая частота гармонического процесса
        
        
        sinDataX = np.arange(0, M * dt, dt)
        sinDataY = A * np.sin(2 * np.pi * f * sinDataX)
         

        plt.plot(sinDataX, sinDataY)
        plt.title("Синусойда")
        plt.grid(True)
        plt.show()
        
        dataX, dataY = self.__FourierTransform(sinDataY, 0, M, 1, 1, 1) 
        plt.figure(figsize=(8, 3))
        plt.plot(dataX[0:int(M/2)], dataY[0:int(M/2)])
        plt.title("Прямой Фурье")
        plt.grid(True)
        plt.show()
        

        dataX, dataY = self.__FourierTransform(dataY, 0, M, 1, 1, 1) 
        plt.plot(dataX[0:int(M/2)], dataY[0:int(M/2)])
        plt.title("Обратное Фурье")
        plt.grid(True)
        plt.show()
        
        if mode == 1:
            newDataImage = self.FourierTransform2D(newDataImage, 1)
            newDataImage = (20 * np.log(newDataImage + 1)).round()
        elif mode == 2:
            newDataImage = self.FourierTransform2D(newDataImage, 2)
            newDataImage = (20 * np.log(newDataImage + 1)).round()
        else:
            newDataImage = self.FourierTransform2D(newDataImage, 3)
            
        return newDataImage


    
    def FourierTransform2D(self, dataImage, mode=1):
        height = dataImage.shape[0]
        width = dataImage.shape[1]
        
        res = np.zeros((height, width))
        iter1 = height
        iter2 = width
        
        if mode == 3:
            iter1 = width
            iter2 = height
        for i in range(iter1):
            if mode == 3:
                dataLineY = dataImage[:, i].copy()
            else:
                dataLineY =  dataImage[i].copy()
            
            dataX, dataY = self.__FourierTransform(dataLineY, 0, iter2, 1, 1, mode) 
            
            if mode == 1:
                swap = np.empty(iter2)
                for k in range(iter2):
                    if k < int(iter2 / 2):
                        swap[k + int(iter2 / 2)] = dataY[k]
                    else:
                        swap[k - int(iter2 / 2)] = dataY[k]
                dataY = swap
            if mode == 3:
                res[:, i] = dataY
            else:
                res[i] = dataY
                
        for i in range(iter2):            
            if mode == 3:
                dataLineY = res[i].copy()
            else:
                dataLineY = res[:, i].copy()
            
            dataX, dataY = self.__FourierTransform(dataLineY, 0, iter1, 1, 1, mode) 
            
            if mode == 1:
                swap = np.empty(iter1)
                for k in range(iter1):
                    if k < int(iter1 / 2):
                        swap[k + int(iter1 / 2)] = dataY[k]
                    else:
                        swap[k - int(iter1 / 2)] = dataY[k]
                dataY = swap
            if mode == 3:
                res[i] = dataY
            else:
                res[:, i] = dataY
        dataImage = res.astype(float)
        
        return dataImage



