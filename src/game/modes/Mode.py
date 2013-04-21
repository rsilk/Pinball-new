'''
Created on 2012-02-19

@author: ryan
'''
import time
from hardware.Events import EventTypes

class Mode(object):
    def __init__(self, game, prio):
        self.game = game
        self.prio = prio # higher priorities will get processed first
        self.handled_switches = [] # (swname, event, handler)
        self.delayed = []
        self.layer = None
        self.dirty = False
    
    def event(self, event):
        # return True if this event has been handled with a terminal handler
        # return False if other modes should handle this.
        
        if event.TYPE in (EventTypes.SWITCH_CLOSED, EventTypes.SWITCH_OPEN):
            for (switch_name, handled_event, handler) in self.handled_switches:
                if event.switch.name == switch_name and event.TYPE == handled_event:
                    return handler(event.switch)
                
        return False
    
    def frame(self, delta):
        if self.layer:
            self.layer.tick(delta)
    
    def getLayer(self):
        return self.layer
    
    def addHandler(self, switch_name, event, delay, handler):
        # handler will be called with switch as the argument
        if event == 'closed':
            event = EventTypes.SWITCH_CLOSED
        elif event == 'open':
            event = EventTypes.SWITCH_OPEN
        self.handled_switches.append((switch_name, event, handler))
    
    def delay(self, name, delay, handler, *args):
        ''' delay in seconds '''
        delayed_time = time.time() + delay
        self.delayed.append((delayed_time, name, handler, args))
    
    def handleDelayed(self, now):
        next_delayed = []
        for (delayed_time, name, handler, args) in self.delayed:
            if delayed_time <= now:
                handler(*args)
            else:
                next_delayed.append((delayed_time, name, handler, args))
        self.delayed = next_delayed
    
    def started(self):
        ''' called when the mode is added to the active queue '''
        pass
    
    def stopped(self):
        ''' called when the mode is removed from the active queue '''
        pass
    
    def top(self):
        ''' called when the mode is first in the active queue '''
        pass
    
    def ballEnded(self):
        ''' called when the ball is over '''
        pass