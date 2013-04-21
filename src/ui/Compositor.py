'''
Created on 2012-04-08

@author: Ryan
'''

class Compositor:
    def __init__(self, game, target):
        self.game = game
        self.target = target
        self.last_visible_modes = set()
    
    def frame(self, delta):
        modes = self.game.modes
        
        dirty = False
        visible_modes = []
        for mode in modes.orderedModes():
            layer = mode.getLayer()
            if not layer:
                continue
            dirty = dirty or layer.isDirty()
            visible_modes.append(mode)
            if layer.opaque:
                break
        if not dirty and set(visible_modes) != self.last_visible_modes:
            dirty = True
        self.last_visible_modes = set(visible_modes)
        
        if dirty:
            self.target.clear()
            for mode in reversed(visible_modes):
                # reversed so top layers get drawn last
                layer = mode.getLayer()
                layer.drawOnto(self.target)
                layer.setDirty(False)
            return True
        else:
            return False
