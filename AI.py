from logic import *
import math
import time
from random import randrange

matrix = None
class AI(object):
    def __init__(self, gamegrid):
        self.gamegrid = gamegrid
    def start(self):
        global matrix
        while game_state(self.gamegrid.matrix) == 'not over':
            bestmove, bestscore = best_move(self.gamegrid.matrix)
            while bestmove == None:
                bestmove, bestscore = best_move(self.gamegrid.matrix)

            self.gamegrid.matrix, done = bestmove(self.gamegrid.matrix)
            self.gamegrid.generate_next()
            print self.gamegrid.matrix, bestscore, minus_middle(self.gamegrid.matrix)
            
def log(x):
    if x <= 1: return 0
    return math.log(x, 2)

def smoothness(matrix):
    s = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i < len(matrix) - 1:
                s -= abs(log(matrix[i+1][j]) - log(matrix[i][j]))
            if i > 0:
                s -= abs(log(matrix[i-1][j]) - log(matrix[i][j]))
            if j < len(matrix[i]) - 1:
                s -= abs(log(matrix[i][j+1]) - log(matrix[i][j]))
            if j > 0:
                s -= abs(log(matrix[i][j-1]) - log(matrix[i][j]))
    return s

a = [[3,0],[2,0],[1,0],[0,0],[0,1],[1,1],[2,1],[3,1],[3,2],[2,2],[1,2],[0,2],[0,3],[1,3],[2,3],[3,3]]

def monotonicity(matrix):
    s = 0
    for x, y in zip(a, a[1:]):
        s += matrix[y[0]][y[1]] > matrix[x[0]][x[1]]
    return s

def free_space(matrix):    
    return sum(x.count(0) for x in matrix)

def corners(matrix):
    return sum(log(matrix[x][y])**2 for x in [0, 3] for y in [0, 3])

def minus_middle(matrix):
    return sum(-log(matrix[x][y])**2 for x in [1, 2] for y in [1, 2])


def heuristic(matrix):
    
#    print free_space(matrix), smoothness(matrix), corners(matrix), minus_middle(matrix)
    highest = log(max(map(max, matrix)))
    
    return smoothness(matrix) + highest*free_space(matrix) + minus_middle(matrix)
# + 10*smoothness(matrix) + \
#           3 * corners(matrix) + 3 * minus_middle(matrix)

def add_random(matrix):
    f = free_space(matrix)
    if f > 4:
        i, j = randrange(4), randrange(4)
        while matrix[i][j] != 0:
            i, j = randrange(4), randrange(4)
        matrix[i][j] = 2
        return True
    elif f == 0:
        return False

    wi, wj, wh = None, None, float('inf')
    for i in xrange(4):
        for j in xrange(4):
            if matrix[i][j] != 0: continue
            matrix[i][j] = 2
            h = heuristic(matrix)
            if h < wh:
                wi, wj, wh = i, j, h
            matrix[i][j] = 0
    matrix[wi][wj] = 2
    return True

    
    
MAX_DEPTH = 5
MOVES = [left, up, down, right]

def best_move(matrix, depth=0):
    if depth > MAX_DEPTH: return None, heuristic(matrix)
    pos = []
    for move1 in MOVES:
        newmatrix, done = move1(matrix)
        if newmatrix == matrix: continue
        if not add_random(newmatrix): continue
        for move2 in MOVES:
            newnewmatrix, done = move2(newmatrix)
            if newnewmatrix == newmatrix: continue
            if not add_random(newnewmatrix): continue
            h = heuristic(newnewmatrix)
            pos.append((h, move1, newnewmatrix))

    pos.sort(reverse=True)
    pos = pos[:min(len(pos), 2)]
    bestmove, bestscore = None, -float('inf')
    for h, move, mat in pos:
        m, s = best_move(mat, depth+1)
        if s > bestscore:
            bestscore = s
            bestmove = move

    return bestmove, bestscore
