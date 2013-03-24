'''
Created on 2012-04-07

@author: Ryan
'''

class Light:
    def __init__(self, name, x, y, deviceR, deviceG, deviceB, offsetR, offsetG, offsetB):
        self.name = name
        self.x = x
        self.y = y
        self.deviceR = deviceR
        self.deviceG = deviceG
        self.deviceB = deviceB
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
    
    def on(self, color):
        r = color.r
        g = color.g
        b = color.b
        self.set_r = r
        self.set_g = g
        self.set_b = b
        self.r = r
        self.g = g
        self.b = b
    
    def pulse(self, time, color):
        # time is in milliseconds
        r = color.r
        g = color.g
        b = color.b
        
        self.time_until_blink = time/1000.0
        self.blink_period = 0
        self.blink_state = True
        self.set_r = r
        self.set_g = g
        self.set_b = b
        self.r = r
        self.g = g
        self.b = b
    
    def blink(self, period, color):
        # period is in milliseconds
        r = color.r
        g = color.g
        b = color.b
        
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
    Light('start', 29, 69, 0, 0, 0, 4, 2, 0),
    
    # lower PF
    Light('outlaneL', 275, 21, 2, 2, 2, 0, 1, 2),
    Light('inlaneL', 279, 44, 2, 2, 2, 3, 4, 5),
    Light('slingshotL', 203, 83, 3, 3, 3, 0, 1, 2),
    Light('slingshotR', 202, 234, 3, 3, 3, 3, 4, 5),
    Light('inlaneR', 278, 271, 4, 4, 4, 0, 1, 2),
    Light('outlaneR', 276, 294, 4, 4, 4, 3, 4, 5),
    
    # upper PF
    Light('pop1', 554, 198, 5, 5, 5, 0, 1, 2),
    Light('pop2', 602, 148, 5, 5, 5, 3, 4, 5),
    Light('pop3', 618, 241, 5, 5, 5, 6, 7, 8),
    
    # mode ring
    Light('ring1', 412, 131, 5, 5, 5, 0, 1, 2),
    Light('ring2', 412, 183, 5, 5, 5, 0, 1, 2),
    Light('ring3', 365, 209, 5, 5, 5, 0, 1, 2),
    Light('ring4', 320, 183, 5, 5, 5, 0, 1, 2),
    Light('ring5', 320, 131, 5, 5, 5, 0, 1, 2),
    Light('ring6', 365, 104, 5, 5, 5, 0, 1, 2),
    ]