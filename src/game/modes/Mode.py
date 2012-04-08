'''
Created on 2012-02-19

@author: ryan
'''
from hardware.Events import EventTypes

class Mode:
    def __init__(self, game, prio):
        self.game = game
        self.prio = 0 # higher priorities will get processed first
        self.handled_switches = {}
    
    def event(self, event):
        # return True if this event has been handled with a terminal handler
        # return False if other modes should handle this.
        
        if event.TYPE in (EventTypes.SWITCH_CLOSED, EventTypes.SWITCH_OPEN):
            if self.handled_switches.has_key(event.switch.name):
                (handled_event, handler) = self.handled_switches[event.switch.name]
                if event.TYPE == handled_event:
                    return handler(event.switch)
                
        return False
    
    def frame(self, delta):
        pass
    
    def addHandler(self, switch_name, event, delay, handler):
        # handler will be called with switch as the argument
        if event == 'closed':
            event = EventTypes.SWITCH_CLOSED
        elif event == 'open':
            event = EventTypes.SWITCH_OPEN
        self.handled_switches[switch_name] = (event, handler)