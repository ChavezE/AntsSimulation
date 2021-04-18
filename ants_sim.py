import cv2
import numpy as np
import random
from enum import Enum

from utils import Point, Direction
from ant import Ant

#
# Globals
#
LOG = False

# inital position
x_init = 100
y_init = 50

# make an colony of ants
antColony = []


# Frame limits
x_limit_px = 1000
y_limit_px = 500

# Frame colors
BACKGROUND_COLOR = [0,0,0]

# World Customization
INITAL_ANT_COUNT = 100
world_matrix = np.ones((y_limit_px, x_limit_px, 3),dtype=np.uint8) 
world_matrix[:] = BACKGROUND_COLOR
ANT_STEP_SIZE = 1
ANT_BODY = [(0,0),(1,0),(-1,0),(0,1),(0,-1)]
assert ANT_BODY[0][0] == 0
assert ANT_BODY[0][1] == 0
ANT_SKIN = [255,255,255]

def drawAntInWorld(ant):
    x = ant.pos.x 
    y = ant.pos.y

    # draw the and in the world mat
    for Point in ANT_BODY:
        yTemp = y + Point[0]
        xTemp = x + Point[1]
        world_matrix[yTemp , xTemp] = ANT_SKIN
        world_matrix[yTemp, xTemp] = ANT_SKIN

def removeAntFromWorld(obj):
    if (type(obj) == type(Ant)):
        x = obj.pos.x 
        y = obj.pos.y
    else:
        x = obj.x 
        y = obj.y

    for Point in ANT_BODY:
        yTemp = y + Point[0]
        xTemp = x + Point[1]
        world_matrix[yTemp , xTemp] = BACKGROUND_COLOR
        world_matrix[yTemp, xTemp] = BACKGROUND_COLOR

# return next coords
def nextPointFromDirection(point, direction):
    if (direction == Direction.N.value):
        return Point(point.y - ANT_STEP_SIZE, point.x )
    elif (direction == Direction.S.value):
        return Point(point.y + ANT_STEP_SIZE, point.x )
    elif (direction == Direction.W.value):
        return Point(point.y, point.x  - ANT_STEP_SIZE)
    elif (direction == Direction.E.value):
        return Point(point.y, point.x  + ANT_STEP_SIZE)
    elif (direction == Direction.NE.value):
        return Point(point.y - ANT_STEP_SIZE, point.x  + ANT_STEP_SIZE)
    elif (direction == Direction.NW.value):
        return Point(point.y - ANT_STEP_SIZE , point.x  - ANT_STEP_SIZE)
    elif (direction == Direction.SE.value):
        return Point(point.y + ANT_STEP_SIZE, point.x  + ANT_STEP_SIZE)
    else:
        return Point(point.y + ANT_STEP_SIZE, point.x  - ANT_STEP_SIZE)

# TODO: we need to consider ants morphology here
def isValidPoint(point):
    return (point.y < y_limit_px - 5) and point.y > 5 and (point.x < x_limit_px - 5) and point.x > 5

def showAntColonyStats(antColony):
    for ant in antColony:
        print ("\t Ant id: ", ant.id, "\t (", ant.pos.y, ",", ant.pos.x, ")", "\t direction: ", ant.direction)

def main():

    # Initialice Ant colony.
    for i in range (INITAL_ANT_COUNT):
        antColony.append(Ant(Point(y_init,x_init), i))

    # run simulation
    #
    while True:
        # update all ants
        for ant in antColony:            
            # safe the current position
            prevPos= ant.pos

            # make a move
            direction = ant.chooseNextDirection()

            nextPoint = nextPointFromDirection(ant.pos, direction)
            
            if (isValidPoint(nextPoint)):                
                # update ant pos
                ant.MoveFromDirection(direction)
                ant.direction = direction
                
                # draw the current position
                drawAntInWorld(ant)
            
            else:
                # make the ant turn around
                dirr = ant.chooseNextDirection(4) # 4 = turn back
                ant.MoveFromDirection(dirr)
                ant.direction = dirr

            # remove the ant from previous pos
            removeAntFromWorld(prevPos)
        
        if (LOG):
            showAntColonyStats(antColony)
    
        cv2.imshow("World", world_matrix)
        k = cv2.waitKey(5)

        # press 'c' to exit.
        if (k == 99):
            break
        
    cv2.destroyAllWindows()

# call main func
main()