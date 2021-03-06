'''
Created on 2012-02-19

@author: ryan
'''
import time
from ui.fonts import *
from ui.layers import *
from game.modes.Mode import Mode
from game.lightshows import *

class AttractMode(Mode):
    
    def __init__(self, *args):
        Mode.__init__(self, *args)
        
        self.game.lights['start'].blink(100, self.game.color(255,255,255))
        
        self.packet_layer = TextLayer(TITLE_FONT, 'PACKET', self.game.color(255,255,255))
        self.packet_layer.move(275, 150)
        
        self.storm_layer = TextLayer(TITLE_FONT, 'STORM', self.game.color(255,255,255))
        self.storm_layer.move(475, 205)
        
        self.start_layer = TextLayer(BIG_FONT, 'PRESS START', self.game.color(255,255,255), align='center')
        self.start_layer.move(1024/2, 350)
        
        infile = open(__file__, 'r')
        code_lines = ['test']
#        code_lines = [line.strip('\n') for line in infile.readlines()]
        infile.close()
        code_surf = renderLines(SMALL_FONT, code_lines, False, (45,45,45))
        self.code_layer = DisplayLayer([code_surf])
        
        self.layer = GroupedLayer([self.code_layer, self.packet_layer, self.storm_layer])
        
        self.delay('blink', 0.5, self.blinkInsert, True)
        self.addHandler('start', 'closed', 0, self.startPressed)
        
        self.lightshow = Searchlight(self.game.lights.values(), 2.0)
    
    def frame(self, delta):
        Mode.frame(self, delta)
        self.lightshow.frame(delta)
    
    def blinkInsert(self, on):
        # blink the "press start" text every half second
        if on:
            self.layer = GroupedLayer([self.code_layer, self.packet_layer, self.storm_layer, self.start_layer])
        else:
            self.layer = GroupedLayer([self.code_layer, self.packet_layer, self.storm_layer])
        self.delay('blink', 0.5, self.blinkInsert, not on)
    
    def startPressed(self, switch):
        self.game.lights['start'].off()
        self.game.startGame()