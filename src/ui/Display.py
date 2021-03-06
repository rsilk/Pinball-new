'''
Created on 2012-02-18

@author: ryan
'''
import pygame
from pygame.locals import *

from .Subdisplay import Subdisplay

class Display:
    W = 1024
    H = 768
    DMD_W = 768
    DMD_H = 576
    
    def __init__(self):
        self.screen = pygame.display.set_mode((self.W, self.H),
                                              pygame.HWSURFACE|pygame.DOUBLEBUF)
                                              #pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
        self.dmd = Subdisplay(self.screen, 1024, 384, 0, 384)
        self.upper = Subdisplay(self.screen, 1024, 384, 0, 0)
        

    def go(self):
        pass
    
    def beginFrame(self):
#        self.screen.fill((0,0,0))
#        self.dmd.clear()
#        self.upper.clear()
        pass
    
    def endFrame(self, dmd_dirty, upper_dirty):
        if dmd_dirty:
            self.screen.blit(self.dmd.surface, dest=(self.dmd.x, self.dmd.y))
        if upper_dirty:
            self.screen.blit(self.upper.surface, dest=(self.upper.x, self.upper.y))
        if dmd_dirty or upper_dirty:
            pygame.display.flip()
