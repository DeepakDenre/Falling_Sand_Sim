from cell import Cell
import random as ran
class Grid:
    def __init__(self, col, row):
        self.__grid = [[Cell((ran.randrange(0,256),ran.randrange(0,256),ran.randrange(0,256))) for _ in range(col+1)] for _ in range(row+1)]
        
    def getGrid(self):
        return self.__grid