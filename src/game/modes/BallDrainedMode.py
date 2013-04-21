'''
Created on 2012-04-16

@author: Ryan
'''
import operator
from game.modes.Mode import Mode
from ui.fonts import *
from ui.layers import *

class BallDrainedMode(Mode):
    def __init__(self, game, prio, bonuses):
        Mode.__init__(self, game, prio)
        
        self.bonuses = bonuses # bonus name: score
        
        # bonus names sorted by bonus scores
        self.ordered_bonuses = [key for key, value in sorted(self.bonuses.items(), key=operator.itemgetter(1))]
        
        self.ordered_bonuses.append('Multiplier')
        self.bonuses['Multiplier'] = '%sx' % self.game.player().multiplier
        
        self.current_bonus_index = 0
        self.current_letter_index = 0
        self.ms_per_letter = 100
        self.ms_since_bonus_displayed = 0
        self.waiting = False
        
        self.message_layer = TextLayer(BIG_FONT, 'CONNECTION LOST', self.game.color(255,255,255), align='center')
        self.message_layer.move(1024/2, 130)
        self.bonus_layer = TextLayer(BIG_FONT, '', self.game.color(255,255,255), align='center')
        self.bonus_layer.move(1024/2, 195)
        self.layer = GroupedLayer([self.message_layer, self.bonus_layer])
        
    def frame(self, delta):
        Mode.frame(self, delta)
        if self.waiting:
            return
        bonus = self.ordered_bonuses[self.current_bonus_index]
        value = self.bonuses[bonus]
        bonus_str = '%s: %s' % (bonus, value)
        
        self.ms_since_bonus_displayed += delta*1000
        last_letter = int(self.ms_since_bonus_displayed/self.ms_per_letter)
        
        if last_letter > len(bonus_str):
            last_letter = len(bonus_str)
            self.delay('next', 1.25, self.nextBonus)
            self.waiting = True
        partial_bonus_str = bonus_str[0:last_letter]
        self.bonus_layer.setText(partial_bonus_str)
        
    def nextBonus(self):
        self.current_bonus_index += 1
        
        if self.current_bonus_index >= len(self.bonuses):
            self.done()
            return
        self.current_letter_index = 0
        self.ms_since_bonus_displayed = 0
        self.waiting = False
        
    def done(self):
        self.game.modes.remove(self)
        self.game.endBall()