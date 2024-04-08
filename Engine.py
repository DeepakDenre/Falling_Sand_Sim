import pygame as pg
from grid import Grid
from Ini import *
import random as ran

class Engine:
    def __init__(self, width, height, title):
        self.gridCurrent = Grid(col,row).getGrid()
        self.gridNext = Grid(col,row).getGrid()
        self.gridEmpty = Grid(col,row).getGrid()
        
        pg.init()
        self.GameOn = True
        self.width = width
        self.height = height
        self.title = title
        self.screen = pg.display.set_mode((width,height))
        pg.display.set_caption(title)

    def __Event(self):
        #for mouse input
        if pg.mouse.get_pressed()[0]:
            p_x, p_y = pg.mouse.get_pos()
            gpx,gpy = p_x//cellSize, p_y//cellSize
            
            for i in range(-(brushSize//2),(brushSize//2)+1):
                for j in range(-(brushSize//2),(brushSize//2)+1):
                    if self.gridCurrent[gpy+i][gpx+j].getStatus() == False:
                        self.gridCurrent[gpy+i][gpx+j].setStatus(True)
                        self.gridCurrent[gpy+i][gpx+j].setColor(colorPallet[ran.randint(0,3)])
            
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.__Quit()
                self.GameOn = False
                
            # for Keybord input
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.GameOn=False
                    
                elif event.key == pg.K_SPACE:
                    print("Clearing screen")
                    for i in range(row):
                        for  j in range(col):
                            self.gridCurrent[i][j].setStatus(False)
                            self.gridCurrent[i][j].setColor((0,0,0))
                            self.screen.fill((0,0,0))
                            
                    
    def GameLoop(self):
        while self.GameOn:
            self.screen.fill((0,0,0))
            self.__Event()
            self.__Update()
            self.__Draw()
            pg.display.flip()
        self.__Quit()
                    
    def __Update(self):
        for i in range(row):
            for j in range(col):
                stat = self.gridCurrent[i][j].getStatus()
                statBelow = self.gridCurrent[i+1][j].getStatus()
                if stat:
                    if statBelow == False:
                        self.gridNext[i+1][j].setColor(self.gridCurrent[i][j].getColor())
                        self.gridNext[i+1][j].setStatus(True)
                        self.gridCurrent[i][j].setStatus(False)
                        self.gridCurrent[i][j].setColor((0,0,0))
                    else:
                        statBelowRight = self.gridCurrent[i+1][j+1].getStatus()
                        statBelowLeft = self.gridCurrent[i+1][j-1].getStatus()
                        if statBelowLeft == False and statBelowRight == False:
                            ranSide = ran.randrange(-1,1,2)
                            self.gridNext[i+1][j+ranSide].setColor(self.gridCurrent[i][j].getColor())
                            self.gridNext[i+1][j+ranSide].setStatus(True)
                            self.gridCurrent[i][j].setStatus(False)
                            self.gridCurrent[i][j].setColor((0,0,0))
                        elif statBelowLeft == False and statBelowRight:
                            self.gridNext[i+1][j-1].setColor(self.gridCurrent[i][j].getColor())
                            self.gridNext[i+1][j-1].setStatus(True)
                            self.gridCurrent[i][j].setStatus(False)
                            self.gridCurrent[i][j].setColor((0,0,0))
                        elif statBelowRight == False and statBelowLeft:
                            self.gridNext[i+1][j+1].setColor(self.gridCurrent[i][j].getColor())
                            self.gridNext[i+1][j+1].setStatus(True)
                            self.gridCurrent[i][j].setStatus(False)
                            self.gridCurrent[i][j].setColor((0,0,0))
        self.gridCurrent = self.gridNext
        self.gridNext = self.gridEmpty
               
    
    def __Draw(self):
        for i in range(row):
            for j in range(col):
                if self.gridCurrent[i][j].getStatus():
                    pg.draw.rect(self.screen,self.gridCurrent[i][j].getColor(),(j*cellSize, i*cellSize, cellSize, cellSize))
        
    def __Quit(self):
        pg.quit()