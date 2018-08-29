import sys
sys.path.append("../Snake")
from Game import SnakeGame
from Directions import Directions
import copy
import time
import pygame

class Solver:
    def __init__(self,game=None):
        if game == None:
            self.game = SnakeGame(rows=10,cols=10)
        else:
            self.game = game
        self.directions = Directions()
        self.moves = []
        self.directionArray = [self.directions.NORTH,self.directions.SOUTH,self.directions.EAST,self.directions.WEST]
        self.tempBodyLocations = copy.deepcopy(self.game.snake.bodyLocations)
        self.tempDirections = copy.deepcopy(self.game.snake.bodyDirections)

        # self.displaySize = 12

        self.myDisplay=pygame.display.set_mode((self.game.map.cols*self.game.displaySize,self.game.map.rows*self.game.displaySize))
        # self.waitTime = 0.1


    def resetTemps(self):
        self.tempBodyLocations = copy.deepcopy(self.game.snake.bodyLocations)
        self.tempDirections = copy.deepcopy(self.game.snake.bodyDirections)
        self.tempTurningPoints = copy.deepcopy(self.game.snake.turningPoints)


    def legal(self,coord):
        x,y = coord
        # print(coord)
        # if coord in self.game.snake.bodyLocations or coor:

        if x < 1 or y < 1 or x > self.game.map.cols-2 or y > self.game.map.rows-2 or [x,y] in self.tempBodyLocations:
            return False
        else:
            return True

    def isGoalState(self,coord):
        if coord == self.game.map.food:
            return True
        else:
            return False

    def getAvailableMoves(self,position):
        #Given a head position as list, get the legal moves as list of directions (moves)
        # print("Position:",position)
        headX,headY = position
        legalMoves = []
        for move in self.directionArray:
            if self.legal(self.getCoordinates(position,move)):
                legalMoves.append(move)

        # time.sleep(.01)
        # print(legalMoves)
        return legalMoves

    def getCoordinates(self,position,direction):
        #Given position and turn direction, get the new position as a list
        headX,headY = position

        if direction == self.directions.NORTH:
            headY -= 1
        elif direction == self.directions.SOUTH:
            headY += 1
        elif direction == self.directions.EAST:
            headX -= 1
        elif direction == self.directions.WEST:
            headX += 1

        return [headX,headY]


    def getScore(self):
        return self.game.snake.bodySize

    def animate(self):
        for i in range(len(self.moves)):
            self.drawState()
            # self.printState()
            # time.sleep(self.game.waitTime)
            self.updateLocations(self.moves[i])

    def setMoves(self,moves):
        self.moves = moves

    def getMoves(self):
        return self.moves

    def drawTempState(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.myDisplay.fill((255,255,255))
        R=(255,0,0)
        G=(0,255,0)
        W=(255,255,255)
        B=(0,0,255)

        startTime = time.time()

        while time.time() < startTime+self.game.waitTime:
            for event in pygame.event.get():
                if event.type==pygame.quit:
                    pygame.quit()
                    sys.exit()
            for component in self.tempBodyLocations:
                # print(component)
            # component = self.game.snake.bodyLocations[0]
                pygame.draw.rect(self.myDisplay,G,(component[0]*self.game.displaySize,component[1]*self.game.displaySize,self.game.displaySize,self.game.displaySize))

            for i in range(self.game.map.cols):
                pygame.draw.rect(self.myDisplay,R,(i*self.game.displaySize,0,self.game.displaySize,self.game.displaySize))
            for i in range(self.game.map.rows):
                pygame.draw.rect(self.myDisplay,R,(0,i*self.game.displaySize,self.game.displaySize,self.game.displaySize))
            for i in range(self.game.map.cols):
                pygame.draw.rect(self.myDisplay,R,(i*self.game.displaySize,self.game.displaySize*self.game.map.rows-self.game.displaySize,self.game.displaySize,self.game.displaySize))
            for i in range(self.game.map.rows):
                pygame.draw.rect(self.myDisplay,R,(self.game.displaySize*self.game.map.cols-self.game.displaySize,i*self.game.displaySize,self.game.displaySize,self.game.displaySize))

            xFood,yFood = self.game.map.food
            pygame.draw.rect(self.myDisplay,B,(xFood*self.game.displaySize,yFood*self.game.displaySize,self.game.displaySize,self.game.displaySize))

            pygame.display.update()

    def drawState(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.myDisplay.fill((255,255,255))
        R=(255,0,0)
        G=(0,255,0)
        W=(255,255,255)
        B=(0,0,255)

        startTime = time.time()

        while time.time() < startTime+self.game.waitTime:
            for event in pygame.event.get():
                if event.type==pygame.quit:
                    pygame.quit()
                    sys.exit()
            for component in self.game.snake.bodyLocations:
                # print(component)
            # component = self.game.snake.bodyLocations[0]
                pygame.draw.rect(self.myDisplay,G,(component[0]*self.game.displaySize,component[1]*self.game.displaySize,self.game.displaySize,self.game.displaySize))

            for i in range(self.game.map.cols):
                pygame.draw.rect(self.myDisplay,R,(i*self.game.displaySize,0,self.game.displaySize,self.game.displaySize))
            for i in range(self.game.map.rows):
                pygame.draw.rect(self.myDisplay,R,(0,i*self.game.displaySize,self.game.displaySize,self.game.displaySize))
            for i in range(self.game.map.cols):
                pygame.draw.rect(self.myDisplay,R,(i*self.game.displaySize,self.game.displaySize*self.game.map.rows-self.game.displaySize,self.game.displaySize,self.game.displaySize))
            for i in range(self.game.map.rows):
                pygame.draw.rect(self.myDisplay,R,(self.game.displaySize*self.game.map.cols-self.game.displaySize,i*self.game.displaySize,self.game.displaySize,self.game.displaySize))

            xFood,yFood = self.game.map.food
            pygame.draw.rect(self.myDisplay,B,(xFood*self.game.displaySize,yFood*self.game.displaySize,self.game.displaySize,self.game.displaySize))

            pygame.display.update()

    def printState(self):
        #Prints top down. x = 0, y = 0 at top left
        print("#" * self.game.map.cols + "#" * 2)
        counter = 0
        for row in range(1,self.game.map.rows-1):
            s = "#"
            for col in range(1,self.game.map.cols-1):
                if [col,row] in self.game.snake.bodyLocations:
                    if [col,row] == self.game.snake.bodyLocations[0]:
                        s += "*"
                    else:
                        s += "O"
                elif (col,row) == self.game.map.food:
                    s += "x"
                else:
                    s += " "
            s += "#"
            print(s)
        print("#" * self.game.map.cols + "#" * 2)
        print("")

    def move(self,component,direction):
        if direction == self.directions.NORTH:
            component[1] -= 1
        elif direction == self.directions.SOUTH:
            component[1] += 1
        elif direction == self.directions.EAST:
            component[0] -= 1
        elif direction == self.directions.WEST:
            component[0] += 1

        return component

    def updateLocations(self,direction):
        head = copy.deepcopy(self.game.snake.bodyLocations[0])
        newHead = self.move(head,direction)
        self.game.snake.bodyLocations.insert(0,newHead)
        self.game.snake.bodyLocations = self.game.snake.bodyLocations[0:self.game.score+1]

    def updateTemp(self,direction):
        head = copy.deepcopy(self.tempBodyLocations[0])
        newHead = self.move(head,direction)
        self.tempBodyLocations.insert(0,newHead)
        self.tempBodyLocations = self.tempBodyLocations[0:self.game.score+1]
