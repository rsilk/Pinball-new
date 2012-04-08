'''
Created on 2012-02-18

@author: ryan
'''
import time
from .Player import Player
from hardware.Events import EventTypes

from game.modes.AttractMode import AttractMode
from game.modes.TestDisplayMode import TestDisplayMode
from game.modes.Lanes import Lanes

from game.switches import SWITCHES
from game.lights import LIGHTS

class GameMain:
    
    def __init__(self, display, events):
        self.display = display
        self.events = events
        self.last_tick_at = time.time()
        
        self.done = False
        
        # initialize switches
        self.switches = {}
        for switch in SWITCHES:
            self.switches[switch.name] = switch
        
        # initialize lights
        self.lights = {}
        for light in LIGHTS:
            self.lights[light.name] = light
        
        self.players = []
        self.modes = [AttractMode(self, 0),
                      TestDisplayMode(self, 0),
                      Lanes(self, 10)]
    
    def go(self):
        while not self.done:
            self.tick()
    
    
    def tick(self):
        for event in self.events.getEvents():
            if event.TYPE == EventTypes.QUIT:
                self.done = True
            else:
                for mode in self.modes:
                    mode.event(event)
        
        now = time.time()
        delta = now - self.last_tick_at
        self.last_tick_at = now
        
        self.display.beginFrame()
        
        for light in self.lights.itervalues():
            light.tick(delta)
        
        for mode in self.modes:
            mode.frame(delta)
        
        self.display.endFrame()