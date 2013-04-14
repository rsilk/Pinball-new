'''
Created on 2012-02-19

@author: ryan
'''

import pygame
import os.path
pygame.font.init()

def _findFont(filename):
    path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', filename))
    return path

TITLE_FONT = pygame.font.Font(_findFont('UpheavalPro.ttf'), 100)
BIG_FONT = pygame.font.Font(_findFont('UpheavalPro.ttf'), 48)
SMALL_FONT = pygame.font.Font(_findFont('UpheavalPro.ttf'), 25)
TEST_DISPLAY_FONT = pygame.font.SysFont('Arial', 12)

def renderLines(font, lines, antialias, color, background=None):
    fontHeight = font.get_height()

    surfaces = [font.render(ln, antialias, color) for ln in lines]
    # can't pass background to font.render, because it doesn't respect the alpha

    maxwidth = max([s.get_width() for s in surfaces])
    result = pygame.Surface((maxwidth, len(lines)*fontHeight), pygame.SRCALPHA)
    if background == None:
        result.fill((90,90,90,0))
    else:
        result.fill(background)

    for i in range(len(lines)):
        result.blit(surfaces[i], (0,i*fontHeight))
    return result
