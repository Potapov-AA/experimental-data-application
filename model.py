
from random import randint
from accessify import private
from matplotlib import pyplot as plt
import numpy as np
import math
import time


class Model:
    def __init__(self):
        self.e = np.e

    def drawLinerTrend(self,  a=1, b=1, N=1000, N1=0, N2=999, type=0):
        '''
        Выводит график линейных трендов
        Если type = 0, выводит массив данные по Y восходящего тренда
        Если type = 1, выводит массив данные по Y низходящего тренда
        Если type = 2, выводит массив массивов данных по Y восходящего тренда и низходящего тренда
        '''
        if type == 0:
            dataX = [i for i in range(N)]
            dataY = self.__calculateYlinear(a, b, N)
            plt.plot(dataX[N1:N2], dataY[N1:N2])
            plt.title("Линейный восходящий тренд")
            plt.show()
        elif type == 1:
            dataX = [i for i in range(N)]
            dataY = -self.__calculateYlinear(a, b, N)
            plt.plot(dataX[N1:N2], dataY[N1:N2])
            plt.title("Линейный низходящий тренд")
            plt.show()
        else:
            plt.subplot(1, 2, 1)
            dataX1 = [i for i in range(N)]
            dataY1 = self.__calculateYlinear(a, b, N)
            plt.plot(dataX1[N1:N2], dataY1[N1:N2])
            plt.title("Линейный восходящий тренд")

            plt.subplot(1, 2, 2)
            dataX2 = [i for i in range(N)]
            dataY2 = -self.__calculateYlinear(a, b, N)
            plt.plot(dataX2[N1:N2], dataY2[N1:N2])
            plt.title("Линейный низходящий тренд")

            plt.show()

    def getLinerTrend(self, a=1, b=1, N=1000, type=1):
        '''
        Получить массив данных линейных трендов
        Если type = 0, возвращает массив данные по Y восходящего тренда
        Если type = 1, возвращает массив данные по Y низходящего тренда
        Если type = 2, возвращает массив массивов данных по Y восходящего тренда и низходящего тренда
        '''
        if type == 0:
            return self.__calculateYlinear(a, b, N)
        elif type == 1:
            return -self.__calculateYlinear(a, b, N)
        else:
            return [self.__calculateYlinear(a, b, N), -self.__calculateYlinear(a, b, N)]

    def drawExponentaTrend(self, alpha=0.01, beta=1, N=1000, N1=0, N2=999, type=0):
        '''
        Выводит график экспонентных трендов
        Если type = 0, выводит массив данные по Y восходящего тренда
        Если type = 1, выводит массив данные по Y низходящего тренда
        Если type = 2, выводит массив массивов данных по Y восходящего тренда и низходящего тренда
        '''
        if type == 0:
            dataX = [i for i in range(N)]
            dataY = self.__calculateYexponenta(alpha, beta, N)[1]
            plt.plot(dataX[N1:N2], dataY[N1:N2])
            plt.title("Экспонентный восходящий тренд")
            plt.show()
        elif type == 1:
            dataX = [i for i in range(N)]
            dataY = self.__calculateYexponenta(alpha, beta, N)[0]
            plt.plot(dataX[N1:N2], dataY[N1:N2])
            plt.title("Экспонентный низходящий тренд")
            plt.show()
        else:
            plt.subplot(1, 2, 1)
            dataX1 = [i for i in range(N)]
            dataY1 = self.__calculateYexponenta(alpha, beta, N)[1]
            plt.plot(dataX1[N1:N2], dataY1[N1:N2])
            plt.title("Экспонентный восходящий тренд")

            plt.subplot(1, 2, 2)
            dataX2 = [i for i in range(N)]
            dataY2 = self.__calculateYexponenta(alpha, beta, N)[0]
            plt.plot(dataX2[N1:N2], dataY2[N1:N2])
            plt.title("Экспонентный низходящий тренд")

            plt.show()

    def getExponentaTrend(self, alpha=0.01, beta=1, N=1000, type=0):
        '''
        Получить массив данных экспонентных трендов
        Если type = 0, возвращает массив данные по Y восходящего тренда
        Если type = 1, возвращает массив данные по Y низходящего тренда
        Если type = 2, возвращает массив массивов данных по Y восходящего тренда и низходящего тренда
        '''
        if type == 0:
            return self.__calculateYexponenta(alpha, beta, N)[1]
        elif type == 1:
            return self.__calculateYexponenta(alpha, beta, N)[0]
        else:
            return self.__calculateYexponenta(alpha, beta, N)

    def drawTrend(self, a=1, b=1, alpha=0.01, beta=1, N=1000):
        '''
        Выводит график всех трендов
        '''
        dataX = [i for i in range(N)]

        plt.subplot(2, 2, 1)
        dataY1 = self.__calculateYexponenta(alpha, beta, N)[1]
        plt.plot(dataX, dataY1)
        plt.title("Экспонентный восходящий тренд")

        plt.subplot(2, 2, 2)
        dataY2 = self.__calculateYexponenta(alpha, beta, N)[0]
        plt.plot(dataX, dataY2)
        plt.title("Экспонентный низходящий тренд")

        plt.subplot(2, 2, 3)
        dataY3 = self.__calculateYlinear(a, b, N)
        plt.plot(dataX, dataY3)
        plt.title("Линейный восходящий тренд")

        plt.subplot(2, 2, 4)
        dataY4 = -self.__calculateYlinear(a, b, N)
        plt.plot(dataX, dataY4)
        plt.title("Линейный низходящий тренд")

        plt.show()

    def drawRandomNoise(self, Range=1000, N=1000):
        '''
        Выводит график шума основанного на встроенном ПСЧ
        '''
        dataX = [i for i in range(N)]
        dataY = self.__calculateRandomNoise(Range, N)

        plt.plot(dataX, dataY)
        plt.title("Шум на основе встроенного ПСЧ")

        plt.show()

    def drawMyRandomNoise(self, Range=1000, N=1000):
        '''
         Выводит график шума основанного на линейном конгруэнтном ПСЧ
        '''
        dataX = [i for i in range(N)]
        dataY = self.__calculateMyRandomNoise(time.time(), Range, N)

        plt.plot(dataX, dataY)
        plt.title("Шум на основе встроенного линейного конгруэнтного ПСЧ")

        plt.show()

    def drawNoise(self, Range=1000, N=1000):
        '''
        Выводит график шума
        '''
        dataX = [i for i in range(N)]
        dataY1 = self.__calculateRandomNoise(Range, N)
        dataY2 = self.__calculateMyRandomNoise(time.time(), Range, N)

        plt.subplot(1, 2, 1)
        plt.plot(dataX, dataY1)
        plt.title("Шум на основе встроенного ПСЧ")

        plt.subplot(1, 2, 2)
        plt.plot(dataX, dataY2)
        plt.title("Шум на основе встроенного линейного конгруэнтного ПСЧ")

        plt.show()

    def getNoise(self, Range=1000, N=1000, type=0):
        '''
        Получить массив данных экспонентных трендов
        Если type = 0, возвращает массив данные по Y встроенного рандомайзера
        Если type = 1, возвращает массив данные по Y написанного рандомайзера
        Если type = 2, возвращает массив массивов данных по Y встроенного рандомайзера и написанного рандомайзера
        '''
        if type == 0:
            return self.__calculateRandomNoise(Range, N)
        elif type == 1:
            return self.__calculateMyRandomNoise(time.time(), Range, N)
        else:
            return [self.__calculateRandomNoise(Range, N), self.__calculateMyRandomNoise(time.time(), Range, N)]

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

        if N2 != len(data) - 1:
            shiftData += [i for i in data[N2:]]

        plt.subplot(1, 2, 1)
        plt.plot([i for i in range(len(data))], data)
        plt.title("Начальные данные")

        plt.subplot(1, 2, 2)
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

    def drawHarm(self, N = 1000, A0 = 10, f0 = 10, dt = 0.01, thetta = 0):
        '''
        Выводит график гармонического процесса
        '''
        dataX = [i * dt for i in range(N)]
        dataY = [A0 * math.sin(2 * math.pi * f0 * dt * k + thetta) for k in range(N)]

        plt.plot(dataX, dataY)
        plt.title("Гармонического процесс")
        plt.show()

    
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

        plt.plot([i * dt for i in range(N)], harm)
        plt.title("harm")
        plt.show()
    
    def getHarm(self, N = 1000, A0 = 10, f0 = 10, dt = 0.01, thetta = 0):
        '''
        Возвращает данные гармонического процесса
        '''
        dataY = [A0 * math.sin(2 * math.pi * f0 * dt * k + thetta) for k in range(N)]

        return dataY
    
    @private
    def __calculateYlinear(self, a, b, N):
        '''
        Расчитывает значения по оси Y для линейного графика
        '''
        return np.asarray([i*a+b for i in range(N)], dtype=float)

    @private
    def __calculateYexponenta(self, alpha, beta, N):
        '''
        Расчитывает значения по оси Y для экспоненты
        '''
        yExponenta = []
        yExponenta_1 = [beta * self.e **
                        (-alpha * i) for i in range(N)]
        yExponenta_2 = [beta * self.e **
                        (alpha * i) for i in range(N)]
        yExponenta.append(yExponenta_1)
        yExponenta.append(yExponenta_2)
        return np.asarray(yExponenta)

    @private
    def __calculateRandomNoise(self, Range, N):
        '''
        Расчитывает значения по оси Y встроенным рандомом
        '''
        return np.asarray(np.random.randint(-Range, Range, N))

    @private
    def __calculateMyRandomNoise(self, seed, Range, N):
        '''
        Расчитывает значения по оси Y по функции с помощью линейного конгруэнтный генератора псевдослучайных чисел
        '''
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

        return np.asarray(dataY)

