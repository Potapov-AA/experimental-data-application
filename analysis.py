from turtle import color
import numpy as np
from scipy.stats import norm
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
        
        result = f'Количество значенией: {len(data)}\n'
        result += f'Минимальное значение: {min}\n'
        result += f'Максимальное значение: {max}\n'
        result += f'Среднее значение: {meanValue}\n'
        result += f'Дисперсия: {variance}\n'
        result += f'Стандартное отклонение: {standardDeviation}\n'
        result += f'Ассиметрия: {assymetry}\n'
        result += f'Коэффицент ассиметрии: {assymetryCoef}\n'
        result += f'Эксцесс: {excess}\n'
        result += f'куртозис: {kurtosis}\n'
        result += f'Средний квадрат: {meanSquare}\n'
        result += f'Ср. квад. ошибка: {meanSquareError}'
        
        return result

    def stationarity(self, data, M=10):
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
                    return 'Процесс нестационарный'
        return 'Процесс стационарный'
        
    def histograma(self, data=[i for i in range(10000)], M=100):
        

        min = int(round(np.min(data), 2))
        max = int(round(np.max(data), 2))
        
        step = int(round((max-min)/M))
        
        lstep = []
        for i in range(min, max, step):
            if i+step<=max:
                lstep.append([i, i+step])
        
        
        dataForBarX = []
        dataForBarY = []
        for i in lstep:
            c = 0
            for j in data:
                if j >= i[0] and j < i[1]:
                    c += 1
            dataForBarY.append(c) 
            dataForBarX.append(f'{i}')
                 
        plt.figure(figsize=(10, 10))
        plt.grid(True)
        plt.bar(dataForBarX, dataForBarY)
        plt.plot(dataForBarX, dataForBarY, color="red")
        plt.show()
    
    def acf(self, data=[i for i in range(1000)]):
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
        plt.title("График взаимной корреляции")
        plt.plot([i for i in range(len(Rxx))], Rxx)
        
        plt.show()
    
    def spectrFourier(self, data = [i for i in range(1000)], N = 1000, L=[24, 124, 224]):
        FN = int(N/2)
        deltaf = FN / (N/2)
        dataX = []
        for n in range(FN):
            dataX.append(n * deltaf)
        dataX = np.asarray(dataX)
        
        dataY = self.model.Fourier(data, N)
        
        plt.figure(figsize=(10, 10))
        plt.subplot(4,1,1)
        plt.grid(True)
        plt.plot(dataX, dataY[0:FN])
        plt.title("Амплитудный спектр Фурье")
        
        for i in range(len(L)):
            window = self.model.Fourier(data, N, L=L[i])
            window = np.asarray(window)
            plt.subplot(4,1,i+2)
            plt.grid(True)
            plt.plot(dataX, window[0:FN])
            plt.title(f"L={L[i]}")
        
        plt.show()
    
    def getSpectrFourier(self, data):
        N = len(data)
        
        
        FN = int(N/2)
        deltaf = FN / (N/2)
        dataX = []
        for n in range(FN):
            dataX.append(n * deltaf)
        dataX = np.asarray(dataX)
        
        dataY = self.model.Fourier(data, N)
        dataY = dataY[0:FN]
        dataY = np.asarray(dataY)
        
        return dataY
    
    def drawFileData(self, data):
        dataX = [i for i in range(len(data))]
        dataY = data
        
        plt.figure(figsize=(10, 10))
        plt.grid(True)
        
        plt.subplot(2,1,1)
        plt.title("Данные из файла")
        plt.plot(dataX, dataY)
        
        N = len(data)
        FN = int(N/2)
        deltaf = FN / (N/2)
        
        dataX = []
        for n in range(FN):
            dataX.append(n * deltaf)
        dataX = np.asarray(dataX)
        
        dataY = self.model.Fourier(data, N)
        
        plt.subplot(2,1,2)
        plt.plot(dataX, dataY[0:FN])
        plt.title("Амплитудный спектр Фурье")
        
        plt.show()
            
