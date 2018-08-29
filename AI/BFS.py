from Solver import Solver
import queue
import time
import copy
import random
class BFS(Solver):
    def __init__(self,game):
        super().__init__(game)
        self.game.printStatus()

    def calculateMoves(self):
        # Calculate moves to get to food
        q = queue.Queue()

        expanded = set()
        root = tuple(self.tempBodyLocations[0])
        currentVertex = [root,[],False]
        coordinatePathDict = {}
        q.put(currentVertex)

        while q.empty() == False:
            self.tempBodyLocations = copy.deepcopy(self.game.snake.bodyLocations)
            currentNode = q.get()
            coord = currentNode[0]
            actions = currentNode[1]

            for i in range(len(actions)):
                # self.drawTempState()
                self.updateTemp(actions[i])

            if self.isGoalState(coord):
                return actions

            # print("Dict:",coordinatePathDict)
            # print("Coord:",coord)
            # print("Actions:",actions)
            # time.sleep(0.1)
            # if coord in expanded and tuple(actions) in coordinatePathDict[coord]:
            if coord in coordinatePathDict.keys():
                if set(actions) in coordinatePathDict[coord]:
                    # print(coord)
                    continue
                else:
                    # print("Maybe None:",coordinatePathDict[coord])
                    # print("tuple action:", tuple(actions))
                    # print("None x2:",coordinatePathDict[coord].append(tuple(actions)))
                    currentPaths = coordinatePathDict[coord]
                    currentPaths.append(set(actions))
                    coordinatePathDict[coord] = currentPaths
            else:
                coordinatePathDict[coord] = [tuple(actions)]

            # print(coordinatePathDict)
            #
            # if coord in expanded:
            #     # print(coord)
            #     continue
            # else:
            #     expanded.add(coord)

            # print(expanded)
            # Iterate through each move
            moves = self.getAvailableMoves(coord)
            random.shuffle(moves)
            for move in moves:
                # print(move)
                # Get new head coordinates of snake with the move
                newCoordinates = tuple(self.getCoordinates(coord,move))

                if newCoordinates not in expanded:
                    q.put([newCoordinates,actions+[move],False])

        print("NO SOLUTION FOUND")
        return None

    def refresh(self):
        self.game.generateFood()
        self.game.snake.bodySize += 1
        self.game.score += 1
        self.moves = []
        self.tempBodyLocations = self.game.snake.bodyLocations

    def run(self):
        while self.game.alive():
            # self.game.printStatus()
            moves = self.calculateMoves()
            if moves == None:
                self.printState()
                print(self.game.score)
                print("GAME OVER")
                break
            self.setMoves(moves)
            self.animate()
            self.refresh()
