from cell import Cell
import random as ran
class Grid:
    def __init__(self, col, row):
        self.__grid = [[Cell() for _ in range(col+1)] for _ in range(row+1)]
        
    def getGrid(self):
        return self.__grid