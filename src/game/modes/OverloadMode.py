'''
Created on 2013-04-16

@author: ryan
'''
from .StoryMode import StoryMode

from ui.layers import GroupedLayer, TextLayer
import ui.fonts

class OverloadMode(StoryMode):
    '''
    classdocs
    '''
    MODE_NAME = 'Overload'
    MODE_DESC = 'Shoot pop bumpers'

    def __init__(self, game, prio, scoop_mode):
        '''
        Constructor
        '''
        StoryMode.__init__(self, game, prio, scoop_mode)
        
        self.blink_delay_ms = 100
        self.lights = ['pop1', 'pop2', 'pop3']
        self.switches = ['pop1', 'pop2', 'pop3']
        self.level_colors = [self.game.color(255,0,0), #red
                             self.game.color(0,255,0), #green
                             self.game.color(0,0,255), #blue
                             ]
        self.level_hits_required = [10, 20, 50]
        self.max_level_score = 10000
        self.at_max_level = False
        self.level = 0
        self.hits_till_next_level = self.level_hits_required[self.level]
        
        self.hits_remaining_layer = TextLayer(ui.fonts.BIG_FONT,
                                      '%s hits to next level' % self.level_hits_required[0],
                                      self.game.color(255,255,255),
                                      align='center')
        self.hits_remaining_layer.move(1024/2, 80)
        self.level_layer = TextLayer(ui.fonts.BIG_FONT,
                                     'Pops level 1', 
                                     self.game.color(255,255,255),
                                     align='center')
        self.level_layer.move(1024/2, 50)
        
    def start(self):
        for light in self.lights:
            self.game.lights[light].blink(self.blink_delay_ms, self.level_colors[self.level])
        
        for switch in self.switches:
            self.addHandler(switch, 'closed', 0, self.popHit)
        
        self.layer = GroupedLayer([self.hits_remaining_layer, self.level_layer])
    
    def popHit(self, switch):
        if self.level >= len(self.level_hits_required):
            self.game.player().score += self.max_level_score
            return True
        
        self.game.player().score += (1000 * (self.level+1))
        self.hits_till_next_level -= 1
        
        if self.hits_till_next_level == 0:
            self.level += 1
            if self.level >= len(self.level_hits_required):
                self.level_layer.setText('Pops at maximum!')
                self.layer = GroupedLayer([self.level_layer])
                for light in self.lights:
                    self.game.lights[light].on(self.game.color(255,255,255))
                return True
                
            self.hits_till_next_level = self.level_hits_required[self.level]
            self.level_layer.setText('Pops level %s' % str(self.level+1))
            for light in self.lights:
                self.game.lights[light].blink(self.blink_delay_ms, self.level_colors[self.level])
        self.hits_remaining_layer.setText('%s hits to next level' % self.hits_till_next_level)
        return True