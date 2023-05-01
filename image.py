import os
import random
import re
from struct import pack, unpack
import PIL.Image as PilImage
import numpy as np
from tkinter import filedialog as fd 
from matplotlib import pyplot as plt
from scipy.fft import fft, ifft, fft2, ifft2, rfft, irfft, rfftfreq
from scipy import signal

class Image:
    def __init__(self, path=None, height=1024, weight=1024) -> None:
        self.dataImageList = []
        if path != None:
            self.dataImageList.append(self.__read_image(path, height, weight))
        else:
            self.dataImageList.append(self.__generate_default_iamge())
            
    
    def add_updated_data_to_list(self, dataImage):
        """
            Добавляет новое изображение в список
            
        Args:
            dataImage (np.array): массив numpy формата [[0 0 0 0 ... 0 0 0]]
        """
        self.dataImageList.append(dataImage)
    
    
    def add_new_image(self, path, height=1024, weight=1024):
        """
            Добавляет новое изображение к текущим

        Args:
            path (string): путь до файла
            height (int, optional): высота изображения для данных формата bin, xmr. По умолчанию 1024.
            weight (int, optional): ширина изображения для данных формата bin, xmr. По умолчанию 1024.
        """
        self.dataImageList.append(self.__read_image(path, height, weight))
    
    
    def get_last_data(self):
        """
            Возвращает последние данные из списка
            
        Returns:
            np.array: массив numpy формата [[0 0 0 0 ... 0 0 0]]
        """
        return self.dataImageList[len(self.dataImageList) - 1]
    
    
    def get_last_index(self):
        """
            Возвращает последний индекс списка изображений

        Returns:
            int: последний индекс списка изображений
        """
        return len(self.dataImageList) - 1
    
    
    def save_image(self, index=-1):
        """
            Функция для сохранения изображения из списка по индексу.
            Поддерживаются следующие расширения: jpg, png
            
        Args:
            index (int, optional): индекс массива для отображение. По умолчанию -1.
        """
        if index == -1:
            index = self.get_last_index()
            
        try:
            path = fd.asksaveasfilename(confirmoverwrite=True, 
                                        defaultextension="jpg", 
                                        initialfile="image.jpg", 
                                        filetypes = (('JPG', '.jpg'), ('PNG', '.png'), ('BIN', '.bin')))
            
            fileExtension = re.search(r'\w+$', path)[0]
            
            if fileExtension in ['jpg', 'png']:
                fileData = PilImage.fromarray(self.dataImageList[index].astype('uint8'))
                fileData.save(path)
            elif fileExtension in ['bin']:
                weight = self.dataImageList[index].shape[0]
                height = self.dataImageList[index].shape[1]
                
                print(height, weight)
                with open(path, 'wb') as f:                    
                    for h in range(height):
                        for w in range(weight):
                            number = pack("<f", self.dataImageList[index][h][w])
                            f.write(number)
            
        except Exception:
            print(Exception)
    
    
    def show_image(self, index = -1):
        """
            Выводит изображение из списка по индексу

        Args:
            index (int, optional): индекс массива для отображение. По умолчанию -1.
        """
        if index == -1:
            index = self.get_last_index()
        
        height = self.dataImageList[index].shape[0]
        weight = self.dataImageList[index].shape[1]
        
        dataForShow =  np.empty((height, weight))
        for h in range(height):
            for w in range(weight):
                value = self.dataImageList[index][h][w]
                while value > 255:
                    value -= 255
                dataForShow[h][w] = value
        
        image = PilImage.fromarray(dataForShow)
        
        width = image.size[0]
        hight = image.size[1]
        
        fig = plt.figure(figsize=(6,6))
        fig.patch.set_facecolor('#e8e8e8')
        plt.title(f"Размеры изображения: {width}x{hight}")
        plt.imshow(image)
        plt.axis("off")
        plt.show()
    
    
    def show_all_images(self):
        """
            Выводит все изображения
        """
        plotCount = len(self.dataImageList)
        rowCount = int(plotCount // 3) + 1
        
        fig = plt.figure(figsize=(5, 5))
        fig.patch.set_facecolor('#e8e8e8')
        
        for p in range(plotCount):
            height = self.dataImageList[p].shape[0]
            weight = self.dataImageList[p].shape[1]
            
            dataForShow =  np.empty((height, weight))
            for h in range(height):
                for w in range(weight):
                    value = self.dataImageList[p][h][w]
                    while value > 255:
                        value -= 255
                    dataForShow[h][w] = value
            
            
            image = PilImage.fromarray(dataForShow)
            plt.subplot(rowCount, 3, p+1)
            plt.imshow(image)
            plt.title(f"Индекс: {p}")
            plt.axis("off")
            
        plt.show()    
    
    
    def __read_image(self, path, height=1024, weight=1024):
        """
            Получает путь до файла и проверяет расширение, 
            если расширение допустимого формата, то проводит 
            считывание и преобразование данных к стандартному формату
            
        Args:
            path (string): путь до файла

        Returns:
            np.array: массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        fileExtension = re.search(r'\w+$', path)[0]
        
        if fileExtension in ['jpg', 'png']:
            try:
                dataImage = np.array(PilImage.open(path)).astype('int32')
                
                return self.__transform_data_image_to_default(dataImage)
            except Exception:
                print(Exception)
        elif fileExtension in ['xcr']:
            try:
                size = os.path.getsize(path)
            
                dataImage = []
                
                with open(path, 'rb') as f:
                    f.read(2048)
                    bytes = f.read(size - 2048 - 8192)
                    
                    for i in range(0, len(bytes), 2):
                        number = bytes[i] * 256 + bytes[i+1]               
                        dataImage.append(number)
                
                
                dataImage = np.asarray(dataImage)
                
                # 1024 x 1024
                # 2500 x 2048
                dataImage = np.reshape(dataImage, (height, weight)) 
                
                return self.__transform_data_image_to_default(dataImage)
            except Exception:
                print(Exception)
        elif fileExtension in ['bin']:
            try:
                dataImage = []
                
                with open(path, 'rb') as f:
                    number = f.read(4)
                    
                    while number:
                        tempTuple = unpack("<f", number)
                        tempValue = tempTuple[0]
                        dataImage.append(int(tempValue))
                        number = f.read(4)
                
                dataImage = np.asarray(dataImage)
                dataImage = dataImage.reshape(height, weight)
                
                return self.__transform_data_image_to_default(dataImage)
            except Exception:
                print(Exception)
        else:
            print("NANI")
    
    
    def __transform_data_image_to_default(self, dataImage):
        """
            Трансформирует стандартный список, в numpy список формата [[0 0 0 0 ... 0 0 0]]

        Args:
            dataImage (list): список данных, формата [[[0 0 0]]] или [[ 0 0 0 0 ... 0 0 0]] 

        Returns:
            np.array: массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        transformDataImage = []
        
        for line in dataImage:
            pixelList = []
            for pixel in line:
                try:
                    firstPixel  = pixel[0]
                    secondPixel = pixel[1]
                    thirdPixel  = pixel[2]
                    
                    if firstPixel == secondPixel == thirdPixel:
                        # Серое RGB изображение
                        pixelList.append(firstPixel)
                    else:
                        # Цветное изображение
                        pixelList.append((firstPixel + secondPixel + thirdPixel) // 3)
                except:
                    # список уже в формате [[0 0 0 0 ... 0 0 0]]
                    return np.array(dataImage).astype('int32')
            
            transformDataImage.append(pixelList)
        
        return np.array(transformDataImage).astype('int32')
    
    
    def __generate_default_iamge(self):
        """
            Генерирует дефолтное изображение
        Returns:
            np.array: массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        sizeBlackSqard = 256
        sizeWhiteSqardWight = 20
        sizeWhiteSqardHeight = 30
        
        dataImage = np.empty((sizeBlackSqard, sizeBlackSqard))
        
        indexForWhiteSqardWightStart = sizeBlackSqard/2 - sizeWhiteSqardWight/2
        indexForWhiteSqardWightEnd = sizeBlackSqard/2 + sizeWhiteSqardWight/2
        
        indexForWhiteSqardHeightStart = sizeBlackSqard/2 - sizeWhiteSqardHeight/2
        indexForWhiteSqardHeightEnd = sizeBlackSqard/2 + sizeWhiteSqardHeight/2
        
        for h in range(sizeBlackSqard):
            for w in range(sizeBlackSqard):
                if (w >= indexForWhiteSqardWightStart and w <= indexForWhiteSqardWightEnd) and (h >= indexForWhiteSqardHeightStart and h <= indexForWhiteSqardHeightEnd):
                    dataImage[h, w] = 255
                else:
                    dataImage[h, w] = 0
                    
        return np.array(dataImage).astype('int32')
    

class TransformImageData:
    def data_to_gray_diapason(self, dataImage):
        """_summary_

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]],
            приведенный к серому диапазону
        """
        maxPixel = dataImage.max()
        minPixel = dataImage.min()
        
        height = dataImage.shape[0]
        weight = dataImage.shape[1]
        
        transformData = np.empty((height, weight))
        
        for h in range(height):
            for w in range(weight):
                transformData[h][w] = ((dataImage[h][w] - minPixel) / (maxPixel - minPixel)) * 255
        
        return np.array(transformData).astype('int32')
    
    
    def shift_data_image(self, dataImage, shiftValue):
        """
            Смещает переданные данные на заданный коэффицент

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            shiftValue (int): значение смещения

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]],
            смещенный на заданный коэффицент
        """
        height = dataImage.shape[0]
        weight = dataImage.shape[1]
        
        transformData = np.empty((height, weight))
        
        for h in range(height):
            for w in range(weight):
                transformData[h][w] = dataImage[h][w] + shiftValue
        
        return np.array(transformData).astype('int32')
    
    
    def multi_data_image(self, dataImage,  multiValue):
        """
            Умножает переданные данные на заданный коэффицент

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            multiValue (int): значение умножения

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]],
            умноженный на заданный коэффицент
        """
        height = dataImage.shape[0]
        weight = dataImage.shape[1]
        
        transformData = np.empty((height, weight))
        
        for h in range(height):
            for w in range(weight):
                transformData[h][w] = dataImage[h][w] * multiValue
        
        return np.array(transformData).astype('int32')
    
    
    def resize_image_nearest_neighbors(self, dataImage, multiplierValue):
        """
            Изменение размера изображения методом ближайщих соседий

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            multiplierValue (int): значение множителя изменения размера

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]],
            размер изменен методом ближайшего соседа
        """
        weight = dataImage.shape[1]
        height = dataImage.shape[0]
        
        newSizeWeight = int(weight * multiplierValue)
        newSizeHeight = int(height * multiplierValue)
        
        transformData = np.zeros((newSizeHeight, newSizeWeight))
        
        for h in range(newSizeHeight):
            for w in range(newSizeWeight):
                x = int(h * (height / newSizeHeight))
                y = int(w * (weight / newSizeWeight))
                try:
                    transformData[h][w] = dataImage[x][y]
                except Exception:
                    print(Exception)
        
        return np.array(transformData).astype('int32')  
    
    
    def resize_image_binary_method(self, dataImage, multiplierValue):
        """
            Изменение размера изображения методом билинейной интерполяции

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            multiplierValue (int): значение множителя изменения размера

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]],
            размер изменен методом билинейной интерполяции
        """
        weight = dataImage.shape[1]
        height = dataImage.shape[0]
        
        newSizeWeight = int(weight * multiplierValue)
        newSizeHeight = int(height * multiplierValue)
        
        transformData = np.zeros((newSizeHeight, newSizeWeight))
        
        value = 0
        
        sh = newSizeHeight / height
        sw = newSizeWeight / weight
        
        for h in range(newSizeHeight):
            for w in range(newSizeWeight):
                x= h / sh
                y= w / sw
                
                p=(h+0.0)/sh-x
                q=(w+0.0)/sw-y
                
                x=int(x)-1
                y=int(y)-1
                try:
                    if x+1<newSizeHeight and y+1<newSizeWeight:
                        value = int(dataImage[x][y]*(1-p)*(1-q)+
                                    dataImage[x][y+1]*q*(1-p)+
                                    dataImage[x+1][y]*(1-q)*p+
                                    dataImage[x+1][y+1]*p*q)
                
                    transformData[h][w] = value
                except Exception:
                    print(Exception)
        
        return np.array(transformData).astype('int32')  
    
    
    def rotate_image_left(self, dataImage):
        """
            Поворот изображения налево

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]],
        """
        weight = dataImage.shape[1]
        height = dataImage.shape[0]
        
        transformData = np.zeros((weight, height))
        
        for w in range(weight):
            for h in range(height):
                transformData[w][h] = dataImage[h][weight - w - 1]
        
        return np.array(transformData).astype('int32') 
    
    
    def rotate_image_right(self, dataImage):
        """
            Поворот изображения направо

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        weight = dataImage.shape[1]
        height = dataImage.shape[0]
        
        transformData = np.zeros((weight, height))
        
        for w in range(weight):
            for h in range(height):
                transformData[w][h] = dataImage[height - h - 1][w]
        
        return np.array(transformData).astype('int32')   
    
    
    def do_negative(self, dataImage):
        """
            Делает изображение негативным

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]],
            сделанное негативным
        """
        L = dataImage.max()
        
        height = dataImage.shape[0]
        weight = dataImage.shape[1]
        
        transformData = np.empty((height, weight))
        
        for h in range(height):
            for w in range(weight):
                transformData[h][w] = L - 1 - dataImage[h][w]
        
        return np.array(transformData).astype('int32')
    
    
    def do_black_and_white(self, dataImage, factor):
        """
            Делает изображение черно-белым

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]],
            сделанное черно-белым
        """
        height = dataImage.shape[0]
        weight = dataImage.shape[1]
        
        transformData = np.empty((height, weight))
        
        for h in range(height):
            for w in range(weight):
                pixelValue = dataImage[h][w]
                if (pixelValue * 3 > (((255 + factor) // 2) * 3)):
                    transformData[h][w] = 255
                else:
                    transformData[h][w] = 0
        
        return np.array(transformData).astype('int32')
    
    
    def do_gamma_transform(self, dataImage, C, y):
        """
            Применяет к изображению гамма-преобразование

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        height = dataImage.shape[0]
        weight = dataImage.shape[1]
        
        transformData = np.empty((height, weight))
        
        for h in range(height):
            for w in range(weight):
                transformData[h][w] = C * (dataImage[h][w] ** y)

        transformData = self.data_to_gray_diapason(transformData)
        
        return np.array(transformData).astype('int32')
    
    
    def do_logarithm_transform(self, dataImage, C):        
        """
            Применяет к изображению логарифмического-преобразование

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        height = dataImage.shape[0]
        weight = dataImage.shape[1]
        
        transformData = np.empty((height, weight))
        
        for h in range(height):
            for w in range(weight):
                transformData[h][w] = C * np.log(dataImage[h][w] + 1)
        
        transformData = self.data_to_gray_diapason(transformData)
        
        return np.array(transformData).astype('int32')
    
    
    def do_gradient_transform(self, dataImage):
        """
            Применяет к изображению градиционное-преобразование

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        height = dataImage.shape[0]
        weight = dataImage.shape[1]
        
        L = dataImage.max()
        
        countListNormolized = AnalysisImageData.normalaized_histogram(AnalysisImageData(), dataImage, mode=2)
        cdf = AnalysisImageData.calculate_CDF(AnalysisImageData(), countListNormolized, mode=2)
        
        transformData = np.empty((height, weight))
        for h in range(height):
            for w in range(weight):
                transformData[h][w] = cdf[int(dataImage[h][w])] * L
        
        transformData = self.data_to_gray_diapason(transformData)
        
        return np.array(transformData).astype('int32')
    
    
    def get_difference_between_images(self, imageToSubtract, imageCurrent):
        """
            Вычитает из текущего изображения заданное

        Args:
            imageToSubtract (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            imageCurrent (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        transformData = imageCurrent - imageToSubtract
        
        transformData = self.data_to_gray_diapason(transformData)
        
        return np.array(transformData).astype('int32')

    
    def do_solid_and_peaper(self, dataImage, countBadPixekOnRow):
        """
            Применяет к переданым данным зашумление типа "Соль и перец"

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            countBadPixekOnRow (int): кол-во битых пикселей на строку

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        height = dataImage.shape[0]
        width = dataImage.shape[1]
        
        transformData = np.copy(dataImage)
        
        for h in range(height):
            noisePixel = random.sample(list(np.arange(width)), countBadPixekOnRow)
            for i in range(countBadPixekOnRow):
                transformData[h, noisePixel[i]] = 0 if random.randint(0, 1) else 255
        
        return np.array(transformData).astype('int32')
    
    
    def do_random_noise(self, dataImage, noiseRange):
        """
            Применяет к переданым данным зашумление типа рандом

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            noiseRange (int): диапазон случайных значений

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        height = dataImage.shape[0]
        width = dataImage.shape[1]
        
        transformData = np.copy(dataImage)
        
        length = int(np.ceil(np.abs(width)))
        
        for h in range(height):
            dataY = np.array([int(random.uniform(-noiseRange, noiseRange)) for _ in range(0, length)])
            transformData[h] += dataY
            
        return np.array(transformData).astype('int32')

    
class AnalysisImageData:
    def classic_histogram(self, dataImage):
        """
            Выводит классическую гистограмму для данных изображения

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        height = dataImage.shape[0]
        weight = dataImage.shape[1]
        
        histogramData = []
        for h in range(height):
            for w in range(weight):
                histogramData.append(dataImage[h][w])
        
        histogramData.sort()
        
        index = 0
        histogramDataX = [None] * 257
        histogramDataY = [0] * 257
        for value in histogramData:
            if value not in histogramDataX:
                histogramDataX[index] = value
                histogramDataY[index] += 1
                index += 1
            else:
                histogramDataY[histogramDataX.index(value)] += 1
        
        plt.figure(figsize=(18, 5))
        plt.title("Классическая гистограмма")
        plt.scatter(histogramDataX, histogramDataY)
        plt.show()
    
    
    def classic_histogram_with_to_gray_diapason(self, imageData):
        """
            Выводит гистограмму с предварительным приведением в серый диапазон

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """      
        histogramData = TransformImageData.data_to_gray_diapason(TransformImageData(), imageData)
        plt.figure(figsize=(18, 5))
        plt.title("Гистограмма с приведением к серому")
        plt.hist(histogramData.ravel(), bins=256, rwidth=0.8, range=(0, 255))
        plt.show()
    
    
    def normalaized_histogram(self, dataImage, mode=1):
        """
            Выводит нормализованную гистограмму

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            mode (int, optional): режим работы. Если 1, то выводит график нормализации
            Если 2, то возвращает нормализованные данные по оси Y. По умолчанию 1.

        Returns:
            histogramDataY (np.array): массив numpy приведенный к формату [0 0 0 0 ... 0 0 0]
        """
        height = dataImage.shape[0]
        weight = dataImage.shape[1]
        
        size = height * weight
        
        histogramData = []
        for h in range(height):
            for w in range(weight):
                histogramData.append(dataImage[h][w])
        
        histogramData.sort()
        
        index = 0
        histogramDataX = [None] * 257
        histogramDataY = [0] * 257
        for value in histogramData:
            if value not in histogramDataX:
                histogramDataX[index] = value
                histogramDataY[index] += 1
                index += 1
            else:
                histogramDataY[histogramDataX.index(value)] += 1
        
        for i in range(len(histogramDataY)):
            histogramDataY[i] = histogramDataY[i] / size
        
        if mode == 1:
            plt.figure(figsize=(18, 5))
            plt.title("Нормализованная гистограмма")
            plt.scatter(histogramDataX, histogramDataY)
            plt.show()
        else: 
            return np.array(histogramDataY)
    
    
    def calculate_CDF(self, normolizedData, mode=1):
        """
            Рассчитывает CDF

        Args:
            normolizedData (list): массив формата [0 0 0 0 ... 0 0 0]
            mode (int, optional): режим работы. Если 1, то выводит график CDF
            Если 2, то возвращает список данных cdf. По умолчанию 1.

        Returns:
            cdf (np.array): массив numpy приведенный к формату [0 0 0 0 ... 0 0 0]
        """
        
        if type(normolizedData[0]) is np.ndarray:
            normolizedData = self.normalaized_histogram(normolizedData, 2)
            
        cdf = []
        cdf.append(normolizedData[0])
        for i in range(1, len(normolizedData)):
            cdf.append(cdf[int(i) - 1] + normolizedData[int(i)])
        
        if mode == 1:
            plt.figure(figsize=(18, 5))
            plt.title("CDF (Кумулятивная функция распределения)")
            plt.plot(cdf)
            plt.show()
        else: 
            return np.array(cdf)
    
    
    def calculate_derivatives(self, dataImage, step, mode=1):
        """
            Расчитывает производные строк изображения

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            step (int): шаг
            mode (int, optional): режим работы. Если 1, то выводит график производных
            Если 2, то возвращает список данные производных. По умолчанию 1.

        Returns:
            derivatives (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        height = dataImage.shape[0]
        weight = dataImage.shape[1]
        
        derivativesHeight = int(np.ceil(height / step))
        derivativesWidht = int(weight - 1)
        
        derivatives =  np.empty((derivativesHeight, derivativesWidht))
        
        for h in range(derivativesHeight):
            for w in range(derivativesWidht):
                derivatives[h][w] = dataImage[int(h * step)][w + 1] - dataImage[int(h * step)][w]
        
        if mode == 1:
            plt.figure(figsize=(18, 5))
            plt.title("Производные")
            plt.plot(derivatives)
            plt.show()
        else: 
            return np.array(derivatives)
    
    
    def calculate_auto_correlation(self, dataImage, step, mode=1):
        """
            Расчитывает автокорреляцию производных строк изображения

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            step (int): шаг для расчета производных
            mode (int, optional): режим работы. Если 1, то выводит график авокорреляции
            Если 2, то возвращает список данные производных. По умолчанию 1.

        Returns:
            correlations (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        derivatives = self.calculate_derivatives(dataImage, step, mode=2)
        
        height = derivatives.shape[0]
        weight = derivatives.shape[1]
        
        correlations = np.empty((height, weight))
        
        for h in range(height):
            meanValue = np.mean(derivatives[h])
            size = derivatives[h].size
            
            corr = np.empty(size)            
            for value in range(size):
                sumOne = 0
                sumTwo = 0
                for k in range(size - value):
                    sumOne += (derivatives[h][k] - meanValue) * (derivatives[h][k + value] - meanValue)
                for k in range(size):
                    sumTwo += (derivatives[h][k] - meanValue) * (derivatives[h][k] - meanValue)
                corr[value] = sumOne / sumTwo
            
            for w in range(weight):
                correlations[h][w] = corr[w]
        
        if mode == 1:
            plt.figure(figsize=(18, 5))
            plt.title("Автокорреляция")
            plt.plot(correlations)
            plt.show()
        else: 
            return np.array(correlations)
    
    
    def calculate_cross_correlation(self, dataImage, step, mode=1):
        """
            Расчитывает кросскорреляцию производных строк изображения

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            step (int): шаг для расчета производных
            mode (int, optional): режим работы. Если 1, то выводит график кросскорреляции
            Если 2, то возвращает список данные производных. По умолчанию 1.

        Returns:
            correlations (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        derivatives = self.calculate_derivatives(dataImage, step, mode=2)
        
        height = derivatives.shape[0] - 1
        weight = derivatives.shape[1]
        
        correlations = np.empty((height, weight))
        
        for h in range(height):
            meanValueOne = np.mean(derivatives[h])
            meanValueTwo = np.mean(derivatives[h + 1])
            
            size = derivatives[h].size
            
            corr = np.empty(size)
            for value in range(size):
                sum = 0
                for k in range(size - value):
                    sum += (derivatives[h][k] - meanValueOne) * (derivatives[h + 1][k + value] - meanValueTwo)
                corr[value] = sum / size
            
            for w in range(weight):
                correlations[h][w] = corr[w]
                
        if mode == 1:
            plt.figure(figsize=(18, 5))
            plt.title("Кросскорреляция")
            plt.plot(correlations)
            plt.show()
        else: 
            return np.array(correlations)
    
    
    def calculate_fourier_transform(self, dataImage, step):
        """
            Выводит информацию об амплитуде спектра Фурье для производных,
            автокорреляции, взаимокорреляции и исходных строк переданныех
            данных изображения

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            step (int): шаг для расчета производных
        """
        derivatives = self.calculate_derivatives(dataImage, step, mode=2)
        autoCorrelation = self.calculate_cross_correlation(dataImage, step, mode=2)
        crossCorrelation = self.calculate_cross_correlation(dataImage, step, mode=2)
        
        derivativesRowCount = derivatives.shape[0]
        autoCorrelationRowCount = autoCorrelation.shape[0]
        crossCorrelationRowCount = crossCorrelation.shape[0]
        dataImgeRowCountForVisual = int(dataImage.shape[0] // step)
        
        derivativesWeight = derivatives.shape[1]
        autoCorrelationWeight = autoCorrelation.shape[1]
        crossCorrelationWeight = crossCorrelation.shape[1]
        dataImageWeight = dataImage.shape[1]        
        
        
        plt.figure(figsize=(10,5))
        plt.suptitle("Амплитудный спектр для исходных строк изображения")
        for i in range(dataImgeRowCountForVisual):
            yf = rfft(dataImage[i * step]) / dataImageWeight
            xf = rfftfreq(dataImageWeight)
            
            plt.subplot(dataImgeRowCountForVisual, 3, i + 1)            
            plt.title(f"Индекс строки {i * step}")
            plt.plot(xf, np.abs(yf))
        
        plt.figure(figsize=(10,5))
        plt.suptitle("Амплитудный спектр для производных строк изображения")  
        for i in range(derivativesRowCount):
            yf = rfft(derivatives[i]) / derivativesWeight
            xf = rfftfreq(derivativesWeight)
            
            plt.subplot(derivativesRowCount, 3, i + 1)            
            plt.title(f"Индекс строки {i}")
            plt.plot(xf, np.abs(yf)) 
        
        plt.figure(figsize=(10,5))
        plt.suptitle("Амплитудный спектр для автокорреляций производных")  
        for i in range(autoCorrelationRowCount):
            yf = rfft(autoCorrelation[i]) / autoCorrelationWeight
            xf = rfftfreq(autoCorrelationWeight)
            
            plt.subplot(autoCorrelationRowCount, 3, i + 1)            
            plt.title(f"Индекс строки {i}")
            plt.plot(xf, np.abs(yf)) 
            
        plt.figure(figsize=(10,5))
        plt.suptitle("Амплитудный спектр для взаимокорреляции производных")  
        for i in range(crossCorrelationRowCount):
            yf = rfft(crossCorrelation[i]) / crossCorrelationWeight
            xf = rfftfreq(crossCorrelationWeight)
            
            plt.subplot(crossCorrelationRowCount, 3, i + 1)            
            plt.title(f"Индекс строки {i}")
            plt.plot(xf, np.abs(yf)) 
         
        plt.show()

    
    def calculate_2D_fourier_transform(self, dataImage):
        """
            Расчитывает 2Д-преобразование Фурье

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]  

        Returns:
            transformData: список формата [[0 0 0 0 ... 0 0 0]]
        """
        height = int(dataImage.shape[0])
        widght = int(dataImage.shape[1])
        
        transformData = np.fft.fft2(dataImage)
        
        # transformData = np.empty((height, widght))    
        
        # for h in range(height):            
        #     yf = rfft(dataImage[h])
            
        #     for w in range(int(widght/2)):
        #         transformData[h][w] = yf[w]
            
        #     # transformData[h] = yf
            
        # transformData = np.transpose(transformData)
        
        # for w in range(widght):            
        #     yf = rfft(transformData[w])
            
        #     for h in range(int(height/2)):
        #         transformData[w][h] = yf[h]
            
        #     # transformData[w] = yf
        
        # transformData = np.transpose(transformData) 
        
        for h in range(height):
            transformData[h] = np.roll(transformData[h], int(widght/2))
        
        transformData = np.transpose(transformData) 
        
        for w in range(widght):
            transformData[w] = np.roll(transformData[w], int(height/2))
        
        transformData = np.transpose(transformData) 
        
        return transformData
    
    
    def calculate_inverse_2D_fourier_transform(self, dataImage):
        """
            Расчитывает обратное 2Д-преобразование Фурье

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]  

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        height = dataImage.shape[0]  
        widght = dataImage.shape[1] 
        
        dataImageForInverse = np.copy(dataImage)        
        
        for h in range(height):
            dataImageForInverse[h] = np.roll(dataImageForInverse[h], -int(widght/2))
        
        dataImageForInverse = np.transpose(dataImageForInverse) 
        
        for w in range(widght):
            dataImageForInverse[w] = np.roll(dataImageForInverse[w], -int(height/2))
        
        dataImageForInverse = np.transpose(dataImageForInverse) 
        
        # transformData = np.empty((height, widght))
        
        # for h in range(height):
        #     yf = ifft(dataImageForInverse[h])
            
        #     # print(yf)
        #     # print(yf[0].real)
        #     # input()
            
        #     for w in range(widght):
        #         transformData[h][w] = yf[w].real
            
        #     # transformData[h] = yf
        
        # transformData = np.transpose(transformData)
        
        # for w in range(widght):            
        #     yf = np.abs(ifft(transformData[w]))
            
        #     for h in range(height):
        #         transformData[w][h] = yf[h].real
                
        #     # transformData[w] = yf
        
        # transformData = np.transpose(transformData) 
        
        transformData = ifft2(dataImageForInverse)
        
        return np.array(transformData).astype('int32')
    
    
    def __inverse_fourier_transform_test_function(self, dataImage):
        """
            Тестовая функция для демонстрации

        Args:
            dataImage (all): заглушка
        """
        N = 200  # количество значений в сигнале
        dt = 0.005  # шаг дискретизации

        A = 10  # тестовая амплитуда гармонического процесса
        f = 4   # тестовая частота гармонического процесса
        
        sinDataX = np.arange(0, N * dt, dt)
        sinDataY = A * np.sin(2 * np.pi * f * sinDataX)
        
        plt.figure(figsize=(10,5))
        
        plt.subplot(1, 3, 1)            
        plt.title(f"Начальный сигнал")
        plt.plot(sinDataX, sinDataY)
        plt.grid(True)
        
        yf = rfft(sinDataY) / N

        plt.subplot(1, 3, 2)            
        plt.title(f"Амплитудный спектр")
        plt.plot(np.abs(yf))
        plt.grid(True)
        
        inverseDataY = irfft(yf) * N
        inverseDataX = np.arange(0, N * dt, dt)
        
        plt.subplot(1, 3, 3)            
        plt.title(f"Обратное преобразование Фурье")
        plt.plot(inverseDataX, inverseDataY)
        plt.grid(True)
        
        plt.show()
    

class FilterImageData:
    def lpf(self, dataImage, freq, m, mode=1):
        """
        Фильтр низких чатсот

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            freq (float): частота
            m (int): размер окна
            mode (int, optional): режим работы. Если 1, то возвращает отфильтрованые данные
            Если 2, то возвращает значение фильтра. По умолчанию 1.
        """
        width = dataImage.shape[1]
        height = dataImage.shape[0]
        
        d = [0.35577019, 0.2436983, 0.07211497, 0.00630165]
        
        fact = float(2 * freq)
        
        # dt = 1 / width
        # fact = float(2 * freq) * dt
        
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
            
        lpwReverse = []
        for i in range(len(lpw) - 1, 0, -1):
            lpwReverse.append(lpw[i])

        lpwResult = np.array(lpwReverse + lpw)
        
        if mode == 1:
            transformData = np.empty((height, width))
            
            for h in range(height): 
                convolveData = signal.convolve(dataImage[h], lpwResult)
                
                for w in range(width):
                    if w < width - m:
                        transformData[h][w] = convolveData[w + m]
                    else:
                        transformData[h][w] = dataImage[h][w] 
                                    
            return np.array(transformData).astype('int32')
        else:
            return lpwResult
    
    
    def hpf(self, dataImage, freq, m, mode=1):
        """
        Фильтр высоких чатсот

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            freq (float): частота
            m (int): размер окна
            mode (int, optional): режим работы. Если 1, то возвращает отфильтрованые данные
            Если 2, то возвращает значение фильтра. По умолчанию 1.
        """
        width = dataImage.shape[1]
        height = dataImage.shape[0]
        
        lpf = self.lpf(dataImage, freq, m, mode=2)
        
        loper = 2 * m + 1
        hpw = [0 for _ in range(0, loper)]
        for k in range(0, loper):
            if k == m:
                hpw[k] = 1 - lpf[k]
            else:
                hpw[k] = -1 * lpf[k]
        
        if mode == 1:
            transformData = np.empty((height, width))
            
            for h in range(height): 
                convolveData = signal.convolve(dataImage[h], hpw)
                
                for w in range(width):
                    if w < width - m:
                        transformData[h][w] = convolveData[w + m]
                    else:
                        transformData[h][w] = convolveData[w - width + m]
                                    
            return np.array(transformData).astype('int32')
        else:
            return hpw
    
    
    def bpf(self, dataImage, freqOne, freqTwo, m, mode=1):
        """
        Полосовой фильтр

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            freqOne (float): первая частота
            freqTwo (float): вторая частота
            m (int): размер окна
            mode (int, optional): режим работы. Если 1, то возвращает отфильтрованые данные
            Если 2, то возвращает значение фильтра. По умолчанию 1.
        """
        width = dataImage.shape[1]
        height = dataImage.shape[0]
        
        lpwOne = self.lpf(dataImage, freqOne, m, mode=2)
        lpwTwo = self.lpf(dataImage, freqTwo, m, mode=2)
        
        loper = 2 * m + 1
        bpw = [0 for _ in range(0, loper)]
        for k in range(0, loper):
            bpw[k] = lpwTwo[k] - lpwOne[k]
            
        if mode == 1:
            transformData = np.empty((height, width))
            
            for h in range(height): 
                convolveData = signal.convolve(dataImage[h], bpw)
                
                for w in range(width):
                    if w < width - m:
                        transformData[h][w] = convolveData[w + m]
                    else:
                        transformData[h][w] = convolveData[w - width + m]
                                    
            return np.array(transformData).astype('int32')
        else:
            return bpw    
    
    
    def bsw(self, dataImage, freqOne, freqTwo, m, mode=1):
        """
        Режекторный фильтр

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            freqOne (float): первая частота
            freqTwo (float): вторая частота
            m (int): размер окна
            mode (int, optional): режим работы. Если 1, то возвращает отфильтрованые данные
            Если 2, то возвращает значение фильтра. По умолчанию 1.
        """
        width = dataImage.shape[1]
        height = dataImage.shape[0]
        
        lpwOne = self.lpf(dataImage, freqOne, m, mode=2)
        lpwTwo = self.lpf(dataImage, freqTwo, m, mode=2)
        
        loper = 2 * m + 1
        bsw = [0 for _ in range(0, loper)]
        for k in range(0, loper):
            if k == m:
                bsw[k] = 1 + lpwOne[k] - lpwTwo[k]
            else:
                bsw[k] = lpwOne[k] - lpwTwo[k]
                
        if mode == 1:
            transformData = np.empty((height, width))
            
            for h in range(height): 
                convolveData = signal.convolve(dataImage[h], bsw)
                
                for w in range(width):
                    if w < width - m:
                        transformData[h][w] = convolveData[w + m]
                    else:
                        transformData[h][w] = convolveData[w - width + m]
                                    
            return np.array(transformData).astype('int32')
        else:
            return bsw  
    
    
    def middle_filter(self, dataImage, maskSize=10):
        """
            Усредняющий арифметический фильтр

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            maskSize (int, optional): размер маски. По умолчанию 10.

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        maskList = [np.zeros((maskSize, maskSize), dtype=float) + 1]
        
        a = int((maskList[0].shape[0] - 1) / 2)
        b = int((maskList[0].shape[1] - 1) / 2)
        
        height = dataImage.shape[0]
        width = dataImage.shape[1]
        
        transformData = np.empty((height, width))
        
        for h in range(height):
            for w in range(width):
                sumOne = 0
                for i in range(len(maskList)):
                    sumTwo = 0
                    for s in range(-1 * a, a + 1):
                        sumTree = 0
                        for t in range(-1 * b, b + 1):
                            try:
                                sumTree += maskList[i][s + 1, t + 1] * dataImage[h + s, w + t]
                            except:
                                pass
                        sumTwo += sumTree
                    sumOne += np.abs(sumTwo)
                transformData[h, w] = sumOne
        
        transformData = transformData / (maskSize * maskSize)
        
        return np.array(transformData).astype('int32')
    
    
    def median_filter(self, dataImage, maskSize=10):
        """
            Медианный фильтр

        Args:
            dataImage (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
            maskSize (int, optional): размер маски. По умолчанию 10.

        Returns:
            transformData (np.array): массив numpy приведенный к формату [[0 0 0 0 ... 0 0 0]]
        """
        a = int((maskSize - 1) / 2)
        b = int((maskSize - 1) / 2)
        
        height = dataImage.shape[0]
        width = dataImage.shape[1]
        
        transformData = np.empty((height, width))
        
        for h in range(height):
            for w in range(width):
                l = []
                for s in range(-1 * a, a + 1):
                    for t in range(-1 * b, b + 1):
                        try:
                            l.append(dataImage[h + s, w + t])
                        except:
                            pass
                transformData[h, w] = np.median(l)
        
        return np.array(transformData).astype('int32')
    
    