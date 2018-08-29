import sys
sys.path.append("../Snake")
from Game import SnakeGame
import time
from DFS import DFS
from BFS import BFS

if __name__ == "__main__":
    snakeGame = SnakeGame(rows=10,cols=10)
    bfsSolver = BFS(snakeGame).run()
