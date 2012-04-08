'''
Created on 2012-02-19

@author: ryan
'''
import time
import ui.fonts
from .Mode import Mode

class AttractMode(Mode):
    
    def __init__(self, *args):
        Mode.__init__(self, *args)
        
        self.time_since_last_switch = 0
        
        self.foo = False
        
        self.game.lights['start'].blink(0.5, 255,0,0)
    
    def frame(self, delta):
        self.time_since_last_switch += delta
        
        if self.time_since_last_switch > 1.5:
            self.time_since_last_switch -= 1.5
            self.foo = not self.foo
            
        if self.foo:
            surf = ui.fonts.BIG_FONT.render('Attract', True, (255,0,0))
        else:
            surf = ui.fonts.BIG_FONT.render('Mode', True, (255,0,0))
        
        self.game.display.dmd.blit(surf, (400,300))