from logic import *
from math import log
import time

class AI(object):
    def __init__(self, gamegrid):
        self.gamegrid = gamegrid
    def start(self):
        while game_state(self.gamegrid.matrix) == 'not over':
            self.gamegrid.matrix, done = left(self.gamegrid.matrix)
            print self.gamegrid.matrix
            best_move(self.game.matrix)
            self.gamegrid.generate_next()
            time.sleep(0.5)
            self.gamegrid.matrix, done = down(self.gamegrid.matrix)
            self.gamegrid.generate_next()
            time.sleep(0.5)

def smoothness(matrix):
    s = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i < len(matrix) - 1:
                s += abs(log(matrix[i+1][j]) - log(matrix[i][j]))
            if i > 0:
                s += abs(log(matrix[i-1][j]) - log(matrix[i][j]))
            if j < len(matrix[i]) - 1:
                s += abs(log(matrix[i][j+1]) - log(matrix[i][j]))
            if j > 0:
                s += abs(log(matrix[i][j-1]) - log(matrix[i][j]))
    return s

a = [[3,0],[2,0],[1,0],[0,0],[0,1],[1,1],[2,1],[3,1],[3,2],[2,2],[1,2],[0,2],[0,3],[1,3],[2,3],[3,3]]
assert len(a) == 16
def monotonicity(matrix):
    s = 0
    for x, y in zip(a, a[1:]):
        s += log(matrix[y[0]][y[1]]) - log(matrix[x[0]][x[1]])
    return s

def free_space(matrix):
    return sum(matrix, []).count(0)

def heuristic(matrix):
    return 20*free_space(matrix) + 2*monotonicity(matrix) + smoothness(matrix)
    
def best_move(matrix):
    pass
        


        
