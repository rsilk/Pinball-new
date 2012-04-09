'''
Created on 2012-02-19

@author: ryan
'''

import pygame

pygame.font.init()

TITLE_FONT = pygame.font.SysFont('Upheaval Pro', 100)
BIG_FONT = pygame.font.SysFont('Upheaval Pro', 48)
SMALL_FONT = pygame.font.SysFont('Joystix', 14)
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