'''
Created on 2012-04-07

@author: Ryan
'''

class Switch:
    def __init__(self, name, x, y, device, offset):
        self.name = name
        self.x = x
        self.y = y
        self.device = device
        self.offset = offset
        
SWITCHES = [
    # cabinet switches
    Switch('menu', 10, 10, 0, 0),
    Switch('exit', 10, 20, 0, 1),
    Switch('up', 10, 30, 0, 2),
    Switch('down', 10, 40, 0, 3),
    Switch('start', 10, 50, 0, 4),
    Switch('flipL', 10, 60, 0, 5),
    Switch('flipR', 10, 70, 0, 6),
    
    # trough switches
    Switch('outhole', 10, 90, 1, 0),
    Switch('trough1', 10, 100, 1, 1),
    Switch('trough2', 10, 110, 1, 2),
    Switch('trough3', 10, 120, 1, 3),
    Switch('shooter', 10, 130, 1, 4),
    
    # lower playfield
    Switch('outlaneL', 10, 150, 1, 5),
    Switch('inlaneL', 10, 160, 1, 6),
    Switch('slingshotL', 10, 170, 1, 7),
    Switch('slingshotR', 10, 180, 1, 8),
    Switch('inlaneR', 10, 190, 1, 9),
    Switch('outlaneR', 10, 200, 1, 10),
]
