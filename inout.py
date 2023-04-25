import numpy as np
import wave
from struct import *

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
    