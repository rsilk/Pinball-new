'''
Created on 2013-05-01

@author: ryan
'''
from game.modes.Mode import Mode
from ui.layers import TextLayer
import ui.fonts

class MultiballMode(Mode):
    def __init__(self, game, prio):
        Mode.__init__(self, game, prio)
        
        self.game.modes.remove(self)