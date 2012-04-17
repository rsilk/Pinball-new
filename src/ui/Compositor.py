'''
Created on 2012-04-08

@author: Ryan
'''

class Compositor:
    def __init__(self, game, target):
        self.game = game
        self.target = target
    
    def frame(self, delta):
        modes = self.game.modes
            
        for mode in reversed(modes):
            # reversed so top layers get drawn last
            layer = mode.getLayer()
            if not layer:
                continue
            layer.drawOnto(self.target, delta)
            if layer.opaque:
                break
