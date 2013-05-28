'''
Created on 2013-05-01

@author: ryan
'''
from game.modes.Mode import Mode
from ui.layers import TextLayer
import ui.fonts

class MultiballMode(Mode):
    '''
    Left ramp-right ramp lights jackpot.
    Hitting all 4 standups increases jackpot value (exponentially?)
    Scoop scores jackpot but resets value
    '''
    def __init__(self, game, prio):
        Mode.__init__(self, game, prio)
        
        self.layer = TextLayer(ui.fonts.BIG_FONT,
                               'Multiball!',
                               self.game.color(255,255,255),
                               'center')
        self.layer.move(1024/2,175)
        self.layer.opaque = True
        
        self.base_jackpot_value = 20000
        self.jackpot_value = self.base_jackpot_value
        self.jackpot_multiplier = 3
        self.jackpot_lit = False
        
        self.ramps_hit = [False, False]
        
        self.standup_switches = ['standup1', 'standup2', 'standup3', 'standup4']
        self.standup_lights = ['standup1', 'standup2', 'standup3', 'standup4']
        self.standups_hit = [False, False, False, False]
        
        self.delay('done introducing', 2, self.doneIntroducing)
    
    def doneIntroducing(self):
        self.layer = None
        
        self.addHandler('rampL', 'closed', 0, self.handleRamp)
        self.addHandler('rampR', 'closed', 0, self.handleRamp)
        
        for switch in self.standup_switches:
            self.addHandler(switch, 'closed', 0, self.handleStandup)
        for light in self.standup_lights:
            self.game.lights[light].on(self.game.color(255,255,255))
        
        self.addHandler('scoop', 'closed', 10, self.handleJackpot)
        
        self.game.trough.unlockBall()
        self.delay('unlock', 0.75, self.unlock)
    
    def unlock(self):
        self.game.trough.unlockBall()
        if self.game.trough.balls_in_lock:
            self.delay('unlock', 0.75, self.unlock)
    
    def handleRamp(self, switch):
        if switch.name == 'rampL':
            self.ramps_hit[0] = True
        elif switch.name == 'rampR':
            self.ramps_hit[1] = True
        if all(self.ramps_hit):
            # light jackpot
            self.jackpot_lit = True
            self.game.lights['jackpot'].blink(100, self.game.color(0,0,255))
            self.ramps_hit = [False, False]
    
    def handleStandup(self, switch):
        index = self.standup_switches.index(switch.name)
        self.standups_hit[index] = True
        self.game.lights[self.standup_lights[index]].off()
        
        if all(self.standups_hit):
            self.jackpot_value *= self.jackpot_multiplier
            self.standups_hit = [False] * len(self.standups_hit)
            for light in self.standup_lights:
                self.game.lights[light].on(self.game.color(255,255,255))
            # TODO: show something about new jackpot value
    
    def handleJackpot(self, switch):
        if not self.jackpot_lit:
            self.game.drivers['scoop'].pulse(50)
            return
        self.game.lights['jackpot'].off()
        self.game.player().score += self.jackpot_value
        self.jackpot_value = self.base_jackpot_value
        self.jackpot_lit = False
        
        # make a big fuss about jackpot
        self.game.drivers['scoop'].pulse(50)
        return True
    
    def stopped(self):
        self.game.lights['jackpot'].off()
        for light in self.standup_lights:
            self.game.lights[light].off()
        