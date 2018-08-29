from Map import Map
from Directions import Directions
from Snake import Snake
import time
# import pygame
import copy
import random
import numpy as np

class SnakeGame:
    def __init__(self,rows=10,cols=10):
        self.map = Map(rows=rows,cols=cols)
        self.snake = Snake(rows=rows,cols=cols)
        self.directions = Directions()
        self.displaySize = 12
        # self.myDisplay=pygame.display.set_mode((cols*self.displaySize,rows*self.displaySize))
        self.waitTime = 0.001
        self.score = 0

    def printStatus(self):
        self.snake.printSnake()
        self.map.printMap()
        print("\n")

    def play(self,display=True):
        i = 0
        while self.alive() == True:
            if display:
                self.drawGame()
            else:
                self.printState()
                time.sleep(self.waitTime)
            self.update()
            # time.sleep(.25)

    def update(self):
        self.updateLocations()
        self.updateSize()
        self.deleteTurns()

    def addTurn(self,dir):
        self.printStatus()

        if dir != self.snake.oppositeDirection():
            # print("Adding Turn:", self.snake.head, dir)
            turnLocation = tuple(self.snake.bodyLocations[0])
            self.snake.turningPoints[turnLocation] = [dir,False]
        else:
            print("Illegal Move")

    def deleteTurns(self):
        keyToDelete = []
        for key,val in zip(list(self.snake.turningPoints.keys()),list(self.snake.turningPoints.values())):
            if key not in self.snake.bodyLocations and val[1] == True:
                keyToDelete.append(key)
                # print("Appending")
        if len(keyToDelete) > 0:
            for key in keyToDelete:
                # print("Deleting Turn:", key)
                del self.snake.turningPoints[key]

    def printState(self):
        #Prints top down. x = 0, y = 0 at top left
        print("#" * self.map.cols + "#" * 2)
        counter = 0
        for row in range(self.map.rows):
            s = "#"
            for col in range(self.map.cols):
                if [col,row] in self.snake.bodyLocations.tolist():
                    s += "O"
                elif (col,row) == self.map.food:
                    s += "x"
                else:
                    s += " "
            s += "#"
            print(s)
        print("#" * self.map.cols + "#" * 2)
        print("")

    def drawGame(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.myDisplay.fill((255,255,255))
        R=(255,0,0)
        G=(0,255,0)
        W=(255,255,255)
        B=(0,0,255)

        startTime = time.time()

        while time.time() < startTime+self.waitTime:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.addTurn(self.directions.NORTH)
                    elif event.key == pygame.K_DOWN:
                        self.addTurn(self.directions.SOUTH)
                    elif event.key == pygame.K_LEFT:
                        self.addTurn(self.directions.EAST)
                    elif event.key == pygame.K_RIGHT:
                        self.addTurn(self.directions.WEST)

                if event.type==pygame.quit:
                    pygame.quit()
                    sys.exit()

            for component in self.snake.bodyLocations:
                pygame.draw.rect(self.myDisplay,G,(component[0]*self.displaySize,component[1]*self.displaySize,self.displaySize,self.displaySize))

            for i in range(self.map.cols):
                pygame.draw.rect(self.myDisplay,R,(i*self.displaySize,0,self.displaySize,self.displaySize))
            for i in range(self.map.rows):
                pygame.draw.rect(self.myDisplay,R,(0,i*self.displaySize,self.displaySize,self.displaySize))
            for i in range(self.map.cols):
                pygame.draw.rect(self.myDisplay,R,(i*self.displaySize,self.displaySize*self.map.rows-self.displaySize,self.displaySize,self.displaySize))
            for i in range(self.map.rows):
                pygame.draw.rect(self.myDisplay,R,(self.displaySize*self.map.cols-self.displaySize,i*self.displaySize,self.displaySize,self.displaySize))

            xFood,yFood = self.map.food
            pygame.draw.rect(self.myDisplay,B,(xFood*self.displaySize,yFood*self.displaySize,self.displaySize,self.displaySize))

            pygame.display.update()

    def move(self,component,direction):
        # print("Moving component", component)
        if direction == self.directions.NORTH:
            component[1] -= 1
        elif direction == self.directions.SOUTH:
            component[1] += 1
        elif direction == self.directions.EAST:
            component[0] -= 1
        elif direction == self.directions.WEST:
            component[0] += 1

        return component

    def alive(self):
        head = self.snake.bodyLocations[0]
        if head[0] == 0 or head[0] == self.map.cols-1 or head[1] == 0 or head[1] == self.map.rows-1:
            print("Hit Wall")
            return False

        # headTup = tuple(head)
        # for bodyPart in self.snake.bodyLocations[1:]:
        #     currentPart = tuple(bodyPart)
        #     if headTup == currentPart:
        #         print(headTup,currentPart)
        #         # print("Hit Body")
                # return False

        return True

    def updateLocations(self):
        tail = self.snake.bodyLocations[len(self.snake.bodyLocations)-1]
        tail = tuple(copy.deepcopy(tail))

        if tail in self.snake.turningPoints:
            self.snake.turningPoints[tail] = [self.snake.turningPoints[tail][0],True]

        # Adjust Snake Body Directions and Locations
        for i in range(len(self.snake.bodyLocations)):
            tup = tuple(self.snake.bodyLocations[i])
            if tup in self.snake.turningPoints:
                # print("Tuple in turnigPoints: ", tup)
                self.snake.bodyDirections[i] = self.snake.turningPoints[tup][0]
            self.snake.bodyLocations[i] = self.move(self.snake.bodyLocations[i],self.snake.bodyDirections[i])




    def updateSize(self):
        if self.snake.bodyLocations[0] == list(self.map.food):
            # print("EATEN")
            self.score += 1
            self.food = self.generateFood()
            tail = self.snake.bodyLocations[len(self.snake.bodyLocations)-1]

            newBody = copy.deepcopy(tail)

            if self.snake.bodyDirections[len(self.snake.bodyLocations)-1] == self.directions.NORTH:
                newBody[1] += 1
            elif self.snake.bodyDirections[len(self.snake.bodyLocations)-1] == self.directions.SOUTH:
                newBody[1] -= 1
            elif self.snake.bodyDirections[len(self.snake.bodyLocations)-1] == self.directions.EAST:
                newBody[0] += 1
            elif self.snake.bodyDirections[len(self.snake.bodyLocations)-1] == self.directions.WEST:
                newBody[0] -= 1

            # print("Tail: ", tail)
            # print("Appended", newBody )
            # self.printStatus()
            self.snake.bodyDirections.append(self.snake.bodyDirections[len(self.snake.bodyLocations)-1])
            self.snake.bodyLocations.append(newBody)

            # self.snake.bodyLocations = np.reshape(np.insert(self.snake.bodyLocations,0,newBody),(-1,2))
            # self.snake.bodyDirections.insert(0,self.snake.bodyDirections[0])
    def generateFood(self):
        newFood = self.snake.bodyLocations[0]

        while newFood in self.snake.bodyLocations:
            newFood = [random.choice(range(1,self.map.rows-1)),random.choice(range(1,self.map.cols-1))]

        self.map.food = tuple(newFood)

    def generateFoodFront(self):
        newFood = copy.deepcopy(self.snake.bodyLocations[0])
        if self.snake.bodyDirections[0] == self.directions.NORTH:
            newFood[1] -= 1
        elif self.snake.bodyDirections[0] == self.directions.SOUTH:
            newFood[1] += 1
        elif self.snake.bodyDirections[0] == self.directions.EAST:
            newFood[0] -= 1
        elif self.snake.bodyDirections[0] == self.directions.WEST:
            newFood[0] += 1
        self.map.food = tuple(newFood)
