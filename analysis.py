import numpy as np

class Analysis:
    def __init__(self):
        pass

    def statistics(self, data):
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
        
