'''
Created on 2012-04-16

@author: Ryan
'''
from game.modes.Mode import Mode

class BallDrainedMode(Mode):
    def __init__(self, game, prio):
        Mode.__init__(self, game, prio)
        
    def frame(self, delta):
        self.game.modes.remove(self)
        self.game.endBall()