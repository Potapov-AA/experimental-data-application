import re
import PIL.Image as PilImage
import numpy as np
from tkinter import filedialog as fd 
from matplotlib import pyplot as plt

class Image:
    def __init__(self, path = None) -> None:
        self.dataImageList = []
        if path != None:
            self.dataImageList.append(self.__read_image(path))
        else:
            self.dataImageList.append(self.__generate_default_iamge())
            
    
    def add_updated_data_to_list(self, dataImage):
        """
            Добавляет новое изображение в список
            
        Args:
            dataImage (np.array): массив numpy формата [[0 0 0 0 ... 0 0 0]]
        """
        self.dataImageList.append(dataImage)
    
    
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
                                        filetypes = (('JPG', '.jpg'), ('PNG', '.png')))
            
            fileExtension = re.search(r'\w+$', path)[0]
            
            if fileExtension in ['jpg', 'png']:
                fileData = PilImage.fromarray(self.dataImageList[index].astype('uint8'))
                fileData.save(path)
            
        except Exception:
            print(Exception)
    
    
    def show_image(self, index = -1):
        """
            Отображает изображение из списка

        Args:
            index (int, optional): индекс массива для отображение. По умолчанию -1.
        """
        if index == -1:
            index = self.get_last_index()
        
        image = PilImage.fromarray(self.dataImageList[index])
        
        width = image.size[0]
        hight = image.size[1]
        
        plt.figure(figsize=(6,6))
        plt.title(f"Размеры изображения: {width}x{hight}")
        plt.imshow(image)
        plt.axis("off")
        plt.show()
    
    
    def __read_image(self, path):
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
        elif fileExtension in ['']:
            pass
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
    def do_negative(self, dataImage):
        L = dataImage.max()
        
        height = dataImage.shape[0]
        weight = dataImage.shape[1]
        
        transformData = np.empty((height, weight))
        
        for h in range(height):
            for w in range(weight):
                transformData[h][w] = L - 1 - dataImage[h][w]
        
        return np.array(transformData).astype('int32')