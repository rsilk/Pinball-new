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
        self.active = False
        
SWITCHES = [
    # cabinet switches
    Switch('menu', 750, 10, 0, 0),
    Switch('exit', 750, 20, 0, 1),
    Switch('up', 750, 30, 0, 2),
    Switch('down', 750, 40, 0, 3),
    Switch('start', 750, 50, 0, 4),
    Switch('flipL', 750, 60, 0, 5),
    Switch('flipR', 750, 70, 0, 6),
    
    # trough switches
    Switch('outhole', 750, 90, 1, 0),
    Switch('trough1', 750, 100, 1, 1),
    Switch('trough2', 750, 110, 1, 2),
    Switch('trough3', 750, 120, 1, 3),
    Switch('shooter', 750, 130, 1, 4),
    
    # lower playfield
    Switch('outlaneL', 750, 150, 1, 5),
    Switch('inlaneL', 750, 160, 1, 6),
    Switch('slingshotL', 750, 170, 1, 7),
    Switch('slingshotR', 750, 180, 1, 8),
    Switch('inlaneR', 750, 190, 1, 9),
    Switch('outlaneR', 750, 200, 1, 10),
    
    # pops
    Switch('pop1', 750, 220, 1, 11),
    Switch('pop2', 750, 230, 1, 12),
    Switch('pop3', 750, 240, 1, 13),
]
