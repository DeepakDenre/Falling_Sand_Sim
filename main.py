from Engine import Engine
from Ini import *

if __name__ == "__main__":
    Eng = Engine(
        ScreenWidth,
        ScreenHeight,
        "Falling Sand"
    )
    Eng.GameLoop()