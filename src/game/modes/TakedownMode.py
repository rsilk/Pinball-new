'''
Created on 2013-04-16

@author: ryan
'''
from .StoryMode import StoryMode
class TakedownMode(StoryMode):
    '''
    classdocs
    '''
    MODE_NAME = 'Takedown'
    MODE_DESC = 'Shoot pop bumpers'

    def __init__(self, game, prio, scoop_mode):
        '''
        Constructor
        '''
        StoryMode.__init__(self, game, prio, scoop_mode)
        
        self.lights = ['pop1', 'pop2', 'pop3']
        self.switches = ['pop1', 'pop2', 'pop3']
        self.level_colors = [self.game.color(255,0,0), #red
                             self.game.color(0,255,0), #green
                             self.game.color(0,0,255), #blue
                             ]
        self.level_hits_required = [10, 20, 50]
        self.level = 0
        self.hits_till_next_level = self.level_hits_required[self.level]
        
    def start(self):
        for light in self.lights:
            self.game.lights[light].blink(500, self.level_colors[self.level])
        
        for switch in self.switches:
            self.addHandler(switch, 'closed', 0, self.popHit)
    
    def popHit(self, switch):
        self.game.player().score += (1000 * self.level)
        self.hits_till_next_level -= 1
        
        if self.hits_till_next_level == 0:
            self.level += 1
            self.hits_till_next_level = self.level_hits_required[self.level]
            for light in self.lights:
                self.game.lights[light].blink(500, self.level_colors[self.level])
            