'''
Created on 2012-02-18

@author: ryan
'''
import time
from .Player import Player
from hardware.Events import EventTypes

from .modes.AttractMode import AttractMode

class GameMain:
    
    def __init__(self, display, events):
        self.display = display
        self.events = events
        self.last_tick_at = time.time()
        
        self.done = False
        
        self.players = []
        self.modes = [AttractMode(self, 0)]
    
    def go(self):
        while not self.done:
            self.tick()
    
    
    def tick(self):
        for event in self.events.getEvents():
            if event.TYPE == EventTypes.QUIT:
                self.done = True
        
        now = time.time()
        delta = now - self.last_tick_at
        self.last_tick_at = now
        
        self.display.beginFrame()
        
        for mode in self.modes:
            mode.frame(delta)
        
        self.display.endFrame()