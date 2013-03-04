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
        
    
    def ballInScoop(self, switch):
        # select a mode
        menu_items = [MenuItem(self.game.datapath('menu_item1.png'), '1'),
                      MenuItem(self.game.datapath('menu_item2.png'), '2'),
                      MenuItem(self.game.datapath('menu_item3.png'), '3'),
                      MenuItem(self.game.datapath('menu_item4.png'), '4')]
        self.menu_mode = Menu(self.game, 0, menu_items, self.modeSelected)
        self.game.modes.append(self.menu_mode)
    
    def modeSelected(self, mode_index):
        # eject ball in a bit
        self.delay('eject', 0.5, self.ejectBall)
        
        # add new mode
        pass
    
    def ejectBall(self):
        self.game.drivers['scoop'].pulse(30)