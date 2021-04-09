import cv2
import numpy as np
import random
from enum import Enum, auto

# globals
x_limit_px = 1000
y_limit_px = 750


EMPTY = [0,0,0]
ANT_SKIN = [255,255,255]
INITAL_ANT_COUNT = 15
world_matrix = np.zeros((y_limit_px, x_limit_px, 3),dtype=np.uint8)
ANT_STEP_SIZE = 3
VERBOSE = False

class Ant:
    def __init__(self, y, x, idd):
        self.y = y
        self.x = x
        self.id = idd

class AntDirection(Enum):
    FIRST = 0
    N = FIRST
    S = auto()
    W = auto()
    E = auto()
    NE = auto()
    NW = auto()
    SE = auto()
    SW = auto()
    LAST = SW
"""
reference
    NW        N         NE
        :------------:
        | ants world |
    W   |            |   E
        |            |
        :------------:
    SW        S         SE
"""

def drawAnt(y,x):
    if (x  > x_limit_px or y > y_limit_px):
        raise Exception("Ant is going off limits")

    # draw the and in the world mat
    world_matrix[y,x] = ANT_SKIN
    world_matrix[y-1,x] = ANT_SKIN

def moveAnt(y_init, x_init, y_final, x_final):
    if (x_init > x_limit_px or y_init > y_limit_px or x_final > x_limit_px or y_final > y_limit_px):
        raise Exception("Ant is going off limits")
    
    # remove ant from old place
    world_matrix[y_init, x_init] = EMPTY
    world_matrix[y_init-1, x_init] = EMPTY

    # draw ant in new place
    drawAnt(y_final, x_final)

# return next coords
def chooseRandomMove(y_init, x_init, verbose):
    move = random.randint(AntDirection.FIRST.value, AntDirection.LAST.value)

    if (verbose):
        print (move)

    if (move == AntDirection.N.value):
        return y_init - ANT_STEP_SIZE, x_init
    elif (move == AntDirection.S.value):
        return y_init + ANT_STEP_SIZE, x_init
    elif (move == AntDirection.W.value):
        return y_init, x_init - ANT_STEP_SIZE
    elif (move == AntDirection.E.value):
        return y_init, x_init + ANT_STEP_SIZE
    elif (move == AntDirection.NE.value):
        return y_init - ANT_STEP_SIZE, x_init + ANT_STEP_SIZE
    elif (move == AntDirection.NW.value):
        return y_init - ANT_STEP_SIZE , x_init - ANT_STEP_SIZE
    elif (move == AntDirection.SE.value):
        return y_init + ANT_STEP_SIZE, x_init + ANT_STEP_SIZE
    elif (move == AntDirection.SW.value):
        return y_init + ANT_STEP_SIZE, x_init - ANT_STEP_SIZE

def isValidMove(y,x):
    return y < y_limit_px and y >= 0 and x < x_limit_px and x >= 0 


def showAntColonyStats(antColony):
    for ant in antColony:
        print (ant.y, " , ", ant.x)

def main():
    
    for direction in AntDirection:
        print (direction, " : ", direction.value)

    # inital position
    x_init = 100
    y_init = 500

    # make an colony of ants
    # for now each ant is just a Point()
    antColony = []
    for i in range (INITAL_ANT_COUNT):
        antColony.append(Ant(y_init, x_init, i))


    # run simulation
    while True:
        # update all ants
        for ant in antColony:
            print ("Ant id: ", ant.id)
            print ("Ant y: ", ant.y)
            print ("Ant x: ", ant.x)
            y_cur = ant.y
            x_cur = ant.x

            drawAnt(y_cur,x_cur)

            # make a random move.
            y_next, x_next = chooseRandomMove(y_cur, x_cur, VERBOSE)
            
            print ("x_cur:", x_cur, " y_cur:", y_cur, " x_next:", x_next, " y_next:", y_next)
            # only move if the position is valid
            if (isValidMove(y_next, x_next)):
                moveAnt(y_cur, x_cur, y_next, x_next)
                
                # update ant pos
                ant.y = y_next
                ant.x = x_next

        showAntColonyStats(antColony)
    
        cv2.imshow("World", world_matrix)
        k = cv2.waitKey(10)

        # press 'c' to exit.
        if (k == 99):
            break

    cv2.destroyAllWindows()

# call main func
main()