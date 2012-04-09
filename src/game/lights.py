'''
Created on 2012-04-07

@author: Ryan
'''

class Light:
    def __init__(self, name, x, y, device, offsetR, offsetG, offsetB):
        self.name = name
        self.x = x
        self.y = y
        self.device = device
        self.offsetR = offsetR
        self.offsetG = offsetG
        self.offsetB = offsetB
        self.set_r = 0
        self.set_g = 0
        self.set_b = 0
        self.r = 0
        self.g = 0
        self.b = 0

        self.time_until_blink = 0
        self.blink_state = False
        self.blink_period = 0
    
    def tick(self, delta):
        if self.time_until_blink:
            self.time_until_blink -= delta
            if self.time_until_blink <= 0:
                if self.blink_period == 0:
                    # handle 'pulse'
                    self.time_until_blink = 0
                else:
                    self.time_until_blink += self.blink_period
                self.blink_state = not self.blink_state
                if self.blink_state:
                    self.r = self.set_r
                    self.g = self.set_g
                    self.b = self.set_b
                else:
                    self.r = 0
                    self.g = 0
                    self.b = 0
    
    def off(self):
        self.blink_period = 0
        self.set_r = 0
        self.set_g = 0
        self.set_b = 0
        self.r = 0
        self.g = 0
        self.b = 0
    
    def on(self, r, g, b):
        self.set_r = r
        self.set_g = g
        self.set_b = b
        self.r = r
        self.g = g
        self.b = b
    
    def pulse(self, time, r, g, b):
        # time is in milliseconds
        self.time_until_blink = time/1000.0
        self.blink_period = 0
        self.blink_state = True
        self.set_r = r
        self.set_g = g
        self.set_b = b
        self.r = r
        self.g = g
        self.b = b
    
    def blink(self, period, r, g, b):
        # period is in milliseconds
        self.set_r = r
        self.set_g = g
        self.set_b = b
        self.r = r
        self.g = g
        self.b = b
        self.blink_state = True
        self.blink_period = period/1000.0
        self.time_until_blink = period/1000.0
    

LIGHTS = [
    # cabinet lights
    Light('start', 29, 69, 0, 7, None, None),
    
    # lower PF
    Light('outlaneL', 275, 21, 2, 0, 1, 2),
    Light('inlaneL', 279, 44, 2, 3, 4, 5),
    Light('slingshotL', 203, 83, 3, 0, 1, 2),
    Light('slingshotR', 202, 234, 3, 3, 4, 5),
    Light('inlaneR', 278, 271, 4, 0, 1, 2),
    Light('outlaneR', 276, 294, 4, 3, 4, 5),
    ]