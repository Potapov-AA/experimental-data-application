import os
import re
from struct import pack, unpack
import PIL.Image as PilImage
import numpy as np
from tkinter import filedialog as fd 
from matplotlib import pyplot as plt

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
        
        image = PilImage.fromarray(self.dataImageList[index])
        
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
            image = PilImage.fromarray(self.dataImageList[p])
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
        sizeWhiteSqard = 100
        
        dataImage = np.empty((sizeBlackSqard, sizeBlackSqard))
        
        indexForWhiteSqardStart = sizeBlackSqard/2 - sizeWhiteSqard/2
        indexForWhiteSqardEnd = sizeBlackSqard/2 + sizeWhiteSqard/2
        
        for h in range(sizeBlackSqard):
            for w in range(sizeBlackSqard):
                if (w >= indexForWhiteSqardStart and w <= indexForWhiteSqardEnd) and (h >= indexForWhiteSqardStart and h <= indexForWhiteSqardEnd):
                    dataImage[h, w] = 0
                else:
                    dataImage[h, w] = 256
                    
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
            Делает изображение сепия

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