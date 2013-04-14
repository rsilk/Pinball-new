'''
Created on 2013-03-02

@author: ryan
'''
from game.modes.Mode import Mode
from game.modes.Menu import Menu, MenuItem

class Scoop(Mode):
    def __init__(self, game, prio):
        Mode.__init__(self, game, prio)
        
        self.addHandler('scoop', 'closed', 30, self.ballInScoop)
        
        self.mode_menu_items = [MenuItem(self.game.datapath('menu_item1.png'), '1'),
                                MenuItem(self.game.datapath('menu_item2.png'), '2'),
                                MenuItem(self.game.datapath('menu_item3.png'), '3'),
                                MenuItem(self.game.datapath('menu_item4.png'), '4'),
                                MenuItem(None, 'mode 5'),
                                MenuItem(None, 'mode 6')]
        
        self.mode_lights = ['ring1', 'ring2', 'ring3', 'ring4', 'ring5', 'ring6']
        self.currently_selected_mode_index = 0
        self.game.lights['scoop'].blink(100, self.game.color(255,255,255))
    
    def ballInScoop(self, switch):
        # select a mode
        self.menu_mode = Menu(self.game, 0, self.mode_menu_items, self.modeSelected, self.modeChanged)
        self.game.modes.append(self.menu_mode)
    
    def modeSelected(self, mode_index):
        # eject ball in a bit
        self.delay('eject', 0.5, self.ejectBall)
        
        # add new mode
        pass
    
    def modeChanged(self, mode_index):
        self.game.lights[self.mode_lights[self.currently_selected_mode_index]].off()
        self.game.lights[self.mode_lights[mode_index]].blink(100, self.game.color(255,255,255))
        self.currently_selected_mode_index = mode_index
    
    def ejectBall(self):
        self.game.drivers['scoop'].pulse(30)