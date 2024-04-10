class Cell:
    def __init__(self,color = (0,0,0),alive=False,cellType = "sand"):
        self.__color = color
        self.__alive = alive
        self.__cellType = cellType
        
    def getColor(self):
        return self.__color
    
    def setColor(self, colorNew):
        self.__color = colorNew
    
    def getStatus(self):
        return self.__alive
    
    def setStatus(self, status):
        self.__alive = status
        
    def getCellType(self):
        return self.__cellType
    
    def setCellType(self, cellType):
        self.getCellType = cellType
        