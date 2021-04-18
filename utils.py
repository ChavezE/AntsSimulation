# util.py

# Imports 
from enum import Enum, auto

class Point():
    def __init__(self, yy=0, xx=0):
        self.y = yy
        self.x = xx

class Direction(Enum):
    FIRST = 1
    N = FIRST
    NE = auto()
    E = auto()
    SE = auto()
    S = auto()
    SW = auto()
    W = auto()
    NW = auto()
    LAST = NW
"""
reference
    NW  N   NE
    W   .   E   
    SW  S   SE
"""

