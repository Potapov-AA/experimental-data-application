from turtle import color
import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt

class Analysis:
    def __init__(self):
        pass

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
        meanValue = round(np.mean(data), 2)
        standardDeviation = round(np.std(data), 2)
        
        normal =  norm.pdf(data, meanValue, standardDeviation)
        
        plt.plot(data, normal, color="red")
        plt.show()
        

        min = int(round(np.min(data), 2))
        max = int(round(np.max(data), 2))
        
        step = int(round((max-min)/M))
        
        lstep = []
        for i in range(min, max, step):
            if i+step<=max:
                lstep.append([i, i+step])
        
        normalForBar = []
        dataForBar = []
        for i in lstep:
            middle = 0
            c = 0
            for j in range(len(normal)):
                if j >= i[0] and j < i[1]:
                    middle += normal[j]
                    c += 1
            if middle != 0:
                normalForBar.append(middle/c) 
                dataForBar.append(f'{i}')
                 
        
        
        plt.bar(dataForBar, normalForBar)
        plt.plot(dataForBar, normalForBar, color="red")
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
        
        plt.title("График автокорялляции")
        plt.plot([i for i in range(len(Rl))], Rl, color="red")
        
        plt.show()
    
    def ccf(self, *args):
        pass