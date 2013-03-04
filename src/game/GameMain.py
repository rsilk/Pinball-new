'''
Created on 2012-02-18

@author: ryan
'''
import time
import os.path
import operator

from hardware.Events import EventTypes
from ui.Compositor import Compositor

from game.modes.AttractMode import AttractMode
from game.modes.TestDisplayMode import TestDisplayMode
from game.modes.Lanes import Lanes
from game.modes.Flippers import Flippers
from game.modes.Bumpers import Bumpers
from game.modes.ScoreDisplay import ScoreDisplay
from game.modes.BallDrainedMode import BallDrainedMode
from game.modes.Trough import Trough
from game.modes.Menu import Menu, MenuItem

from game.ColorManager import ColorManager
from game.Player import Player
from game.switches import SWITCHES
from game.lights import LIGHTS
from game.drivers import DRIVERS

class GameMain:
    
    def __init__(self, display, events):
        self.display = display
        self.compositor = Compositor(self, self.display.dmd)
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
        
        # initialize drivers
        self.drivers = {}
        for driver in DRIVERS:
            self.drivers[driver.name] = driver
            
        self.color_manager = ColorManager()
        
        self.players = []
        self.current_player = None
        self.current_ball = 0
        
        # initialize common modes
        menu_items = [MenuItem(self.datapath('menu_item1.png'), '1'),
                      MenuItem(self.datapath('menu_item2.png'), '2'),
                      MenuItem(self.datapath('menu_item3.png'), '3'),
                      MenuItem(self.datapath('menu_item4.png'), '4')]
        self.attract_mode = Menu(self, 0, menu_items)
#        self.attract_mode = AttractMode(self, 0)
        self.test_display_mode = TestDisplayMode(self, 0)
        
        self.trough = Trough(self, 1)
        self.modes = [self.attract_mode,
                      self.test_display_mode,
                      self.trough]
    
    def go(self):
        while not self.done:
            self.tick()
    
    def datapath(self, path):
        # get the path to a datafile
        base_dir = os.path.dirname(__file__)
        
        return os.path.join(base_dir, '..', '..', 'data', path)
    
    def color(self, *input_color):
        return self.color_manager.translate(*input_color)
    
    def player(self):
        # get the current player
        return self.current_player
    
    def tick(self):
        for event in self.events.getEvents():
            # update switch state
            if event.TYPE == EventTypes.SWITCH_CLOSED:
                event.switch.active = True
            elif event.TYPE == EventTypes.SWITCH_OPEN:
                event.switch.active = False
                
            if event.TYPE == EventTypes.QUIT:
                self.done = True
            else:
                for mode in self.modes:
                    mode.event(event)
        
        now = time.time()
        delta = now - self.last_tick_at
        self.last_tick_at = now
        
        self.display.beginFrame()
        
        for mode in self.modes[:]: # copy in case modes get added
            mode.handleDelayed(now)
            mode.frame(delta)
        
        for light in self.lights.itervalues():
            light.tick(delta)
        
        for driver in self.drivers.itervalues():
            driver.tick(delta)
        
        # reorder modes by priority
        self.modes = sorted(self.modes, key=operator.attrgetter('prio'), reverse=True)
        
        self.compositor.frame(delta)
        self.display.endFrame()
    
    def addPlayer(self):
        player = Player('Player %s' % (len(self.players) + 1))
        self.players.append(player)
    
    def startGame(self):
        self.current_ball = 1
        self.addPlayer()
        self.modes.remove(self.attract_mode)
        
        self.score_display_mode = ScoreDisplay(self, 1)
        
        self.current_player = self.players[0]
        
        self.startBall()
    
    def endGame(self):
        self.modes.append(self.attract_mode)
    
    def startBall(self):
        self.basic_modes = [self.score_display_mode,
                            Flippers(self, 5),
                            Bumpers(self, 5),
                            Lanes(self, 10)]
        self.modes.extend(self.basic_modes)
        self.trough.launchBall()

    def endBall(self):
        # TODO: handle extra balls
        current_player_offset = self.players.index(self.current_player)
        next_player_offset = current_player_offset + 1
        if next_player_offset == len(self.players):
            next_player_offset = 0
            self.current_ball += 1
            if self.current_ball > 3:
                self.endGame()
                return
            
        self.current_player = self.players[next_player_offset]
        self.startBall()
    
    def ballDrained(self):
        # TODO: don't do this if in multiball
        
        for mode in self.basic_modes:
            self.modes.remove(mode)
        
        self.modes.append(BallDrainedMode(self, 100, self.player().bonuses)) # this will eventually call endBall
    
    def ballLocked(self):
        pass