import numpy as np
from scipy.fft import fft
from matplotlib import pyplot as plt
from model import Model
from config import Config

class Analysis:
    def __init__(self):
        self.model = Model()
        self.parametrs = Config()

    def statistics(self, data):
        '''
        Возвращает статистику по переданным данным
        '''
        data = np.asarray(data)
        min = round(np.min(data), 2)
        max = round(np.max(data), 2)
        meanValue = round(np.mean(data), 2)
        variance = round(np.var(data), 2)
        standardDeviation = round(np.std(data), 2)
        assymetry = round(sum((i - meanValue) ** 3 for i in data) / len(data))
        assymetryCoef = round(assymetry / standardDeviation ** 3, 2)
        excess = round(sum((i - meanValue) ** 4 for i in data) / len(data), 2)
        kurtosis = round(excess / standardDeviation ** 4 - 3, 2)
        meanSquare = sum(i ** 2 for i in data) / len(data)
        meanSquareError = np.sqrt(meanSquare)
        
        result = f'Number of values: {len(data)}\n'
        result += f'Min value: {min}\n'
        result += f'Max value: {max}\n'
        result += f'Middle value: {meanValue}\n'
        result += f'Dispersion: {variance}\n'
        result += f'Standard deviation: {standardDeviation}\n'
        result += f'Asymmetry: {assymetry}\n'
        result += f'Asymmetry coefficient: {assymetryCoef}\n'
        result += f'Excess: {excess}\n'
        result += f'Kurtosis: {kurtosis}\n'
        result += f'Medium square: {meanSquare}\n'
        result += f'RMS error: {meanSquareError}'
        
        return result

    def stationarity(self, data, M=10):
        '''
        Возвращает стационарность данных
        '''
        sub_arrays = np.split(data, M)

        means = []
        std_deviations = []
        
        for arr in sub_arrays:
            means.append(np.mean(arr))
            std_deviations.append(np.sqrt(np.var(arr)))
        
        for i in range(M-1):
                if (abs((means[i] - means[i+1]) / means[i+1]) > 0.1 or 
                    abs((std_deviations[i] - std_deviations[i+1]) / std_deviations[i+1] > 0.1)):
                    #print (f'\ti = {i}\n\tmeans[i] = {means[i]}\n\tmeans[i+1] = {means[i+1]}\n\tabs((means[i] - means[i+1]) / means[i+1]) = {abs((means[i] - means[i+1]) / means[i+1])}')
                    #print (f'\ti = {i}\n\tstd_deviations[i] = {std_deviations[i]}\n\tstd_deviations[i+1] = {std_deviations[i+1]}\n\tabs((std_deviations[i] - std_deviations[i+1]) / std_deviations[i+1]) = {abs((std_deviations[i] - std_deviations[i+1]) / std_deviations[i+1])}')
                    return 'The process is non-stationary'
        return 'Stationary process'
       
    def histograma(self, data, draw=False):
        '''
        Создает гистограмму для переданных данных
        '''
        try:
            M = int(self.parametrs.GetParametr("Parametrs", "M"))
            
            sortData = sorted(data)
            coutData = len(data)
            
            step = int(coutData/M)
            currentIndex = 0
            
            lstep = []
            for i in range(currentIndex, coutData, step):
                lstep.append([sortData[i], sortData[i+step-1]])
            
            
            dataForBarX = []
            dataForBarY = []
            for i in lstep:
                c = 0
                for j in data:
                    if j >= i[0] and j < i[1]:
                        c += 1
                dataForBarY.append(c) 
                dataForBarX.append(f'{i}')
            if draw:        
                plt.figure(figsize=(10, 10))
                plt.grid(True)
                plt.bar(dataForBarX, dataForBarY)
                plt.plot(dataForBarX, dataForBarY, color="red")
                plt.show()
            
            return [dataForBarX, dataForBarY]
        except:
            print("Текущие данные - пусты")

    def acf(self, data):
        '''
        График корреляции переданных данных
        '''
        L = [i for i in range(0, len(data)-1)]
        middleValue = round(np.mean(data), 2)
        Rxx = []
        Rl = []
        
        for i in L:
            Rx = 0
            for j in range(len(data) - i - 1):
                Rx += (data[j] - middleValue) * (data[j + i] - middleValue)
            Rxx.append(Rx / len(data))   
        
        Rxx = np.array(Rxx)
        
        for i in Rxx:
            Rl.append(i/np.max(Rxx))
        
        Rl = np.array(Rl)
        
        plt.figure(figsize=(10, 10))
        plt.grid(True)
        plt.title("График автокорялляции")
        plt.plot([i for i in range(len(Rl))], Rl)
        
        plt.show()

    def ccf(self, *args):
        '''
        Взаимокорреляция переданных данных
        '''
        L = [i for i in range(0, len(args[0])-1)]
        
        middleValue = []
        for i in args:
            middleValue.append(round(np.mean(i), 2))
        
        Rxx = []
        for i in L:
            Rx = 0
            for j in range(len(args[0]) - i - 1):
                Rx += (args[0][j] - middleValue[0]) * (args[1][j + i] - middleValue[1])
            Rxx.append(Rx / len(args[0]))   
        
        Rxx = np.array(Rxx)
        
        plt.figure(figsize=(10, 10))
        plt.grid(True)
        plt.title("График взаимокорреляции")
        plt.plot([i for i in range(len(Rxx))], Rxx)
        
        plt.show()


    def fourier(self, data, N, L=0):
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
    
    def spectrFourier(self, data, draw=False):
        N=len(data)
        L=[
            int(self.parametrs.GetParametr("Parametrs", "L1")),
            int(self.parametrs.GetParametr("Parametrs", "L2")),
            int(self.parametrs.GetParametr("Parametrs", "L3"))
        ]
        
        FN = int(N/2)
        deltaf = FN / (N/2)
        
        dataX = []
        for n in range(FN):
            dataX.append(n * deltaf)
        dataX = np.asarray(dataX)
        
        dataY = self.fourier(data, N, L=0)
        
        if draw:
            plt.figure(figsize=(10, 10))
            plt.subplot(4,1,1)
            plt.grid(True)
            plt.plot(dataX, dataY[0:FN])
            plt.title("Амплитудный спектр Фурье")
            
            for i in range(len(L)):
                window = self.fourier(data, N, L=L[i])
                window = np.asarray(window)
                plt.subplot(4,1,i+2)
                plt.grid(True)
                plt.plot(dataX, window[0:FN])
                plt.title(f"L={L[i]}")
            
            plt.show()
        
        return dataY
    
    def spectrFourierForAudio(self, data, rate, draw=False):
        N=len(data)
        
        
        dt = 1 / rate
        
        FN = 1 / (2 * dt)
        deltaf = round(2 * FN / N, 2)
        
        dataX = []
        for n in range(int(N/2)):
            dataX.append(n * deltaf)
        dataX = np.asarray(dataX)
        
        dataY = self.fourier(data, N, L=0)
        
        if draw:
            plt.figure(figsize=(10, 10))
            plt.grid(True)
            plt.plot(dataX[0:500], dataY[0:500])
            plt.title("Амплитудный спектр Фурье")
            
            plt.show()
        