'''
Created on 2012-02-18

@author: ryan
'''
import pygame
from pygame.locals import *

class Display:
    
    def __init__(self):
        self.screen = pygame.display.set_mode((800,600))

    def go(self):
        pass
    
    def beginFrame(self):
        self.screen.fill((0,0,0))
    
    def endFrame(self):
        pygame.display.flip()