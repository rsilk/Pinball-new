'''
Created on 2012-02-19

@author: ryan
'''

class Mode:
    def __init__(self, game, prio):
        self.game = game
        self.prio = 0 # higher priorities will get processed first
    
    def event(self, event):
        # return True if this event has been handled with a terminal handler
        # return False if other modes should handle this.
        return False
    
    def frame(self, delta):
        pass