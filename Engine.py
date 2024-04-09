import pygame as pg
from grid import Grid
import random as ran

class Engine:
    def __init__(self, width, height, title, CellSize,brushSize,colorPallet):
        self.__colorPallet = colorPallet
        self.__brushSize = brushSize
        self.__CellSize = CellSize
        self.__width = width
        self.__height = height
        self.__title = title
        self.__col = self.__width // self.__CellSize
        self.__row = self.__height // self.__CellSize
        self.__gridCurrent = Grid(self.__col,self.__row).getGrid()
        self.__gridNext = Grid(self.__col,self.__row).getGrid()
        self.__gridEmpty = Grid(self.__col,self.__row).getGrid()
        
        pg.init()
        self.__GameOn = True
        self.__screen = pg.display.set_mode((width,height))
        pg.display.set_caption(self.__title)

    def __Event(self):
        #for mouse input
        try:
            if pg.mouse.get_pressed()[0]:
                p_x, p_y = pg.mouse.get_pos()
                gpx,gpy = p_x//self.__CellSize, p_y//self.__CellSize
                for __i in range(-(self.__brushSize//2),(self.__brushSize//2)+1):
                    for __j in range(-(self.__brushSize//2),(self.__brushSize//2)+1):
                        if self.__gridCurrent[gpy+__i][gpx+__j].getStatus() == False:
                            self.__gridCurrent[gpy+__i][gpx+__j].setStatus(True)
                            self.__gridCurrent[gpy+__i][gpx+__j].setColor(self.__colorPallet["sand"][ran.randint(0,3)])
            elif pg.mouse.get_pressed()[2]:
                p_x, p_y = pg.mouse.get_pos()
                gpx,gpy = p_x//self.__CellSize, p_y//self.__CellSize
                for __i in range(-(self.__brushSize//2),(self.__brushSize//2)+1):
                    for __j in range(-(self.__brushSize//2),(self.__brushSize//2)+1):
                        if self.__gridCurrent[gpy+__i][gpx+__j].getStatus():
                            self.__gridCurrent[gpy+__i][gpx+__j].setStatus(False)
                            self.__gridCurrent[gpy+__i][gpx+__j].setColor((0,0,0))
        except Exception:
            pass
                            
        for __event in pg.event.get():
            if __event.type == pg.QUIT:
                self.__Quit()
                self.__GameOn = False
                
            # for Keybord input
            elif __event.type == pg.KEYDOWN:
                if __event.key == pg.K_ESCAPE:
                    self.__GameOn=False
                    
                elif __event.key == pg.K_SPACE:
                    print("Clearing screen")
                    for __i in range(self.__row):
                        for  __j in range(self.__col):
                            self.__gridCurrent[__i][__j].setStatus(False)
                            self.__gridCurrent[__i][__j].setColor((0,0,0))
                            self.__screen.fill((0,0,0))
                            
                    
    def GameLoop(self):
        while self.__GameOn:
            self.__screen.fill((0,0,0))
            self.__Event()
            self.__Update()
            self.__Draw()
            pg.display.flip()
        self.__Quit()
                    
    def __Update(self):
        for __i in range(self.__row):
            for __j in range(self.__col):
                stat = self.__gridCurrent[__i][__j].getStatus()
                statBelow = self.__gridCurrent[__i+1][__j].getStatus()
                if stat:
                    if statBelow == False:
                        self.__gridNext[__i+1][__j].setColor(self.__gridCurrent[__i][__j].getColor())
                        self.__gridNext[__i+1][__j].setStatus(True)
                        self.__gridCurrent[__i][__j].setStatus(False)
                        self.__gridCurrent[__i][__j].setColor((0,0,0))
                    else:
                        statBelowRight = self.__gridCurrent[__i+1][__j+1].getStatus()
                        statBelowLeft = self.__gridCurrent[__i+1][__j-1].getStatus()
                        if statBelowLeft == False and statBelowRight == False:
                            ranSide = ran.randrange(-1,1,2)
                            self.__gridNext[__i+1][__j+ranSide].setColor(self.__gridCurrent[__i][__j].getColor())
                            self.__gridNext[__i+1][__j+ranSide].setStatus(True)
                            self.__gridCurrent[__i][__j].setStatus(False)
                            self.__gridCurrent[__i][__j].setColor((0,0,0))
                        elif statBelowLeft == False and statBelowRight:
                            self.__gridNext[__i+1][__j-1].setColor(self.__gridCurrent[__i][__j].getColor())
                            self.__gridNext[__i+1][__j-1].setStatus(True)
                            self.__gridCurrent[__i][__j].setStatus(False)
                            self.__gridCurrent[__i][__j].setColor((0,0,0))
                        elif statBelowRight == False and statBelowLeft:
                            self.__gridNext[__i+1][__j+1].setColor(self.__gridCurrent[__i][__j].getColor())
                            self.__gridNext[__i+1][__j+1].setStatus(True)
                            self.__gridCurrent[__i][__j].setStatus(False)
                            self.__gridCurrent[__i][__j].setColor((0,0,0))
        self.__gridCurrent = self.__gridNext
        self.__gridNext = self.__gridEmpty
               
    
    def __Draw(self):
        for __i in range(self.__row):
            for __j in range(self.__col):
                if self.__gridCurrent[__i][__j].getStatus():
                    pg.draw.rect(self.__screen,self.__gridCurrent[__i][__j].getColor(),(__j*self.__CellSize, __i*self.__CellSize, self.__CellSize, self.__CellSize))
        
    def __Quit(self):
        pg.quit()