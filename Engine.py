import pygame as pg
from grid import Grid
import random as ran


class Engine:
    def __init__(self, width, height, title, cellsize, brushsize, colorpallet, backgroundcolor=(0, 0, 0)):
        self.__backgroundColor = backgroundcolor
        self.__type = list(colorpallet.keys())
        self.__typeCurrent = self.__type[0]
        self.__colorPallet = colorpallet
        self.__brushSize = brushsize
        self.__CellSize = cellsize
        self.__width = width
        self.__height = height
        self.__title = title
        self.__col = self.__width // self.__CellSize
        self.__row = self.__height // self.__CellSize
        self.__gridCurrent = Grid(self.__col, self.__row).getGrid()
        self.__gridNext = Grid(self.__col, self.__row).getGrid()
        self.__gridEmpty = Grid(self.__col, self.__row).getGrid()

        pg.init()
        pg.font.init()
        self.__font = pg.font.Font(None, 30)
        self.__GameOn = True
        self.__screen = pg.display.set_mode((width, height))
        self.__clock = pg.time.Clock()
        pg.display.set_caption(self.__title)

    def __event(self):
        # for closing the window
        for __event in pg.event.get():
            if __event.type == pg.QUIT:
                self.__GameOn = False

            elif __event.type == pg.MOUSEWHEEL:
                if __event.y == 1:
                    for __i in range(0, len(self.__type)):
                        if self.__type[__i] == self.__typeCurrent:
                            if self.__type[__i] != self.__type[-1]:
                                self.__typeCurrent = self.__type[__i + 1]
                                break
                elif __event.y == -1:
                    for __i in range(0, len(self.__type)):
                        if self.__type[__i] == self.__typeCurrent:
                            if self.__type[__i] != self.__type[0]:
                                self.__typeCurrent = self.__type[__i - 1]
                                break

            # for Keybord input
            elif __event.type == pg.KEYDOWN:
                # for closing the window
                if __event.key == pg.K_ESCAPE:
                    self.__GameOn = False

                if __event.key == pg.K_UP:
                    if self.__brushSize < 10:
                        self.__brushSize += 1
                elif __event.key == pg.K_DOWN:
                    if self.__brushSize > 1:
                        self.__brushSize -= 1

                # for changing the type of cell
                elif __event.key == pg.K_s:
                    for __i in range(0, len(self.__type)):
                        if self.__type[__i] == self.__typeCurrent:
                            if self.__type[__i] != self.__type[-1] and self.__type[__i] != "null":
                                self.__typeCurrent = self.__type[__i + 1]
                                break
                            else:
                                self.__typeCurrent = self.__type[0]
                                break

                # for clearing the screen
                elif __event.key == pg.K_SPACE:
                    print("Clearing screen")
                    for __i in range(self.__row - 1, 0, -1):
                        for __j in range(self.__col - 1, 0, -1):
                            self.__gridCurrent[__i][__j].setStatus(False)
                            self.__gridCurrent[__i][__j].setColor((0, 0, 0))
                            self.__screen.fill((0, 0, 0))

        # for mouse input
        try:
            # for drawing the cell
            if pg.mouse.get_pressed()[0]:
                p_x, p_y = pg.mouse.get_pos()
                gpx, gpy = p_x // self.__CellSize, p_y // self.__CellSize
                for __i in range(-(self.__brushSize // 2), (self.__brushSize // 2) + 1):
                    for __j in range(-(self.__brushSize // 2), (self.__brushSize // 2) + 1):
                        __gitter = ran.randrange(-1, 2, 2)
                        if self.__gridCurrent[gpy + __i][gpx + __j].getStatus() is False and __gitter == 1:
                            self.__gridCurrent[gpy + __i][gpx + __j].setStatus(True)
                            self.__gridCurrent[gpy + __i][gpx + __j].setColor(
                                self.__colorPallet[self.__typeCurrent][ran.randint(0, 3)])
                            self.__gridCurrent[gpy + __i][gpx + __j].setCellType(self.__typeCurrent)

            # for erasing the cell
            elif pg.mouse.get_pressed()[2]:
                p_x, p_y = pg.mouse.get_pos()
                gpx, gpy = p_x // self.__CellSize, p_y // self.__CellSize
                for __i in range(-(self.__brushSize // 2), (self.__brushSize // 2) + 1):
                    for __j in range(-(self.__brushSize // 2), (self.__brushSize // 2) + 1):
                        if self.__gridCurrent[gpy + __i][gpx + __j].getStatus():
                            __gitter = ran.randrange(-1, 2, 2)
                            if self.__gridCurrent[gpy + __i][gpx + __j].getStatus() is True and __gitter == 1:
                                self.__gridCurrent[gpy + __i][gpx + __j].setStatus(False)
                                self.__gridCurrent[gpy + __i][gpx + __j].setColor((0, 0, 0))
        except IndexError:
            pass

    def __update(self):
        # go through the grid and update the cell
        for __i in range(self.__row - 2, -1, -1):
            for __j in range(self.__col - 2, -1, -1):
                __state = self.__gridCurrent[__i][__j].getStatus()
                __cellType = self.__gridCurrent[__i][__j].getCellType()
                if __state:
                    if __cellType == "sand":
                        __statBelow = self.__gridCurrent[__i + 1][__j].getStatus()
                        if not __statBelow:
                            self.__gridNext[__i + 1][__j].setColor(self.__gridCurrent[__i][__j].getColor())
                            self.__gridNext[__i + 1][__j].setStatus(True)
                            self.__gridNext[__i + 1][__j].setCellType("sand")
                            self.__gridCurrent[__i][__j].setCellType("null")
                            self.__gridCurrent[__i][__j].setStatus(False)
                            self.__gridCurrent[__i][__j].setColor((0, 0, 0))
                        else:
                            __statBelowRight = self.__gridCurrent[__i + 1][__j + 1].getStatus()
                            __statBelowLeft = self.__gridCurrent[__i + 1][__j - 1].getStatus()
                            if __statBelowLeft is False and __statBelowRight is False:
                                ranside = ran.randrange(-1, 2, 2)
                                self.__gridNext[__i + 1][__j + ranside].setColor(self.__gridCurrent[__i][__j].getColor())
                                self.__gridNext[__i + 1][__j + ranside].setStatus(True)
                                self.__gridNext[__i + 1][__j + ranside].setCellType("sand")
                                self.__gridCurrent[__i][__j].setCellType("null")
                                self.__gridCurrent[__i][__j].setStatus(False)
                                self.__gridCurrent[__i][__j].setColor((0, 0, 0))
                            elif __statBelowLeft is False and __statBelowRight:
                                self.__gridNext[__i + 1][__j - 1].setColor(self.__gridCurrent[__i][__j].getColor())
                                self.__gridNext[__i + 1][__j - 1].setStatus(True)
                                self.__gridNext[__i + 1][__j - 1].setCellType("sand")
                                self.__gridCurrent[__i][__j].setCellType("null")
                                self.__gridCurrent[__i][__j].setStatus(False)
                                self.__gridCurrent[__i][__j].setColor((0, 0, 0))
                            elif __statBelowRight is False and __statBelowLeft:
                                self.__gridNext[__i + 1][__j + 1].setColor(self.__gridCurrent[__i][__j].getColor())
                                self.__gridNext[__i + 1][__j + 1].setStatus(True)
                                self.__gridNext[__i + 1][__j + 1].setCellType("sand")
                                self.__gridCurrent[__i][__j].setCellType("null")
                                self.__gridCurrent[__i][__j].setStatus(False)
                                self.__gridCurrent[__i][__j].setColor((0, 0, 0))
                    elif __cellType == "water":
                        __statBelow = self.__gridCurrent[__i + 1][__j].getStatus()
                        if __statBelow is False:
                            self.__gridNext[__i + 1][__j].setColor(self.__gridCurrent[__i][__j].getColor())
                            self.__gridNext[__i + 1][__j].setStatus(True)
                            self.__gridNext[__i + 1][__j].setCellType("water")
                            self.__gridCurrent[__i][__j].setCellType("null")
                            self.__gridCurrent[__i][__j].setStatus(False)
                            self.__gridCurrent[__i][__j].setColor((0, 0, 0))
                        else:
                            __statRight = self.__gridCurrent[__i][__j + 1].getStatus()
                            __statLeft = self.__gridCurrent[__i][__j - 1].getStatus()
                            if __statLeft is False and __statRight is False:
                                ranside = ran.randrange(-1, 2, 2)
                                self.__gridNext[__i][__j + ranside].setColor(self.__gridCurrent[__i][__j].getColor())
                                self.__gridNext[__i][__j + ranside].setStatus(True)
                                self.__gridNext[__i][__j + ranside].setCellType("water")
                                self.__gridCurrent[__i][__j].setCellType("null")
                                self.__gridCurrent[__i][__j].setStatus(False)
                                self.__gridCurrent[__i][__j].setColor((0, 0, 0))
                            elif __statLeft is False and __statRight:
                                self.__gridNext[__i][__j - 1].setColor(self.__gridCurrent[__i][__j].getColor())
                                self.__gridNext[__i][__j - 1].setStatus(True)
                                self.__gridNext[__i][__j - 1].setCellType("water")
                                self.__gridCurrent[__i][__j].setCellType("null")
                                self.__gridCurrent[__i][__j].setStatus(False)
                                self.__gridCurrent[__i][__j].setColor((0, 0, 0))
                            elif __statRight is False and __statLeft:
                                self.__gridNext[__i][__j + 1].setColor(self.__gridCurrent[__i][__j].getColor())
                                self.__gridNext[__i][__j + 1].setStatus(True)
                                self.__gridNext[__i][__j + 1].setCellType("water")
                                self.__gridCurrent[__i][__j].setCellType("null")
                                self.__gridCurrent[__i][__j].setStatus(False)
                                self.__gridCurrent[__i][__j].setColor((0, 0, 0))
                    elif __cellType == "mud":
                        __statAbove = self.__gridCurrent[__i + -1][__j].getStatus()
                        if not __statAbove:
                            self.__gridNext[__i - 1][__j].setColor(self.__gridCurrent[__i][__j].getColor())
                            self.__gridNext[__i - 1][__j].setStatus(True)
                            self.__gridNext[__i - 1][__j].setCellType("mud")
                            self.__gridCurrent[__i][__j].setCellType("null")
                            self.__gridCurrent[__i][__j].setStatus(False)
                            self.__gridCurrent[__i][__j].setColor((0, 0, 0))
                        else:
                            __statAboveRight = self.__gridCurrent[__i - 1][__j + 1].getStatus()
                            __statAboveLeft = self.__gridCurrent[__i - 1][__j - 1].getStatus()
                            if __statAboveLeft is False and __statAboveRight is False:
                                ranside = ran.randrange(-1, 2, 2)
                                self.__gridNext[__i - 1][__j + ranside].setColor(self.__gridCurrent[__i][__j].getColor())
                                self.__gridNext[__i - 1][__j + ranside].setStatus(True)
                                self.__gridNext[__i - 1][__j + ranside].setCellType("mud")
                                self.__gridCurrent[__i][__j].setCellType("null")
                                self.__gridCurrent[__i][__j].setStatus(False)
                                self.__gridCurrent[__i][__j].setColor((0, 0, 0))
                            elif __statAboveLeft is False and __statAboveRight:
                                self.__gridNext[__i - 1][__j - 1].setColor(self.__gridCurrent[__i][__j].getColor())
                                self.__gridNext[__i - 1][__j - 1].setStatus(True)
                                self.__gridNext[__i - 1][__j - 1].setCellType("mud")
                                self.__gridCurrent[__i][__j].setCellType("null")
                                self.__gridCurrent[__i][__j].setStatus(False)
                                self.__gridCurrent[__i][__j].setColor((0, 0, 0))
                            elif __statAboveRight is False and __statAboveLeft:
                                self.__gridNext[__i - 1][__j + 1].setColor(self.__gridCurrent[__i][__j].getColor())
                                self.__gridNext[__i - 1][__j + 1].setStatus(True)
                                self.__gridNext[__i - 1][__j + 1].setCellType("mud")
                                self.__gridCurrent[__i][__j].setCellType("null")
                                self.__gridCurrent[__i][__j].setStatus(False)
                                self.__gridCurrent[__i][__j].setColor((0, 0, 0))
                self.__gridCurrent = self.__gridNext
                self.__gridNext = self.__gridEmpty

    def __draw(self):
        for __i in range(self.__row - 1, -1, -1):
            for __j in range(self.__col - 1, -1, -1):
                if self.__gridCurrent[__i][__j].getStatus():
                    pg.draw.rect(
                        self.__screen,
                        self.__gridCurrent[__i][__j].getColor(),
                        (
                            __j * self.__CellSize,
                            __i * self.__CellSize,
                            self.__CellSize,
                            self.__CellSize
                        )
                    )
        self.__clock.tick(60)

        __currentTypeSurface = self.__font.render(f"Type: {self.__typeCurrent}", False, (255, 255, 255))
        self.__screen.blit(__currentTypeSurface, (0, 0))
        __BrushSizeSurface = self.__font.render(f"Brush Size: {self.__brushSize}", False, (255, 255, 255))
        self.__screen.blit(__BrushSizeSurface, (0, 30))
        self.__fps = self.__font.render(f"FPS: {self.__clock.get_fps()}", False, (255, 255, 255))
        self.__screen.blit(self.__fps, (self.__width - 100, 0))

    def gameloop(self):
        while self.__GameOn:
            self.__screen.fill(self.__backgroundColor)
            self.__event()
            self.__update()
            self.__draw()
            pg.display.flip()
        pg.quit()
