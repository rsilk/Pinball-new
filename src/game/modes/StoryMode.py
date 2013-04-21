'''
Created on 2013-04-14

@author: ryan
'''
from .Mode import Mode
from ui.layers import GroupedLayer, ImageLayer, TextLayer, AnimatedTextLayer
import ui.fonts

class StoryMode(Mode):
    '''
    classdocs
    '''
    MODE_NAME = 'Mode template'
    MODE_DESC = 'Shoot some stuff'

    def __init__(self, game, prio, scoop_mode):
        '''
        Base class for the 6 main "story" modes
        '''
        Mode.__init__(self, game, prio)
        self.scoop_mode = scoop_mode
    
    def top(self):
        Mode.top(self)
        self.introduce()
    
    def introduce(self):
        # introduce the mode with sound and an intro animation
        map_layer = ImageLayer(self.game.datapath('map_background.png'))
        title_layer = AnimatedTextLayer(ui.fonts.TITLE_FONT,
                                self.MODE_NAME, 
                                self.game.color(255,255,255), align='center')
        title_layer.move(1024/2, 50)
        description_layer = TextLayer(ui.fonts.BIG_FONT,
                                self.MODE_DESC, 
                                self.game.color(255,255,255), align='center')
        description_layer.move(1024/2, 175)
        self.layer = GroupedLayer([map_layer, title_layer, description_layer])
        self.layer.opaque = True
        self.delay('end_intro', 3, self.endIntroduce)
    
    def endIntroduce(self):
        print "end introduce"
        self.layer = None
        self.start()
        self.scoop_mode.ejectBall()
    
    def start(self):
        pass