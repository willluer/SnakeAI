import sys
sys.path.append("../Snake")
from Game import SnakeGame
import time
from DFS import DFS
from BFS import BFS

if __name__ == "__main__":
    snakeGame = SnakeGame(rows=12,cols=12)
    bfsSolver = BFS(snakeGame).run()
