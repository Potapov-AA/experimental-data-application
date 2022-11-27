from model import Model
import numpy as np
from struct import *


class InOut():
    def __init__(self): pass
    
    def readFile(self, path):
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
    
    def saveFile(self, name, data):
        with open(name, 'wb') as f:
            for number in data:
                tempValue = pack("<f", number)
                f.write(tempValue) 