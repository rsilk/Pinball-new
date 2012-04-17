'''
Created on 2012-02-18

@author: ryan
'''
class Player:
    
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.multiplier = 1
        self.extra_balls = 0
        self.gamestate = None
        self.bonuses = {}
        
        self.bonuses = {'bonus1': 12345,
                        'bonus2': 6789}