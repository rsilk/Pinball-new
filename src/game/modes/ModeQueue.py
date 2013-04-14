'''
Created on 2013-04-05

@author: Ryan
'''
import operator

class ModeQueue(object):
    def __init__(self):
        self.modes = []
    
    def extend(self, modes):
        for mode in modes:
            self.add(mode)
        
    def add(self, mode):
        if mode in self.modes:
            raise ValueError, "Attempted to add mode "+str(mode)+", already in mode queue."
        self.modes.append(mode)
        # Sort by priority, descending:
        self.modes.sort(key=operator.attrgetter('prio'), reverse=True)
        mode.started()
        if mode == self.modes[0]:
            mode.top()

    def remove(self, mode):
        self.modes.remove(mode)
        mode.stopped()
        if len(self.modes) > 0:
            self.modes[0].top()

    def event(self, event):
        for mode in self.modes[:]:
            handled = mode.event(event)
            if handled:
                break
    
    def tick(self, now, delta):
        for mode in self.modes[:]:
            mode.handleDelayed(now)
            mode.frame(delta)
    
    def orderedModes(self):
        ''' return a list of all the modes in the queue, in priority order '''
        return self.modes