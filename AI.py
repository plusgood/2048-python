from logic import *
import math
import time
from random import randrange

class AI(object):
    def __init__(self, gamegrid):
        self.gamegrid = gamegrid
    def start(self):
        while game_state(self.gamegrid.matrix) == 'not over':
            bestmove, bestscore = best_move(self.gamegrid.matrix)
            self.gamegrid.matrix, done = bestmove(self.gamegrid.matrix)
            self.gamegrid.generate_next()
            print self.gamegrid.matrix
            
def log(x):
    if x == 0: return 0
    return math.log(x)

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
    #print matrix
    
    try:return sum(matrix, []).count(0)
    except Exception as e:
        print e

def heuristic(matrix):
    return 20*free_space(matrix) + 2*monotonicity(matrix) + smoothness(matrix)

def add_random(matrix):
    if sum(matrix, []).count(0) == 0: return
    i, j = randrange(4), randrange(4)
    while matrix[i][j] != 0:
        i, j = randrange(4), randrange(4)
    matrix[i][j] = 2
    
    
MAX_DEPTH = 5
def best_move(matrix, depth=0):
    if depth > MAX_DEPTH: return matrix, heuristic(matrix)
    possible = []
    bestmove, bestscore = None, -float('inf')
    
    for move in [left, up, down, right]:
        newmatrix, done = move(matrix)
        add_random(newmatrix)
        if newmatrix == matrix: continue
        else:
            m, s = best_move(newmatrix, depth+1)
            if s > bestscore:
                bestscore = s
                bestmove = move
                
    return bestmove, bestscore
    
