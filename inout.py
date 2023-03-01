import os
import numpy as np
import wave
import imageio
import PIL.Image as pil
from struct import *
from PIL import Image

class InOut():
    def __init__(self): pass
    
    def readBinaryFile(self, path):
        data = []
        with open(path, 'rb') as f:
            number = f.read(4)
            
            while number:
                tempTuple = unpack("<f", number)
                tempValue = tempTuple[0]
                data.append(tempValue)
                number = f.read(4)
            
        data = np.asarray(data)
        return data
    
    def saveBinaryFile(self, name, data):
        with open(name, 'wb') as f:
            for number in data:
                tempValue = pack("<f", number)
                f.write(tempValue) 
    
    def readSoundFile(self, path):
        result = dict()
        data = object
        with wave.open(path, 'rb') as f:
            params = f.getparams()  
            nchannels, sampwidth, framerate, nframes, comptype, compname = params[:6]
            result["nchannels"] = nchannels
            result["framerate"] = framerate
            result["nframes"] = nframes
            result["compname"] = compname
            result["sampwidth"] = sampwidth
            
            str_data  = f.readframes(nframes)
            data = np.fromstring(str_data,dtype = np.short)
        
        if nchannels == 2:
            data.shape = -1,2
            data = data.T
        
        result["data"] = data
        
        return result
    
    def saveSoundFile(self, name, data):
        with wave.open(name, 'wb') as f:
            f.setnchannels(data["nchannels"])
            f.setsampwidth(data["sampwidth"])
            f.setframerate(data["framerate"])
            if data["nchannels"] == 1:                
                f.writeframes(data["data"])
            else:
                data1 = data["data"][0]
                data2 = data["data"][1]
                dataY = np.hstack([data1 , data2])
                f.writeframes(dataY)
         
    def statisticSave(self, name, statistic):
        with open(name, 'w') as f:
            f.write(statistic.encode('utf-16').decode('utf-16'))
    
    
    def readImages(self, path):
        try:
            img = Image.open(path)
            return img
        except Exception:
            print(Exception)
            
    def saveImage(self, name, image):
        try:
            image.save(name)
        except Exception:
            imageio.imwrite(name, image)
    
    def readXcrImage(self, path):
        size = os.path.getsize(path)
        data = []
        
        with open(path, 'rb') as f:
            f.read(2048)
            bytes = f.read(size - 2048 - 8192)
            
            for i in range(0, len(bytes), 2):
                
                number = bytes[i] * 256 + bytes[i+1]               
                data.append(number)
        
        
        data = np.asarray(data)
        data = np.reshape(data, (1024, 1024))
        
        
        
        new_image = pil.fromarray(data)
        
        
        return new_image
    
    def saveBinImages(self, name, image):
        data_image = np.array(image)
        with open(name, 'wb') as f:
            for i in data_image:
                for j in i:
                    for k in j:
                        number = pack("<f", k)
                        f.write(number)
    
    def readBinImage(self, path):
        data = []
        with open(path, 'rb') as f:
            number = f.read(4)
            
            while number:
                tempTuple = unpack("<f", number)
                tempValue = tempTuple[0]
                data.append(int(tempValue))
                number = f.read(4)
        
        data = np.asarray(data)
        data = data.reshape(360, 480, 3)
        print(data.shape)
            
        new_image = pil.fromarray((data).astype(np.uint8))
        
        return new_image