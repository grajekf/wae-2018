from abc import ABC


class Parametrisible(ABC):
    def getparameters(self):
        pass
    
    def setparameter(self, key, value):
        pass