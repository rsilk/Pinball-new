'''
Created on 2012-04-08

@author: Ryan
'''
import pygame

from game.modes.Mode import Mode
from ui.fonts import *
from ui.layers import *

class ScoreDisplay(Mode):
    def __init__(self, game, prio):
        Mode.__init__(self, game, prio)
        
        self.score_layer = TextLayer(TITLE_FONT, '', (255,0,0), align='center')
        self.score_layer.move(1024/2, 175)
        
        self.player_layer = TextLayer(SMALL_FONT, '', (255,255,255))
        self.player_layer.move(10, 360)
        
        self.ball_layer = TextLayer(SMALL_FONT, '', (255,255,255), align='right')
        self.ball_layer.move(1014, 360)
        self.layer = GroupedLayer([self.score_layer, self.player_layer, self.ball_layer])
        self.layer.opaque = True
    
    def frame(self, delta):
        player = self.game.player()
        if player:
            self.score_layer.setText('%02d' % player.score)
            self.player_layer.setText(player.name)
            self.ball_layer.setText('Ball %s' % self.game.current_ball)
        else:
            self.player_layer.setText('Game over')
            self.ball_layer.setText('Game over')