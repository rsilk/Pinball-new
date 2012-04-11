'''
Created on 2012-04-08

@author: Ryan
'''
import pygame
from pygame.locals import *
import time

class DisplayLayer:
    # Show only the first frame all the time
    def __init__(self, frames):
        self.x = 0
        self.y = 0
        self.frames = frames
        self.operation = 'blit'
        self.opaque = False # if True, none of the layers below this will be drawn
    
    def move(self, x, y):
        self.x = x
        self.y = y
    
    def frame(self, delta):
        return self.frames[0]
    
    def drawOnto(self, target, delta):
        target.blit(self.frame(delta), (self.x, self.y))

class ImageLayer(DisplayLayer):
    # Convenience class - show a static image
    def __init__(self, path):
        image = pygame.image.load(path)
        DisplayLayer.__init__(self, [image])
    
    
class TextLayer(DisplayLayer):
    # Convenience class - show static text
    def __init__(self, font, text, color, align=None, antialias=False):
        DisplayLayer.__init__(self, [])
        self.align = align or 'left' # or 'center' or 'right'
        self.font = font
        self.color = color
        self.aa = antialias
        self.set_x = self.x
        self.set_y = self.y
        self.text = None
        self.setText(text)
    
    def setText(self, text):
        if text == self.text:
            return
        self.text = text
        text_surf = self.font.render(text, self.aa, self.color)
        self.frames = [text_surf]
        self.move(self.set_x, self.set_y)
    
    def move(self, x, y):
        self.set_x = x
        self.set_y = y
        self.y = y
        
        if self.align == 'left':
            self.x = self.set_x
        elif self.align == 'center':
            self.x = self.set_x - self.width()/2
        elif self.align == 'right':
            self.x = self.set_x - self.width()
    
    def width(self):
        return self.frames[0].get_width()

class AnimationLayer(DisplayLayer):
    # Display a sequence of frames
    def __init__(self, frames, delay):
        DisplayLayer.__init__(self, frames)
        self.delay = delay
        self.current_frame = 0
        self.time_until_next_frame = delay
    
    def frame(self, delta):
        self.time_until_next_frame -= delta
        if self.time_until_next_frame <= 0:
            self.current_frame += 1
            self.current_frame %= len(self.frames)
            self.time_until_next_frame += self.delay
        return self.frames[self.current_frame]


class GroupedLayer(DisplayLayer):
    # Group a set of layers into one logical layer
    def __init__(self, layers):
        DisplayLayer.__init__(self, None)
        self.layers = layers
    
    def frame(self, delta):
        group_rect = pygame.Rect(0,0,0,0)
        
        frames = [layer.frame(delta) for layer in self.layers]
        for frame, layer in zip(frames, self.layers):
            rect = frame.get_rect()
            rect.move_ip(layer.x, layer.y)
            group_rect.union_ip(rect)
         
        surf = pygame.Surface((group_rect.width, group_rect.height), SRCALPHA)
        for frame, layer in zip(frames, self.layers):
            surf.blit(frame, (layer.x, layer.y)) # TODO: compositing
        return surf
    
    def drawOnto(self, target, delta):
        for layer in self.layers:
            frame = layer.frame(delta)
            target.blit(frame, (self.x+layer.x, self.y+layer.y))


class MotionEffect(DisplayLayer):
    # Pan a layer
    def __init__(self, layer, dx, dy):
        # dx: change in X direction (pixels/second)
        # dy: change in Y direction (pixels/second)
        DisplayLayer.__init__(self, None)
        self.dx = dx
        self.dy = dy
        self.layer = layer
    
    def frame(self, delta):
        new_x = self.x + self.dx*delta
        new_y = self.y + self.dy*delta
        self.move(new_x, new_y)
        return self.layer.frame(delta)

class FadeEffect(DisplayLayer):
    # Fade a layer in or out (alpha)
    # 0 = fully transparent, 255 = fully opaque
    def __init__(self, layer, starting_alpha, da):
        # da: change in alpha per second
        DisplayLayer.__init__(self, None)
        self.da = da
        self.alpha = starting_alpha
        self.layer = layer
    
    def frame(self, delta):
        self.alpha += self.da*delta
        surf = self.layer.frame(delta).copy()
        surf.set_alpha(self.alpha)
        return surf