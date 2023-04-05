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
        hpw = self.hpf()[0]
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
        hpw = self.hpf()[0]
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
        
    
    # Смещение данных изображения на заданный коэффицент
    def shift2D(self, dataImage):
        shifImage = int(self.parametrs.GetParametr("Parametrs", "shiftImage"))
        
        for i in range(len(dataImage)):
            for j in range(len(dataImage[i])):
                dataImage[i][j] = dataImage[i][j] + shifImage
        
        return dataImage
    
    
    # Умножение данных изображения на заданный коэффицент
    def multModel2D(self, dataImage):
        multiImage = float(self.parametrs.GetParametr("Parametrs", "multiImage"))
        
        for i in range(len(dataImage)):
            for j in range(len(dataImage[i])):
                dataImage[i][j] = dataImage[i][j] * multiImage
           
        return dataImage
    
    
    # Приведение к серому диапозону
    def toGray(self, dataImage):
        maxPixel = dataImage.max();
        minPixel = dataImage.min();
        
        for i in range(len(dataImage)):
            for j in range(len(dataImage[i])):
                dataImage[i][j] = ((dataImage[i][j] - minPixel) / (maxPixel - minPixel)) * 255
        
        return dataImage
    
    
    # Изменение размера методом ближайших соседей
    def resizeNearestImage(self, dataImage):
        multiSize = float(self.parametrs.GetParametr("Parametrs", "multiSize"))
        
        w = dataImage.shape[1]
        h = dataImage.shape[0]
        
        newSizeW = int(w * multiSize)
        newSizeH = int(h * multiSize)
        
        emptyImage=np.zeros((newSizeH, newSizeW, 3))
        
        sh = newSizeH / h
        sw = newSizeW / w
        
        for i in range(newSizeH):
            for j in range(newSizeW):
                x=int(i/sh)
                y=int(j/sw)
                try:
                    emptyImage[i,j]=dataImage[x,y]
                except:
                    print(x, y)
        
        return emptyImage
    
    
    # Изменение размера бинарным методом
    def resizeBinaryImage(self, dataImage):
        multiSize = float(self.parametrs.GetParametr("Parametrs", "multiSize"))
        
        w = dataImage.shape[1]
        h = dataImage.shape[0]
        
        newSizeW = int(w * multiSize)
        newSizeH = int(h * multiSize)
        
        emptyImage=np.zeros((newSizeH, newSizeW, 3), np.uint8)
        value=[0,0,0]
        
        sh = newSizeH / h
        sw = newSizeW / w
        
        for i in range(newSizeH):
            for j in range(newSizeW):
                x= i/sh
                y= j/sw
                p=(i+0.0)/sh-x
                q=(j+0.0)/sw-y
                x=int(x)-1
                y=int(y)-1
                for k in range(3):
                    try:
                        if x+1<newSizeH and y+1<newSizeW:
                            value[k]=int(dataImage[x][y][k]*(1-p)*(1-q)+
                                    dataImage[x][y+1][k]*q*(1-p)+
                                    dataImage[x+1][y][k]*(1-q)*p+
                                    dataImage[x+1][y+1][k]*p*q)
                    except:
                        print(x, y)
                try:
                    emptyImage[i, j] = (value[0], value[1], value[2])
                except:
                    print(x, y)
        
        return dataImage
    
    
    # Поворот изображения
    def rotateImage(self, dataImage, isRight = true):
        dataImage = dataImage.astype('uint8')
        image = pil.fromarray(dataImage)
        
        if isRight:
            im_rotate = image.rotate(-90, expand=True)
        else:
            im_rotate = image.rotate(90, expand=True)
        
        dataImage = np.array(im_rotate)
        dataImage = dataImage.astype('int32')
        
        return dataImage
    
    # Делает изображение негативным
    def doNegative(self, dataImage):
        L = dataImage.max()
        
        for i in range(len(dataImage)):
            for j in range(len(dataImage[i])):
                dataImage[i][j] = L - 1 - dataImage[i][j]
        
        return dataImage
    
    
    # Делает цветное изображение серым
    def doGray(self, dataImage):
        
        for i in range(len(dataImage)):
            for j in range(len(dataImage[i])):
                r = dataImage[i][j][0]
                g = dataImage[i][j][1]
                b = dataImage[i][j][2]
                
                s = (r + g + b) // 3
                
                dataImage[i][j][0] = s
                dataImage[i][j][1] = s
                dataImage[i][j][2] = s
        
        return dataImage
    
    
    # Гамма преобразование
    def gammaTransform(self, dataImage):
        C = float(self.parametrs.GetParametr("Parametrs", "C"))
        y = float(self.parametrs.GetParametr("Parametrs", "y"))
        
        
        for i in range(len(dataImage)):
            for j in range(len(dataImage[i])):
                # print(dataImage[i][j])
                dataImage[i][j] = C * dataImage[i][j] ** y

        dataImage = self.toGray(dataImage)
        
        return dataImage
    
    
    # Логарифмическое преобразование
    def logTransform(self, dataImage):
        C = float(self.parametrs.GetParametr("Parametrs", "C"))
        
        
        for i in range(len(dataImage)):
            for j in range(len(dataImage[i])):
                dataImage[i][j] = C * np.log(dataImage[i][j] + 1)
        
        dataImage = self.toGray(dataImage)
        
        return dataImage
    
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
    def ResultForLab5(self, dataImage):
        STEP = 200
        
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
        
        n = 3  # количество графиков
        
        plt.figure(figsize=(15, 4))
        plt.title('Спектры исходных строк изображения')
        for i in range(n):
            func = Function(0, newDataImage.shape[1], 1)
            func.Y = newDataImage[int(i * STEP)]
            fourier = Function(0, newDataImage.shape[1], 1)
            fourier.fourier_transform(func, 1, 1, False, True)
            fourier.X = fourier.X / newDataImage.shape[1]
            plt.subplot(1, 3, i + 1)
            plt.plot(fourier.X, fourier.Y)
            plt.title(str(i * STEP + 1) + " строк")
            plt.xlabel("Частота")
            plt.ylabel("Амплитуда")
            plt.grid(True)
            
        plt.show()


        plt.figure(figsize=(15, 4))
        plt.title('Спектры производных строк изображения')
        for i in range(n):
            func = Function(0, derivatives.shape[1], 1)
            func.Y = derivatives[i]
            fourier = Function(0, derivatives.shape[1], 1)
            fourier.fourier_transform(func, 1, 1, False, True)
            fourier.X = fourier.X / newDataImage.shape[1]
            plt.subplot(1, n, i + 1)
            plt.plot(fourier.X, fourier.Y)
            plt.title(str(i * STEP + 1) + " строк")
            plt.xlabel("Частота")
            plt.ylabel("Амплитуда")
            plt.grid(True)
        
        plt.show()
        
        
        plt.figure(figsize=(15, 4))
        plt.title('Спектры автокорреляций производных')
        for i in range(n):
            func = Function(0, autoCorrelations.shape[1], 1)
            func.Y = autoCorrelations[i]
            fourier = Function(0, autoCorrelations.shape[1], 1)
            fourier.fourier_transform(func, 1, 1, False, True)
            fourier.X = fourier.X / newDataImage.shape[1]
            plt.subplot(1, n, i + 1)
            plt.plot(fourier.X, fourier.Y)
            plt.title(str(i * STEP + 1) + " строк")
            plt.xlabel("Частота")
            plt.ylabel("Амплитуда")
            plt.grid(True)

        plt.show()
        
        
        plt.figure(figsize=(15, 4))
        plt.title('Спектры взаимных корреляций производных')
        for i in range(2):
            func = Function(0, correlations.shape[1], 1)
            func.Y = correlations[i]
            fourier = Function(0, correlations.shape[1], 1)
            fourier.fourier_transform(func, 1, 1, False, True)
            fourier.X = fourier.X / newDataImage.shape[1]
            plt.subplot(1, 2, i + 1)
            plt.plot(fourier.X, fourier.Y)
            plt.title(str(i * STEP + 1) + " строк" + "и " + str((i + 1) * STEP + 1) + " строк")
            plt.xlabel("Частота")
            plt.ylabel("Амплитуда")
            plt.grid(True)

        plt.show()
        
        
        bottom = 0.25  # нижняя частота
        top = 0.35  # верхняя частота
        m = 32  # параметр фильтрации (длина фильтра)

        newDataImage = self.ImageFilter(newDataImage, 3, m, bottom, top)
        
        return newDataImage
    
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
    
    # Метод получения индексов максимумов в строках двумерного списка
    def GetFourierSpikes(lself, listFourier):
        lHeight = len(listFourier)
        spikes = np.empty(lHeight)
        for i in range(lHeight):
            spikes[i] = listFourier[i].X[listFourier[i].Y.argmax()]
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

    # Метод получения амплитудных спектров Фурье строк двумерного массива
    def GetFourierSpectr(self, arrRows):
        arrHeight = arrRows.shape[0]
        arrWidth = arrRows.shape[1]
        
        dt = 1 / arrWidth
        spectra = []
        
        for i in range(arrHeight):
            func = Function(0, arrWidth * dt, dt)
            func.Y = arrRows[i].copy()
            fourier = Function(0, arrWidth, 1)
            fourier.fourier_transform(func, 1, 1, False, True)
            fourier.X = fourier.X / arrWidth
            spectra.append(fourier)
        return spectra


    def ImageFilter(self, dataImage, kind, m, fc1, fc2=None):
        width = dataImage.shape[1]
        height = dataImage.shape[0]
        
        dt = 1 / width
        filter_P = Function(0, 2 * m + 1, 1)
        if kind == 1:
            filter_P.lpf(fc1, dt, m)
        elif kind == 2:
            filter_P.hpf(fc1, dt, m)
        elif kind == 3:
            filter_P.bsf(fc1, fc2, dt, m)
    
        for h in range(height):
            funcRow = Function(0, width * dt, dt)
            funcRow.Y = dataImage[h].copy()
            funcConv = Function(0, width * dt, dt)
            funcConv.convolution_func(funcRow, filter_P)
            for w in range(width):
                if w < width - m:
                    dataImage[h, w] = funcConv.Y[w + m]
                else:
                    dataImage[h, w] = funcConv.Y[w - width + m]

        return dataImage
    
    #####################
    # Усредняющий арифметический фильтр
    def MiddleFilter(self, dataImage):
        maskSize = 50
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
        maskSize = 50
        
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
    

        
import numpy as np
import random
import matplotlib.pyplot as plt

# Класс математических функций
class Function:
    # Конструктор класса
    #
    # start - начальное значение оси абсцисс
    # end - конечное значение оси абсцисс
    # step - шаг
    def __init__(self, start=None, end=None, step=None):
        if start is not None and end is not None and step is not None:
            self.initializeX(start, end, step)
            self.initializeY()

    # Инициализация оси абсцисс
    #
    # start - начальное значение оси абсцисс
    # end - конечное значение оси абсцисс
    # step - шаг
    def initializeX(self, start, end, step):
        self.start = start
        self.end = end
        self.step = step
        self.length = int(np.ceil(np.abs(end - start) / step))
        self.X = np.arange(start, end, step)

    # Инициализация оси ординат
    def initializeY(self):
        self.Y = np.zeros(self.length)

    # Функция экспоненты вида b*exp^(-a*x)
    def exp(self, a, b):
        self.Y = np.exp(-a * self.X) * b

    # Функция синусоиды
    #
    # A - амплитуда
    # f - частота
    def sin(self, A, f):
        self.Y = A * np.sin(2 * np.pi * f * self.X)

    # Функция сложной синусоиды
    #
    # arrA - массив амплитуд
    # arrF - массив частот
    def complex_sin(self, arrA, arrF):
        for i in range(0, len(arrA)):
            self.Y += arrA[i] * np.sin(2 * np.pi * arrF[i] * self.X)

    # Функция случайного шума
    #
    # scale - диапазон шума
    def rand(self, scale):
        self.Y = np.array([random.uniform(-scale, scale) for _ in range(0, self.length)])

    # Метод произведения функций
    #
    # arrFunc - массив функций
    def multiply_func(self, arrFunc):
        self.Y = 1
        for i in range(0, len(arrFunc)):
            self.Y *= arrFunc[i].Y.copy()

    # Метод свёртки функций
    def convolution_func(self, x, h):
        N = x.length
        M = h.length
        self.Y = np.zeros(N + M)  # меняем количесвто значений функции
        for k in range(0, N + M):
            sum = 0
            for j in range(0, M):
                try:
                    sum += x.Y[k - j] * h.Y[j]
                except:
                    sum += 0
            self.Y[k] = sum
        self.Y = np.array(list(self.Y)[: len(self.Y) - M])  # удаляем справа M значений

    # Метод преобразований Фурье
    #
    # func - исходная функция
    # window - окно [0..1]
    # kind - тип преобразования
    ## kind = 1 - Амплитудный спектр Фурье
    ## kind = 2 - Прямое преобразование Фурье
    ## kind = 3 - Обратное преобразование Фурье
    # freq - привести шкалу абсцисс к [Гц]
    # half - отобразить половину шкалы
    # dt - шаг дискретизации
    def fourier_transform(self, func, window, kind=1, freq=False, half=False, dt=1):
        lenZeros = int(func.length * (1 - window) / 2)
        for i in range(0, lenZeros):
            func.Y[i] = 0
            func.Y[N - i - 1] = 0
        sumRe, sumIm = 0, 0
        for k in range(0, func.length):
            sumRe += func.Y[k] * np.cos(2 * np.pi * self.X * k / func.length)
            sumIm += func.Y[k] * np.sin(2 * np.pi * self.X * k / func.length)
        Re = (1 / func.length) * sumRe
        Im = (1 / func.length) * sumIm
        if kind == 1:
            self.Y = (Re ** 2 + Im ** 2) ** 0.5
        elif kind == 2:
            self.Y = Re + Im
        else:
            self.Y = sumRe + sumIm
        if freq:
            # переходим от параметра n к f
            df = 1 / (self.end * dt)
            self.initializeX(self.start, self.end * df, df)
        if half:
            # берём первую половину графика
            self.initializeX(self.start, int(self.end / 2), self.step)
            self.Y = np.array(list(self.Y)[:self.length])

    # Метод восстановления функции
    #
    # func1 - исходная функция
    # func2 - искажающая функция
    # alpha - параметр [0..1]
    def recover(self, func1, func2, alpha2=0):
        sumRe1, sumIm1 = 0, 0
        sumRe2, sumIm2 = 0, 0
        for k in range(0, func1.length):
            sumRe1 += func1.Y[k] * np.cos(2 * np.pi * self.X * k / func1.length)
            sumIm1 += func1.Y[k] * np.sin(2 * np.pi * self.X * k / func1.length)
            sumRe2 += func2.Y[k] * np.cos(2 * np.pi * self.X * k / func2.length)
            sumIm2 += func2.Y[k] * np.sin(2 * np.pi * self.X * k / func2.length)
        Re1 = (1 / func1.length) * sumRe1
        Im1 = (1 / func1.length) * sumIm1
        Re2 = (1 / func2.length) * sumRe2
        Im2 = (1 / func2.length) * sumIm2
        self.Y = (Re1 * Re2 + Im1 * Im2 - Re1 * Im2 + Re2 * Im1) / (alpha2 + np.abs(Re2 ** 2 + Im2 ** 2))

    # Метод нормализации функции
    def normalize(self):
        maxY = self.Y.max()
        for i in range(0, self.length):
            self.Y[i] = self.Y[i] / maxY

    # Метод для расчёта весов фильтра низких частот Поттера
    #
    # fc - частота
    # dt - шаг дискретизации
    # m - параметр (длина фильтра)
    def lpf(self, fc, dt, m):
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
        self.Y = np.array(lpwRes + lpw)

    # Метод для расчёта весов фильтра высоких частот Поттера
    #
    # fc - частота
    # dt - шаг дискретизации
    # m - параметр (длина фильтра)
    def hpf(self, fc, dt, m):
        lpw = Function(0, 2 * m + 1, 1)
        lpw.lpf(fc, dt, m)
        loper = 2 * m + 1
        hpw = [0 for _ in range(0, loper)]
        for k in range(0, loper):
            if k == m:
                hpw[k] = 1 - lpw.Y[k]
            else:
                hpw[k] = -1 * lpw.Y[k]
        self.Y = np.array(hpw)

    # Метод для расчёта весов полосового фильтра Поттера
    #
    # fc1 - нижняя частота
    # fc2 - верхняя частота
    # dt - шаг дискретизации
    # m - параметр (длина фильтра)
    def bpf(self, fc1, fc2, dt, m):
        lpw1 = Function(0, 2 * m + 1, 1)
        lpw1.lpf(fc1, dt, m)
        lpw2 = Function(0, 2 * m + 1, 1)
        lpw2.lpf(fc2, dt, m)
        loper = 2 * m + 1
        bpw = [0 for _ in range(0, loper)]
        for k in range(0, loper):
            bpw[k] = lpw2.Y[k] - lpw1.Y[k]
        self.Y = np.array(bpw)

    # Метод для расчёта весов режекторного фильтра Поттера
    #
    # fc1 - нижняя частота
    # fc2 - верхняя частота
    # dt - шаг дискретизации
    # m - параметр (длина фильтра)
    def bsf(self, fc1, fc2, dt, m):
        lpw1 = Function(0, 2 * m + 1, 1)
        lpw1.lpf(fc1, dt, m)
        lpw2 = Function(0, 2 * m + 1, 1)
        lpw2.lpf(fc2, dt, m)
        loper = 2 * m + 1
        bsw = [0 for _ in range(0, loper)]
        for k in range(0, loper):
            if k == m:
                bsw[k] = 1 + lpw1.Y[k] - lpw2.Y[k]
            else:
                bsw[k] = lpw1.Y[k] - lpw2.Y[k]
        self.Y = np.array(bsw)

    # Метод для отображения графика функции
    #
    # title - название графика
    # xlabel - название оси абсцисс
    # ylabel - название оси ординат
    def display(self, title, xlabel='x', ylabel='y'):
        plt.plot(self.X, self.Y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        #plt.grid(True)