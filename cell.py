class Cell:
    def __init__(self,color = (0,0,0),alive=False):
        self.color = color
        self.alive = alive
        
    def getColor(self):
        return self.color
    
    def setColor(self, colorNew):
        self.color = colorNew
    
    def getStatus(self):
        return self.alive
    
    def setStatus(self, status):
        self.alive = status
        