'''
Created on 2012-04-16

@author: Ryan
'''
import pygame

class ColorManager(object):
    ''' Class to handle the overall "mood color" of the game '''
    def __init__(self):
        self.set_color = pygame.Color('white')
        self.current_color = self.set_color
        self.transition_time = 0.25 # seconds
    
    def setColor(self, color):
        self.set_color = pygame.Color(color)
    
    def translate(self, *color):
        ''' Translate a color into a mood color. If the color is grayscale
        (r=g=b), multiply it by the mood color. Else pass through the color unchanged.
        '''
        c = pygame.Color(*color)
        r, g, b, a = c.normalize()
        
        if r == g == b:
            cr, cg, cb, ca = self.current_color.normalize()
            r *= cr
            g *= cg
            b *= cb
            return pygame.Color(int(r*255), int(g*255), int(b*255), int(a*255))
        else:
            return c