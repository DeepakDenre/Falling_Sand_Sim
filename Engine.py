import pygame as pg
from grid import Grid
from Ini import *

class Engine:
    def __init__(self, width, height, title):
        self.gridCurrent = Grid(col,row).getGrid()
        self.gridNext = Grid(col,row).getGrid()
        self.gridEmpty = Grid(col,row).getGrid()
        
        self.gridCurrent[20][2].setStatus(True)
        
        pg.init()
        self.GameOn = True
        self.width = width
        self.height = height
        self.title = title
        self.screen = pg.display.set_mode((width,height))
        pg.display.set_caption(title)

    def __Event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.__Quit()
                self.GameOn = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.__Quit()
                    self.GameOn=False
                elif event.key == pg.K_w:
                    print("pressed W")
                    
    def GameLoop(self):
        while self.GameOn:
            self.__Update()
            self.__Draw()
            self.__Event()
                    
    def __Update(self):
        for i in range(row):
            for j in range(col):
                stat = self.gridCurrent[i][j].getStatus()
                statBelow = self.gridCurrent[i][j+1].getStatus()
                if stat:
                    if statBelow == False:
                        self.gridNext[i][j+1].setColor(self.gridNext[i][j].getColor())
                        self.gridNext[i][j+1].setStatus(True)
                        self.gridNext[i][j].setStatus(False)
                        self.gridNext[i][j].setColor((0,0,0))
        self.gridCurrent = self.gridNext
        self.gridNext = self.gridEmpty
               
    
    def __Draw(self):
        for i in range(row):
            for j in range(col):
                if self.gridCurrent[i][j].getStatus():
                    pg.draw.rect(self.screen,self.gridCurrent[i][j].getColor(),(i*cellSize, j*cellSize, cellSize, cellSize))
        pg.display.flip()
        
    def __Quit(self):
        pg.quit()