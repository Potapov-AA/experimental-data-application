import numpy as np
import wave
from struct import *


class InOut():
    def __init__(self): pass
    
    def readBinaryFile(self, path):
        data = []
        with open(path, 'rb') as f:
            number = f.read(4)
            print(number)
            
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
            
            str_data  = f.readframes(nframes)
            data = np.fromstring(str_data,dtype = np.short)
        
        data.shape = -1,2
        data = data.T
        
        result["data"] = data
        
        return result
            
    def statisticSave(self, name, statistic):
        with open(name, 'w') as f:
            f.write(statistic)    