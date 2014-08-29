from logic import *
import time

class AI(object):
  def __init__(self, gamegrid):
    self.gamegrid = gamegrid
  def start(self):
    while game_state(self.gamegrid.matrix) == 'not over':
      self.gamegrid.matrix, done = left(self.gamegrid.matrix)
      self.gamegrid.generate_next()
      time.sleep(0.5)
      self.gamegrid.matrix, done = down(self.gamegrid.matrix)
      self.gamegrid.generate_next()
      time.sleep(0.5)
      
    a = 0
    mat = map(list, self.gamegrid.matrix)
    while True:
      if self.gamegrid.matrix != mat:
        mat = map(list, self.gamegrid.matrix)
        print mat
    
