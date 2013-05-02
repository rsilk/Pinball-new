'''
Created on 2013-04-16

@author: ryan
'''
import random
import string
import ui.fonts
from ui.layers import TextLayer
from .StoryMode import StoryMode

class CodebreakerMode(StoryMode):
    '''
    Hit every shot to unlock all the letters
    '''
    MODE_NAME = 'Codebreaker'
    MODE_DESC = 'Crack the password'

    def __init__(self, game, prio, scoop_mode):
        '''
        Constructor
        '''
        StoryMode.__init__(self, game, prio, scoop_mode)
        
        # TODO: proper lights and switches when added
        self.lights = ['leftorbit', 'pop1', 'pop2', 'pop3', 'rightorbit']
        self.switches = ['orbitL', 'standup1', 'standup2', 'standup3', 'orbitR']
        
        self.level = 0
        self.letter_scramble_delay = 50
        
        # password is a random one of these each time the mode starts
        self.words = ['hunts', 'brain', 'safer']
    
    def start(self):
        self.level = 0
        for switch in self.switches:
            self.addHandler(switch, 'closed', 0, self.switchHit)
        
        self.layer = TextLayer(ui.fonts.TITLE_FONT,
                               '???', 
                               self.game.color(255,255,255), align='center')
        self.layer.move(1024/2, 50)
        self.layer.opaque = True
        
        self.startLevel()
        
    def startLevel(self):
        self.letters_found = [False] * len(self.switches)
        self.password = random.choice(self.words)
        
        for light in self.lights:
            self.game.lights[light].blink(500, self.game.color(255,0,0))
        
        self.delay('scramble', 0.1, self.scramble)
        self.delay('defeat', 60, self.defeat)
    
    def switchHit(self, switch):
        self.game.player().score += 1000
        
        index = self.switches.index(switch.name)
        self.letters_found[index] = True
        self.game.lights[self.lights[index]].off()
        
    def scramble(self):
        letters = []
        for i, found in enumerate(self.letters_found):
            if found:
                letters.append(self.password[i])
            else:
                letters.append(random.choice(string.ascii_letters+string.digits))
        self.layer.setText(''.join(letters))
        
        if all(self.letters_found):
            self.delay('victory', 0.6, self.victory)
        else:
            self.delay('scramble', 0.1, self.scramble)
    
    def victory(self):
        self.layer.setText('Success!')
        self.game.player().score += 10000
        self.delay('victory', 1, self.victory2)
    
    def victory2(self):
        self.game.modes.remove(self)
    
    def defeat(self):
        if all(self.letters_found):
            return # we didn't lose, it just timed out before the victory sequence fired
        self.game.modes.remove(self)