'''
Created on 2013-03-02

@author: ryan
'''
from game.modes.Mode import Mode

class Scoop(Mode):
    def __init__(self, game, prio):
        Mode.__init__(self, game, prio)
        
        self.addHandler('scoop', 'closed', 30, self.ballInScoop)
        
    
    def ballInScoop(self, switch):
        # select a mode
        
        
        # eject ball in a bit
        self.delay('eject', 1.25, self.ejectBall)
    
    def ejectBall(self):
        self.game.drivers['scoop'].pulse(30)