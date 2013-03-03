'''
Created on 2012-04-07

@author: Ryan
'''
import time

class Driver:
    def __init__(self, name, x, y, device, offset):
        self.name = name
        self.x = x
        self.y = y
        self.device = device
        self.offset = offset
        self.active_time = 0
        self.active = False
    
    def tick(self, delta):
        if self.active_time:
            self.active_time -= delta
            if self.active_time <= 0:
                self.active = False
                self.active_time = 0
    
    def pulse(self, millis):
        self.active_time = millis/1000.0 # active_time is in seconds
        self.active = True


DRIVERS = [
    Driver('outhole', 800, 10, 5, 0),
    Driver('trough', 800, 20, 5, 1),
    Driver('slingshotL', 800, 30, 5, 2),
    Driver('slingshotR', 800, 40, 5, 3),
    Driver('flipL', 800, 50, 5, 4),
    Driver('flipR', 800, 60, 5, 5),
    Driver('pop1', 800, 70, 5, 6),
    Driver('pop2', 800, 80, 5, 7),
    Driver('pop3', 800, 90, 5, 8),
    Driver('lock', 800, 100, 5, 9),
    Driver('scoop', 800, 110, 5, 10),
    ]