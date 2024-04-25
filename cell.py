class Cell:
    def __init__(self,color = (0,0,0),alive=False,cellType = "null"):
        self.__color : tuple = color
        self.__alive : bool = alive
        self.__cellType : str = cellType
        
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
        self.__cellType = cellType
        