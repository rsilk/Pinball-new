'''
Created on 2012-04-07

@author: Ryan
'''
import pygame
from pygame.locals import *

class Subdisplay:
    def __init__(self, display, width, height, x, y):
        self.display = display
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.border_rect = pygame.Rect(0,0, self.width, self.height)
        self.surface = pygame.Surface((width, height))
    
    def clear(self):
        self.surface.fill((0,0,0))
    
    def blit(self, *args, **kwargs):
#        pygame.draw.rect(self.surface, (255,255,255), self.border_rect, 1)
        return self.surface.blit(*args, **kwargs)