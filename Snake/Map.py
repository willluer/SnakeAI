import numpy as np
import copy
from Snake import Snake
from Directions import Directions

class Map:
    def __init__(self,rows=10,cols=10):

        self.directions = Directions()

        self.rows = rows
        self.cols = cols

        # Location of Food
        self.food = (int(self.cols/3),int(self.rows/3))


    def printMap(self):
        print("Food Location: ", str(self.food))




    # TO-DO
    # def updateTurningPoints(self):
    #     for i
