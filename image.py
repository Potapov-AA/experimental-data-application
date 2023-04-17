import re
import PIL.Image as PilImage
import numpy as np
from tkinter import filedialog as fd 

class Image:
    def __init__(self, path = None) -> None:
        self.dataImage = self.__read_image(path)
        
        self.dataImageList = []
        self.dataImageList.append(self.dataImage)
        
        ### ТЕСТОВАЯ, УБРАТЬ КОГДА ВСЕ ОТКРЫТИЯ ФАЙЛА СДЕЛАЮ
        print(self.dataImageList)
    
    
    def save_last_image(self):
        """
            Функция для сохранения последнего изображения.
            Поддерживаются следующие расширения: jpg, png
        """
        try:
            fileName = fd.asksaveasfilename(confirmoverwrite=True, 
                                            defaultextension="jpg", 
                                            initialfile="image.jpg", 
                                            filetypes = (('JPG', '.jpg'), ('PNG', '.png')))
            fileData = PilImage.fromarray(self.dataImage.astype('uint8'))
            fileData.save(fileName)
        except Exception:
            print(Exception)
    
    
    def save_image_at_index(self, index=0):
        pass
    
    
    def add_updated_data_to_list(self):
        pass
    
    
    def show_last_image(self):
        pass
    
    
    def show_image_at_index(self):
        pass
    
    
    def __read_image(self, path):
        fileExtension = re.search(r'\w+$', path)[0]
        
        if fileExtension in ['jpg']:
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
        transformDataImage = []
        
        for line in dataImage:
            pixelList = []
            for pixel in line:
                try:
                    firstPixel  = pixel[0]
                    secondPixel = pixel[1]
                    thirdPixel  = pixel[2]
                    
                    if firstPixel == secondPixel == thirdPixel:
                        pixelList.append(firstPixel)
                    else:
                        pixelList.append((firstPixel + secondPixel + thirdPixel) // 3)
                
                except:
                    return dataImage
            
            transformDataImage.append(pixelList)
        
        return np.array(transformDataImage).astype('int32')