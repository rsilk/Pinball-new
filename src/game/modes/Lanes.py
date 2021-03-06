'''
Created on 2012-04-07

@author: Ryan
'''
from game.modes.Mode import Mode

class Lanes(Mode):
    
    def __init__(self, game, prio, switch_names, light_names):
        Mode.__init__(self, game, prio)
        
        self.switches = switch_names
        self.lights = light_names
        
        self.states = [False] * len(self.switches)
        
        for switch_name in self.switches:
            self.addHandler(switch_name, 'closed', 0, self.switchClosed)
        
        self.addHandler('flipL', 'closed', 0, self.rotateLeft)
        self.addHandler('flipR', 'closed', 0, self.rotateRight)
    
    def switchClosed(self, switch):
        index = self.switches.index(switch.name)
        self.states[index] = True
        
        self.game.player().score += 100
        if all(self.states):
            self.complete()
        else:
            self._updateLights()
    
    def rotateLeft(self, switch):
        leftmost = self.states[0]
        self.states = self.states[1:]
        self.states.append(leftmost)
        self._updateLights()
    
    def rotateRight(self, switch):
        rightmost = self.states[-1]
        self.states = self.states[:-1]
        self.states.insert(0, rightmost)
        self._updateLights()
    
    def complete(self):
        self.game.player().score += 1000
        self.states = [False] * len(self.switches)
        self._updateLights()
        
    def _updateLights(self):
        for state, light_name in zip(self.states, self.lights):
            if state:
                self.game.lights[light_name].on(self.game.color(255,255,255))
            else:
                self.game.lights[light_name].off()