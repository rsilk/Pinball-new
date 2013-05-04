'''
Created on 2012-04-10

@author: ryan
'''
from game.modes.Mode import Mode
from ui.layers import TextLayer
import ui.fonts

class Trough(Mode):
    def __init__(self, game, prio):
        Mode.__init__(self, game, prio)
    
        self.balls = 3
        self.balls_in_play = 0
        self.balls_in_lock = 0
        self.balls_in_trough = self.balls
        
        self.trough_switches = ['trough1', 'trough2', 'trough3']
        self.lock_switches = ['lock1', 'lock2', 'lock3']
        self.outhole_switch = 'outhole'
        self.shooter_switch = 'shooter'
        
        self.addHandler(self.outhole_switch, 'closed', 30, self.ballDrained)
        
        for switch_name in self.trough_switches:
            self.addHandler(switch_name, 'closed', 0, self.handleTroughSwitch)
        
        for switch_name in self.lock_switches:
            self.addHandler(switch_name, 'closed', 0, self.handleLockSwitch)
        
        self.updateDebugInfo()
    
    def updateDebugInfo(self):
        text = 'T:%s L:%s P:%s' % (self.balls_in_trough, self.balls_in_lock, self.balls_in_play)
        self.layer = TextLayer(ui.fonts.SMALL_FONT, text,
                               self.game.color(255,255,255), 'center')
        self.layer.move(1024/2, 5)
    
    def ballDrained(self, switch):
        # always want to kick a ball from the outhole into the trough
        self.game.drivers['outhole'].pulse(30)
        self.balls_in_play -= 1
        self.balls_in_trough += 1
        self.game.ballDrained()
        self.updateDebugInfo()
    
    def launchBall(self):
        # if there's a ball sitting on trough1, launch ball
        if True: #self.game.switches['trough1'].active:
            self.game.drivers['trough'].pulse(30)
            self.balls_in_play += 1
            self.balls_in_trough -= 1
        
        # else ??
        self.updateDebugInfo()
    
    def unlockBall(self):
        if True: #self.game.switches['lock1'].active:
            self.game.drivers['lock'].pulse(30)
            self.balls_in_lock -= 1
            self.balls_in_play += 1
        self.updateDebugInfo()
    
    def handleTroughSwitch(self, switch):
        self.delay('check trough', 0.2, self.updateTroughStatus)
    
    def handleLockSwitch(self, switch):
        print "handle lock"
        self.delay('check lock', 0.2, self.updateLockStatus)
    
    def updateTroughStatus(self):
        self.balls_in_trough = 0
        for switch_name in self.trough_switches:
            if self.game.switches[switch_name].active:
                self.balls_in_trough += 1
        self.updateDebugInfo()
    
    def updateLockStatus(self):
        print "update lock"
        balls_in_lock = 0
        for switch_name in self.lock_switches:
            if self.game.switches[switch_name].active:
                balls_in_lock += 1
        print "%s in lock" % balls_in_lock
        if balls_in_lock > self.balls_in_lock:
            self.balls_in_lock = balls_in_lock
            self.balls_in_play = self.balls - self.balls_in_lock - self.balls_in_trough
            self.game.ballLocked()
        self.updateDebugInfo()