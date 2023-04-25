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
    
    
    
    
    # Градиционное преобразование
    def ImageGradientTransform(self, dataImage):
        newDataImage = []
        L = dataImage.max()
        
        if len(dataImage.shape) == 3:
            M, N, _ = dataImage.shape
            for i in dataImage:
                for j in i:
                    newDataImage.append(j[0])
        else:
            M, N = dataImage.shape
            for i in dataImage:
                for j in i:
                    newDataImage.append(j)
        
        pixelCountResult, _, _ = plt.hist(newDataImage, bins=256, rwidth=0.8, range=(0, 255))
        plt.show()
        pixelCountResult = pixelCountResult / (M * N)
        
        cdf = []
        cdf.append(pixelCountResult[0])
        for i in range(1, len(pixelCountResult)):
            cdf.append(cdf[int(i) - 1] + pixelCountResult[int(i)])
        
        plt.plot(cdf)
        plt.show()
        
        resultData = []
        for i in newDataImage:
            resultData.append(cdf[int(i)] * L)
        
        resultData = np.array(resultData)        
        
        resultData = np.reshape(resultData, (M, N))
        
        resultData = self.toGray(resultData)
        
        return resultData
    
    
    
    
    ########################
    # Кореляция
    # Пометка. 1) Решить проблему с массивом изображения;
    #          2) Сделать новый класс для работы и хранения изображения
    #          3) Сделать универсальное сохранение и открытие изображений в новом классе
    def ResultForLab5(self, dataImage):
        STEP = 400
        
        newDataImage = np.empty((dataImage.shape[0], dataImage.shape[1]))
        
        for h in range(dataImage.shape[0]):
            for w in range(dataImage.shape[1]):
                try:
                    newDataImage[h, w] = dataImage[h, w]
                except:
                    newDataImage[h, w] = dataImage[h, w, 0]
        
        derivatives = self.GetDerivatives(STEP, dataImage)
        
        autoCorrelations = self.GetAutoCorr(derivatives)
        correlations = self.GetCorrBetweenRows(derivatives)
        
        spectrAutoCorrelations = self.GetFourierSpectr(autoCorrelations)
        spectraCorrelations = self.GetFourierSpectr(correlations)

        spikesSpectrAutoCorrelations = self.GetFourierSpikes(spectrAutoCorrelations)
        spikesSpectraCorrelations = self.GetFourierSpikes(spectraCorrelations)
        
        print("Максимумы спектров автокорреляций производных:", spikesSpectrAutoCorrelations)
        print("Максимумы спектров взаимных корреляций производных:", spikesSpectraCorrelations)
        
        
        plt.figure(figsize=(15, 4))
        plt.title('Спектры исходных строк изображения')
        for i in range(3):
            dataX, dataY = self.__FourierTransform(newDataImage[int(i * STEP)], 0, newDataImage.shape[1], 1, 1, 1)
            
            dataX = dataX / newDataImage.shape[1]
            
            middleIndex = int(len(dataX)/2)
            
            plt.subplot(1, 3, i + 1)
            plt.plot(dataX[0:middleIndex], dataY[0:middleIndex])
            plt.title(str(i * STEP + 1) + " строк")
            plt.xlabel("Частота")
            plt.ylabel("Амплитуда")
            plt.grid(True)
        
        plt.show()
        
        
        plt.figure(figsize=(15, 4))
        plt.title('Спектры производных строк изображения')
        for i in range(3):
            dataX, dataY = self.__FourierTransform(derivatives[i], 0, derivatives.shape[1], 1, 1, 1)
            
            dataX = dataX / newDataImage.shape[1]
            
            middleIndex = int(len(dataX)/2)
            
            plt.subplot(1, 3, i + 1)
            plt.plot(dataX[0:middleIndex], dataY[0:middleIndex])
            plt.title(str(i * STEP + 1) + " строк")
            plt.xlabel("Частота")
            plt.ylabel("Амплитуда")
            plt.grid(True)
            
        plt.show()
        
        plt.figure(figsize=(15, 4))
        plt.title('Спектры автокорреляций производных')
        for i in range(3):
            dataX, dataY = self.__FourierTransform(autoCorrelations[i], 0, autoCorrelations.shape[1], 1, 1, 1)
            
            dataX = dataX / newDataImage.shape[1]
            
            middleIndex = int(len(dataX)/2)
            
            plt.subplot(1, 3, i + 1)
            plt.plot(dataX[0:middleIndex], dataY[0:middleIndex])
            plt.title(str(i * STEP + 1) + " строк")
            plt.xlabel("Частота")
            plt.ylabel("Амплитуда")
            plt.grid(True)
        
        plt.show()
        
        plt.figure(figsize=(15, 4))
        plt.title('Спектры взаимных корреляций производных')
        for i in range(2):
            dataX, dataY = self.__FourierTransform(correlations[i], 0, correlations.shape[1], 1, 1, 1)
            
            dataX = dataX / newDataImage.shape[1]
            
            middleIndex = int(len(dataX)/2)
            
            plt.subplot(1, 2, i + 1)
            plt.plot(dataX[0:middleIndex], dataY[0:middleIndex])
            plt.title(str(i * STEP + 1) + " строк" + "и " + str((i + 1) * STEP + 1) + " строк")
            plt.xlabel("Частота")
            plt.ylabel("Амплитуда")
            plt.grid(True)

        plt.show()
        
        
        bottom = 0.2  # нижняя частота
        top = 0.3  # верхняя частота
        m = 32  # параметр фильтрации (длина фильтра)
        
        newDataImage = self.ImageFilter(newDataImage, 3, m, bottom, top)
        
        return newDataImage
    
    # Автокорреляция
    def __AutoCorr(self, func):
        N = func.size
        meanF = np.mean(func)
        corr = np.empty(N)
        for l in range(N):
            sum1 = 0
            sum2 = 0
            for k in range(N - l):
                sum1 += (func[k] - meanF) * (func[k + l] - meanF)
            for k in range(N):
                sum2 += (func[k] - meanF) * (func[k] - meanF)
            corr[l] = sum1 / sum2
        return corr

    # Взаимная корреляция
    def __Corr(self, func1, func2):
        N = func1.size
        meanF1 = np.mean(func1)
        meanF2 = np.mean(func2)
        corr = np.empty(N)
        for l in range(N):
            sum = 0
            for k in range(N - l):
                sum += (func1[k] - meanF1) * (func2[k + l] - meanF2)
            corr[l] = sum / N
        return corr
    
    
    # Фуцнкция получения производных строк изображения
    # Пометка. Переделать под универсальный массив изображений (глянуть библиотеку OpenCV)
    def GetDerivatives(self, step, dataImage):
            try:
                if len(dataImage[0][0]) != 3:
                    sizeW, sizeH = dataImage.shape
                else:
                    sizeH, sizeW, _ = dataImage.shape
            except:
                sizeW, sizeH = dataImage.shape
            
            derHeight = int(np.ceil(sizeH / step))
            derWidth = int(sizeW - 1)
            
            print(derWidth, derHeight)
            
            derivatives = np.empty((derHeight, derWidth))
            
            for h in range(derHeight):
                for w in range(derWidth):
                    try:
                        derivatives[h, w] = dataImage[int(h * step), w + 1] - dataImage[int(h * step), w]
                    except:
                        derivatives[h, w] = dataImage[int(h * step), w + 1, 0] - dataImage[int(h * step), w, 0]
            
            return derivatives
    
    # Функция получения индексов максимумов в строках двумерного списка
    def GetFourierSpikes(lself, listFourier):
        lHeight = len(listFourier)
        spikes = np.empty(lHeight)
        for i in range(lHeight):
           spikes[i] = listFourier[i].max()
        return spikes

    
    # Функция получения автокорреляций строк двумерного массива
    def GetAutoCorr(self, arrRows):
        corrHeight = arrRows.shape[0]
        corrWidth = arrRows.shape[1]
        correlations = np.empty((corrHeight, corrWidth))
        
        for h in range(corrHeight):
            corr = self.__AutoCorr(arrRows[h])
            for w in range(corrWidth):
                correlations[h, w] = corr[w]
        return correlations


    # Метод получения взаимных корреляций строк двумерного массива
    def GetCorrBetweenRows(self, arrRows):
        corrHeight = arrRows.shape[0] - 1
        corrWidth = arrRows.shape[1]
        correlations = np.empty((corrHeight, corrWidth))
        
        for h in range(corrHeight):
            corr = self.__Corr(arrRows[h], arrRows[h + 1])
            for w in range(corrWidth):
                correlations[h, w] = corr[w]
        return correlations
    
    
    def __FourierTransform(self, data, startIndex, endIndex, step, window, mode=1):
        length = int(np.ceil(np.abs(endIndex - startIndex) / step))
        
        dataY = data
        dataX = np.arange(startIndex, endIndex, step)
        
        lenZeros = int(length * (1 - window) / 2)
        
        for i in range(0, lenZeros):
            dataY[i] = 0
            dataY[N - i - 1] = 0
        sumRe, sumIm = 0, 0
        
        for k in range(0, length):
            sumRe += dataY[k] * np.cos(2 * np.pi * dataX * k / length)
            sumIm += dataY[k] * np.sin(2 * np.pi * dataX * k / length)
        Re = (1 / length) * sumRe
        Im = (1 / length) * sumIm
        if mode == 1:
            dataY = (Re ** 2 + Im ** 2) ** 0.5
        elif mode == 2:
            dataY = Re + Im
        else:
            dataY = sumRe + sumIm
        
        return dataX, dataY
    
    
    # Метод получения амплитудных спектров Фурье строк двумерного массива
    def GetFourierSpectr(self, arrRows):
        arrHeight = arrRows.shape[0]
        arrWidth = arrRows.shape[1]
        
        dt = 1 / arrWidth
        spectra = []
        
        for i in range(arrHeight):
            
            dataX, dataY = self.__FourierTransform(arrRows[i].copy(), 0, arrWidth, 1, 1, 1)
            
            dataX = dataX / arrWidth
            
            spectra.append(dataY)
        return spectra

    def ImageFilter(self, dataImage, mode, m, fc1, fc2=None):
        width = dataImage.shape[1]
        height = dataImage.shape[0]
        
        dt = 1 / width
        
        if mode == 1:
            dataFilter = self.NewLPF(fc1, dt, m)
        elif mode == 2:
            dataFilter = self.NewHPF(fc1, dt, m)
        elif mode == 3:
            dataFilter = self.NewBSF(fc1, fc2, dt, m)
        
        for h in range(height): 
            dataRow = dataImage[h].copy()
            
            dataConv = self.Convolution(dataRow, dataFilter, 1)
            
            for w in range(width):
                if w < width - m:
                    dataImage[h, w] = dataConv[w + m]
                else:
                    dataImage[h, w] = dataConv[w - width + m]
                    
        return dataImage
    
    
    
    def Convolution(self, data1, data2, step):
        
        N = int(np.ceil(np.abs(len(data1)) / step))
        M= int(np.ceil(np.abs(len(data1)) / step))
        
        dataY = np.zeros(N + M)
        
        for k in range(0, N + M):
            sum = 0
            for j in range(0, M):
                try:
                    sum += data1[k - j] * data2[j]
                except:
                    sum += 0
            dataY[k] = sum
        
        dataY = np.array(list(dataY)[: len(dataY) - M])
        
        return dataY
    
    # Пометка. Надо сделать отдельный класс для фильтров, так как накопилось уже мног
    # Пометка 2. Подумать над именованием или переопределении методов. А еще стоит разделить логику с лабами из прошлого семестра
    # Фильтр низких частот Поттера
    def NewLPF(self, fc, dt, m):
        d = [0.35577019, 0.2436983, 0.07211497, 0.00630165]
        fact = float(2 * fc)
        lpw = []
        lpw.append(fact)
        arg = fact * np.pi
        for i in range(1, m + 1):
            lpw.append(np.sin(arg * i) / (np.pi * i))
        lpw[m] /= 2
        sumg = lpw[0]
        for i in range(1, m + 1):
            sum = d[0]
            arg = np.pi * i / m
            for k in range(1, 4):
                sum += 2 * d[k] * np.cos(arg * k)
            lpw[i] *= sum
            sumg += 2 * lpw[i]
        for i in range(0, m + 1):
            lpw[i] /= sumg
        lpwRes = []
        for i in range(len(lpw) - 1, 0, -1):
            lpwRes.append(lpw[i])
        return np.array(lpwRes + lpw)

    # Фильтр высоких частот Поттера
    def NewHPF(self, fc, dt, m):
        lpf = self.NewLPF(fc, dt, m)
        loper = 2 * m + 1
        hpw = [0 for _ in range(0, loper)]
        for k in range(0, loper):
            if k == m:
                hpw[k] = 1 - lpf[k]
            else:
                hpw[k] = -1 * lpf[k]
        return np.array(hpw)

    # Полосовой фильтр Поттера
    def NewBPF(self, fc1, fc2, dt, m):
        lpw1 = self.NewLPF(fc1, dt, m)
        lpw2 = self.NewLPF(fc2, dt, m)
        loper = 2 * m + 1
        bpw = [0 for _ in range(0, loper)]
        for k in range(0, loper):
            bpw[k] = lpw2[k] - lpw1[k]
        return np.array(bpw)

    # Режекторный фильтр Поттера
    def NewBSF(self, fc1, fc2, dt, m):
        lpw1 = self.NewLPF(fc1, dt, m)
        lpw2 = self.NewLPF(fc2, dt, m)
        loper = 2 * m + 1
        bsw = [0 for _ in range(0, loper)]
        for k in range(0, loper):
            if k == m:
                bsw[k] = 1 + lpw1[k] - lpw2[k]
            else:
                bsw[k] = lpw1[k] - lpw2[k]
        return np.array(bsw)
        
    #####################
    # Усредняющий арифметический фильтр
    def MiddleFilter(self, dataImage):
        maskSize = 10
        maskList = [np.zeros((maskSize, maskSize), dtype=float) + 1]
        
        a = int((maskList[0].shape[0] - 1) / 2)
        b = int((maskList[0].shape[1] - 1) / 2)
        
        height = dataImage.shape[0]
        width = dataImage.shape[1]
        
        newDataImage = np.empty((height, width))
        
        for h in range(height):
            for w in range(width):
                sum1 = 0
                for i in range(len(maskList)):
                    sum2 = 0
                    for s in range(-1 * a, a + 1):
                        sum3 = 0
                        for t in range(-1 * b, b + 1):
                            try:
                                sum3 += maskList[i][s + 1, t + 1] * dataImage[h + s, w + t]
                            except:
                                pass
                        sum2 += sum3
                    sum1 += np.abs(sum2)
                newDataImage[h, w] = sum1
        
        newDataImage = newDataImage / (maskSize * maskSize)
        
        return newDataImage
    
    # Медианный фильтр
    def MedianFilter(self, dataImage):
        maskSize = 5010
        a = int((maskSize - 1) / 2)
        b = int((maskSize - 1) / 2)
        
        height = dataImage.shape[0]
        width = dataImage.shape[1]
        
        newDataImage = np.empty((height, width))
        
        for h in range(height):
            for w in range(width):
                l = []
                for s in range(-1 * a, a + 1):
                    for t in range(-1 * b, b + 1):
                        try:
                            l.append(dataImage[h + s, w + t])
                        except:
                            pass
                newDataImage[h, w] = np.median(l)
        
        return newDataImage
    
    def GenerateImageBlackAndWhiteSqard(self):
        sizeBlackSqard = 256
        sizeWhiteSqard = 30
        
        newDataImage = np.empty((sizeBlackSqard, sizeBlackSqard))
        
        indexForWhiteSqardStart = sizeBlackSqard/2 - sizeWhiteSqard/2
        indexForWhiteSqardEnd = sizeBlackSqard/2 + sizeWhiteSqard/2
        
        for h in range(sizeBlackSqard):
            for w in range(sizeBlackSqard):
                if (w >= indexForWhiteSqardStart and w <= indexForWhiteSqardEnd) and (h >= indexForWhiteSqardStart and h <= indexForWhiteSqardEnd):
                    newDataImage[h, w] = 0
                else:
                    newDataImage[h, w] = 256
        
        return newDataImage
            
    
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



