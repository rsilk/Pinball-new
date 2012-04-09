'''
Created on 2012-02-19

@author: ryan
'''
import time
from ui.fonts import *
from ui.layers import *
from game.modes.Mode import Mode

class AttractMode(Mode):
    
    def __init__(self, *args):
        Mode.__init__(self, *args)
        
        self.game.lights['start'].blink(500, 255,0,0)
        
        self.packet_layer = MotionEffect(FadeEffect(TextLayer(TITLE_FONT, 'PACKET', (255,0,0)), 0, 50), 100, 0)
        self.packet_layer.move(0, 150)
        
        self.storm_layer = MotionEffect(TextLayer(TITLE_FONT, 'STORM', (255,0,0)), 50, 10)
        self.storm_layer.move(100, 250)
        
        self.layer = GroupedLayer([self.packet_layer, self.storm_layer])
        