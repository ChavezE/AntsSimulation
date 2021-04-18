# ant.py

import numpy as np
import random
from enum import Enum

from utils import Point, Direction

class Ant:
    #
    # General Properties for Ant class.
    #

    # Ants Body.
    # Desc: Pixel wise cardinal reference for Ants based on Points()
    # 
    """
            x
          x . x
            x
    """ 
    ANT_BODY = [(0,0),(1,0),(-1,0),(0,1),(0,-1)]
    assert ANT_BODY[0][0] == 0
    assert ANT_BODY[0][1] == 0

    # Ant Skin (B,G,R)
    # Desc: 8 bit 3 dimmentional coloring 255=max light.
    ANT_SKIN = [255,255,255]

    # Steps Ants travel on movement.
    ANT_STEP_SIZE = 3
    
    LOG = False
    # 
    # Constructor
    # 
    def __init__(self, point, idd):
        #
        # Ants atributes.
        #
        self.pos = point
        self.direction = Direction(Direction.FIRST)
        self.id = idd
        self.sight = 5

    # return next coords
    def MoveFromDirection(self, direction):
        if (direction == Direction.N or direction == Direction.FIRST):
            self.pos = Point(self.pos.y - self.ANT_STEP_SIZE, self.pos.x )
        elif (direction == Direction.S):
            self.pos = Point(self.pos.y + self.ANT_STEP_SIZE, self.pos.x )
        elif (direction == Direction.W):
            self.pos = Point(self.pos.y, self.pos.x  - self.ANT_STEP_SIZE)
        elif (direction == Direction.E):
            self.pos = Point(self.pos.y, self.pos.x  + self.ANT_STEP_SIZE)
        elif (direction == Direction.NE):
            self.pos = Point(self.pos.y - self.ANT_STEP_SIZE, self.pos.x  + self.ANT_STEP_SIZE)
        elif (direction == Direction.NW):
            self.pos = Point(self.pos.y - self.ANT_STEP_SIZE , self.pos.x  - self.ANT_STEP_SIZE)
        elif (direction == Direction.SE):
            self.pos = Point(self.pos.y + self.ANT_STEP_SIZE, self.pos.x  + self.ANT_STEP_SIZE)
        elif (direction == Direction.SW or direction == Direction.LAST):
            self.pos = Point(self.pos.y + self.ANT_STEP_SIZE, self.pos.x  - self.ANT_STEP_SIZE)


    def chooseNextDirection(self, tickk = -1):
        """
        To make the move the Ant will have a propety called 'sight range', with this propety the ant can make a scan of 
        what's in this range. Then it can make desitions based in what it sees.
        """
        def between(num, a, b, inclusive=True):
            if (inclusive):
                return num >= a and num <= b
            else:
                return num >= a and num <= b

        mean_value = 8.0
        std_value = 3.0
        ndis_no = np.random.default_rng().normal(mean_value, std_value,1)

        # Ants naive intuition probabilistic distribution
        #

        # deltas
        d1 = 4
        d2 = 5
        d3 = 6
        d3 = 7
        d4 = 8

        # Chose tick # from probabilistic dist.
        #

        tick = 0 # Poiting N
        if (between(ndis_no, mean_value - d1, mean_value + d1)):
            pass        # go N
        elif (between(ndis_no, mean_value - d2, mean_value)):
            tick = -1   # go NW
        elif (between(ndis_no, mean_value, mean_value + d2)):
            tick = 1    # go NE
        elif (between(ndis_no,  mean_value - d3, mean_value - d2)):
            tick = -2   # go W
        elif (between(ndis_no, mean_value + d2, mean_value + d3)):
            tick = 2    # go E
        elif (between(ndis_no, mean_value - d4, mean_value - d3)):
            tick = 3    # go SW
        elif (between(ndis_no, mean_value + d3, mean_value + d4)):
            tick = -3   # go SE
        else:
            tick = 4

        # TODO    
        # Take a ROI of the map based on sight.
        # ROI = world_matrix[self.pos.y - self.sight, self.pos.x - self.sight : 
        #     self.pos.y + self.sight, self.pos.x + self.sight]

        # compute the next direction 
        if (tickk == -1):
            compassNextDirection = self.direction.value + tick
        else:
            compassNextDirection = self.direction.value + tickk


        if (compassNextDirection < Direction.FIRST.value):
            # for now, do hard code mapping
            if (compassNextDirection == 0):
                compassNextDirection = 8
            elif (compassNextDirection == -1):
                compassNextDirection = 7
            elif (compassNextDirection == -2):
                compassNextDirection = 3
        elif (compassNextDirection > Direction.LAST.value):
            # for now, do hard code mapping
            if (compassNextDirection == 9):
                compassNextDirection = 1
            elif (compassNextDirection == 10):
                compassNextDirection = 2
            elif (compassNextDirection == 11):
                compassNextDirection = 3
            elif (compassNextDirection == 12):
                compassNextDirection = 4

        if (self.LOG):
            print ("\t Ant id: ", self.id, " cur dir: ", self.direction, " num next dir: ", \
                ndis_no, " next dir: ", Direction(compassNextDirection))

        return Direction(compassNextDirection)
