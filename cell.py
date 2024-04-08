class Cell:
    def __init__(self,color = (0,0,0),alive=False):
        self.__color = color
        self.__alive = alive
        
    def getColor(self):
        return self.__color
    
    def setColor(self, colorNew):
        self.__color = colorNew
    
    def getStatus(self):
        return self.__alive
    
    def setStatus(self, status):
        self.__alive = status
        