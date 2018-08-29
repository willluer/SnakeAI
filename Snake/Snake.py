from Directions import Directions
import numpy as np

class Snake:
    def __init__(self,rows,cols):
        self.directions = Directions()

        # Body Locations
        self.head = [int(cols/2),int(rows/2)]
        self.bodyLocations = [[int(cols/2),int(rows/2+1)]]#,[int(cols/2),int(rows/2+2)],[int(cols/2),int(rows/2+3)]]
        # self.bodyLocations = [[5,6]]
        self.bodySize = 3

        # Orientations
        self.bodyDirections= [self.directions.NORTH,self.directions.NORTH,self.directions.NORTH]
        # self.orientation = self.directions.NORTH
        self.turningPoints = {}

    def oppositeDirection(self):
        if self.bodyDirections[0] == self.directions.NORTH:
            return self.directions.SOUTH
        elif self.bodyDirections[0] == self.directions.SOUTH:
            return self.directions.NORTH
        elif self.bodyDirections[0] == self.directions.WEST:
            return self.directions.EAST
        elif self.bodyDirections[0] == self.directions.EAST:
            return self.directions.WEST

    def printSnake(self):
        print("Body:", self.bodyLocations)
        print("Score: ", self.bodySize)
        print("Turning Points:", self.turningPoints)
