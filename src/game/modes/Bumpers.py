'''
Created on 2012-04-07

@author: Ryan
'''
from game.modes.Mode import Mode

class Bumpers(Mode):
    def __init__(self, game, prio):
        Mode.__init__(self, game, prio)
        
        self.bumper_switches = ['pop1', 'pop2', 'pop3']
        self.slingshot_switches = ['slingshotL', 'slingshotR']
        
        for switch_name in self.slingshot_switches:
            self.addHandler(switch_name, 'closed', 0, self.slingshot)
        
        for switch_name in self.bumper_switches:
            self.addHandler(switch_name, 'closed', 0, self.bumper)
    
    
    def slingshot(self, switch):
        # assumes driver name == switch name for now
        self.game.drivers[switch.name].pulse(20)
        self.game.lights[switch.name].pulse(50, 255,255,255)
        self.game.player().score += 100
    
    def bumper(self, switch):
        # assumes driver name == switch name for now
        self.game.drivers[switch.name].pulse(20)
        self.game.lights[switch.name].pulse(50, 255,255,255)
        self.game.player().score += 100