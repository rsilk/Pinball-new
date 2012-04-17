'''
Created on 2012-04-07

@author: Ryan
'''
from game.modes.Mode import Mode

class Flippers(Mode):
    def __init__(self, game, prio):
        Mode.__init__(self, game, prio)
        
        self.addHandler('flipL', 'closed', 0, self.flip)
        self.addHandler('flipR', 'closed', 0, self.flip)
        
        self.addHandler('flipL', 'open', 0, self.unflip)
        self.addHandler('flipR', 'open', 0, self.unflip)
    
    def flip(self, switch):
        self.game.drivers[switch.name].active = True
    
    def unflip(self, switch):
        self.game.drivers[switch.name].active = False