'''
Created on 2013-05-01

@author: ryan
'''
from game.modes.Mode import Mode
from ui.layers import TextLayer
import ui.fonts

class BallLockedMode(Mode):
    '''
    classdocs
    '''


    def __init__(self, game, prio, ball):
        '''
        Constructor
        '''
        Mode.__init__(self, game, prio)
        self.layer = TextLayer(ui.fonts.BIG_FONT,
                               'Ball %s locked' % ball,
                               self.game.color(255,255,255),
                               'center')
        self.layer.move(1024/2, 175)
        self.layer.opaque = True
        self.delay('wait', 1.5, self.done)
    
    def done(self):
        self.game.modes.remove(self)