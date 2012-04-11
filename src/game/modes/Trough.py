'''
Created on 2012-04-10

@author: ryan
'''
from game.modes.Mode import Mode

class Trough(Mode):
    def __init__(self, game, prio):
        Mode.__init__(self, game, prio)
    
        self.balls = 3
        self.balls_in_play = 0
        self.balls_in_lock = 0
        
        self.trough_switches = ['trough1', 'trough2', 'trough3']
        self.lock_switches = ['lock1', 'lock2', 'lock3']
        self.outhole_switch = 'outhole'
        self.shooter_switch = 'shooter'
        
        self.addHandler(self.outhole_switch, 'closed', 30, self.ballDrained)
    
        
    
    def ballDrained(self, switch):
        # always want to kick a ball from the outhole into the trough
        self.game.drivers['outhole'].pulse(30)
        self.balls_in_play -= 1
        self.game.ballDrained()
    
    def launchBall(self):
        # if there's a ball sitting on trough1, launch ball
        if True: #self.game.switches['trough1'].active:
            self.game.drivers['trough'].pulse(30)
            self.balls_in_play += 1
        
        # else ??
    
    def unlockBall(self):
        if True: #self.game.switches['lock1'].active:
            self.game.drivers['lock'].pulse(30)
            self.balls_in_lock -= 1
    
    def updateTroughStatus(self, switch):
        balls_in_trough = 0
        for switch_name in self.trough_switches:
            if self.game.switches[switch_name].active:
                balls_in_trough += 1
    
    def updateLockStatus(self, switch):
        balls_in_lock = 0
        for switch_name in self.lock_switches:
            if self.game.switches[switch_name].active:
                balls_in_lock += 1
        
        if balls_in_lock > self.balls_in_lock:
            self.balls_in_lock = balls_in_lock
            self.game.ballLocked()