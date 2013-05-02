'''
Created on 2013-03-02

@author: ryan
'''
from game.modes.Mode import Mode
from game.modes.Menu import Menu, MenuItem

from game.modes.StoryMode import StoryMode
from game.modes.TakedownMode import TakedownMode
from game.modes.OverloadMode import OverloadMode
from game.modes.CodebreakerMode import CodebreakerMode

class Scoop(Mode):
    def __init__(self, game, prio):
        Mode.__init__(self, game, prio)
        
        self.addHandler('scoop', 'closed', 30, self.ballInScoop)
        
        self.mode_menu_items = [MenuItem(self.game.datapath('menu_overload.png'), '1', self.game.color(255,255,255)),
                                MenuItem(self.game.datapath('menu_takedown.png'), '2', self.game.color(255,255,255)),
                                MenuItem(self.game.datapath('menu_codebreaker.png'), '3', self.game.color(255,255,255)),
                                MenuItem(self.game.datapath('menu_item4.png'), '4', self.game.color(255,255,255)),
                                MenuItem(None, 'mode 5', self.game.color(255,255,255)),
                                MenuItem(None, 'mode 6', self.game.color(255,255,255))]
        
        self.mode_lights = ['ring1', 'ring2', 'ring3', 'ring4', 'ring5', 'ring6']
        
        self.modes = [OverloadMode(game, 500, self),
                      TakedownMode(game, 500, self),
                      CodebreakerMode(game, 500, self),
                      None,
                      None,
                      None]
        
        self.currently_selected_mode_index = 0
        self.game.lights['scoop'].blink(100, self.game.color(255,255,255))
    
    def ballInScoop(self, switch):
        # select a mode
        self.menu_mode = Menu(self.game, 100, self.mode_menu_items, self.modeSelected, self.modeChanged)
        self.game.modes.add(self.menu_mode)
    
    def modeSelected(self, mode_index):
        # add new mode
        mode = self.modes[mode_index]
        if mode:
            self.game.modes.add(mode)
    
    def modeChanged(self, mode_index):
        self.game.lights[self.mode_lights[self.currently_selected_mode_index]].off()
        self.game.lights[self.mode_lights[mode_index]].blink(100, self.game.color(255,255,255))
        self.currently_selected_mode_index = mode_index
    
    def ejectBall(self):
        print "eject"
        self.game.drivers['scoop'].pulse(30)