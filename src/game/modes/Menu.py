'''
Created on 2012-05-06

@author: Ryan
'''
import pygame
from game.modes.Mode import Mode
from ui.fonts import *
from ui.layers import *

class MenuItem:
    def __init__(self, image_path, text):
        self.image_path = image_path
        self.text = text

class Menu(Mode):
    
    '''
    A menu for player selections. Player scrolls with the flipper buttons,
    selects with start.
    
    When a selection is made, selection_callback will be called, with the index
    of the selected item as an argument.
    '''
    
    IMAGE_SIZE = 250
    DIP_HEIGHT = 25
    BASE_HEIGHT = 10
    
    def __init__(self, game, prio, items, selection_callback=None):
        Mode.__init__(self, game, prio)
        
        assert items
        
        self.items = items
        self.selection_callback = selection_callback
        self.current_item_index = 0
        
        self.middle_item_position = (1024/2 - self.IMAGE_SIZE/2, self.BASE_HEIGHT+self.DIP_HEIGHT*1)
        self.left_item_position = (1024/2 - int(self.IMAGE_SIZE*1.5), self.BASE_HEIGHT+self.DIP_HEIGHT*0)
        self.right_item_position = (1024/2 + int(self.IMAGE_SIZE*0.5), self.BASE_HEIGHT+self.DIP_HEIGHT*0)
        
        self.new_left_item_position = (1024/2 - int(self.IMAGE_SIZE*2.5), self.BASE_HEIGHT-self.DIP_HEIGHT*1)
        self.new_right_item_position = (1024/2 + int(self.IMAGE_SIZE*1.5), self.BASE_HEIGHT-self.DIP_HEIGHT*1)
        
        self._rebuild()
                
        self.addHandler('flipR', 'closed', 0, self.rotateLeft)
        self.addHandler('flipL', 'closed', 0, self.rotateRight)
        self.addHandler('start', 'closed', 0, self.select)
    
    def _rebuild(self):
        self.middle_layer = ImageLayer(self.items[self.current_item_index].image_path)
        self.middle_layer.move(*self.middle_item_position)
        
        if self.current_item_index == 0:
            left_index = len(self.items) - 1
        else:
            left_index = self.current_item_index - 1
        self.left_layer = ImageLayer(self.items[left_index].image_path)
        self.left_layer.move(*self.left_item_position)
        
        if self.current_item_index == len(self.items) - 1:
            right_index = 0
        else:
            right_index = self.current_item_index + 1
        self.right_layer = ImageLayer(self.items[right_index].image_path)
        self.right_layer.move(*self.right_item_position)
        
        self.new_item_layer = None
        
        self.middle_layer.frames[0].set_alpha(255)
        self.left_layer.frames[0].set_alpha(155)
        self.right_layer.frames[0].set_alpha(155)
        
        self.help_layer = TextLayer(SMALL_FONT,
                                    'CHANGE SELECTION WITH FLIPPER BUTTONS. START SELECTS.',
                                    self.game.color(255,255,255), 'center')
        self.help_layer.move(1024/2, 360)
        
        self.layer = GroupedLayer([self.help_layer, self.middle_layer, self.left_layer, self.right_layer])
        
    def rotateLeft(self, sw):
        self.delay('rotate', 0.01, self._interval, 'left', 0)
    
    def rotateRight(self, sw):
        self.delay('rotate', 0.01, self._interval, 'right', 0)
    
    def _interval(self, direction, fraction):
        if self.new_item_layer is None:
            # set the "new" item layer with whatever is 2 from the current index
            if direction == 'left':
                if self.current_item_index == len(self.items) - 2:
                    new_index = 0
                elif self.current_item_index == len(self.items) - 1:
                    new_index = 1
                else:
                    new_index = self.current_item_index + 2
            else:
                if self.current_item_index == 0:
                    new_index = len(self.items) - 2
                else:
                    new_index = self.current_item_index - 1
            self.new_item_layer = ImageLayer(self.items[new_index].image_path)
            self.layer = GroupedLayer([self.help_layer, self.middle_layer, self.left_layer, self.right_layer, self.new_item_layer])
        
        if direction == 'left':
            # move middle item
            x = self.middle_item_position[0] - (self.middle_item_position[0] - self.left_item_position[0]) * fraction
            y = self.BASE_HEIGHT+self.DIP_HEIGHT*(1-fraction)
            alpha = 255 - int(100*fraction)
            self.middle_layer.move(x, y)
            self.middle_layer.frames[0].set_alpha(alpha)
            
            # move left item
            x = self.left_item_position[0] - (self.middle_item_position[0] - self.left_item_position[0]) * fraction
            y = self.BASE_HEIGHT-self.DIP_HEIGHT*fraction
            alpha = int(155*(1-fraction))
            self.left_layer.move(x, y)
            self.left_layer.frames[0].set_alpha(alpha)
            
            # move right item
            x = self.right_item_position[0] - (self.right_item_position[0] - self.middle_item_position[0]) * fraction
            y = self.BASE_HEIGHT+self.DIP_HEIGHT*fraction
            alpha = 155 + int(100*fraction)
            self.right_layer.move(x, y)
            self.right_layer.frames[0].set_alpha(alpha)
            
            # move the "new" item in from the right
            x = self.new_right_item_position[0] - (self.right_item_position[0] - self.middle_item_position[0]) * fraction
            y = self.BASE_HEIGHT-self.DIP_HEIGHT*(1-fraction)
            alpha = int(155*fraction)
            self.new_item_layer.move(x, y)
            self.new_item_layer.frames[0].set_alpha(alpha)
        else:
            # move middle item
            x = self.middle_item_position[0] + (self.right_item_position[0] - self.middle_item_position[0]) * fraction
            y = self.BASE_HEIGHT+self.DIP_HEIGHT*(1-fraction)
            alpha = 255 - int(100*fraction)
            self.middle_layer.move(x, y)
            self.middle_layer.frames[0].set_alpha(alpha)
            
            # move left item
            x = self.left_item_position[0] + (self.middle_item_position[0] - self.left_item_position[0]) * fraction
            y = self.BASE_HEIGHT+self.DIP_HEIGHT*fraction
            alpha = 155 + int(100*fraction)
            self.left_layer.move(x, y)
            self.left_layer.frames[0].set_alpha(alpha)
            
            # move right item
            x = self.right_item_position[0] + (self.right_item_position[0] - self.middle_item_position[0]) * fraction
            y = self.BASE_HEIGHT-self.DIP_HEIGHT*fraction
            alpha = int(155*(1-fraction))
            self.right_layer.move(x, y)
            self.right_layer.frames[0].set_alpha(alpha)
            
            # move the "new" item in from the left
            x = self.new_left_item_position[0] + (self.right_item_position[0] - self.middle_item_position[0]) * fraction
            y = self.BASE_HEIGHT-self.DIP_HEIGHT*(1-fraction)
            alpha = int(155*fraction)
            self.new_item_layer.move(x, y)
            self.new_item_layer.frames[0].set_alpha(alpha)
        
        
        if fraction < 1:
            self.delay('rotate', 0.01, self._interval, direction, fraction+0.1)
        else:
            # done animating
            if direction == 'left':
                if self.current_item_index == len(self.items) - 1:
                    self.current_item_index = 0
                else:
                    self.current_item_index += 1
                
            else:
                if self.current_item_index == 0:
                    self.current_item_index = len(self.items) - 1
                else:
                    self.current_item_index -= 1
            self._rebuild()
    
    def select(self, sw):
        # call callback, then remove self from mode stack
        if self.selection_callback:
            self.selection_callback(self.current_item_index)
        self.game.modes.remove(self)