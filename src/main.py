'''
Created on 2012-02-18

@author: ryan
'''
import pygame

from ui.Display import Display
from game.GameMain import GameMain
from hardware.Events import Events

if __name__ == '__main__':
    
    # fire up pygame
    pygame.init()
    
    # bring up UI
    display = Display()
    display.go()
    
    # initialize game objects
    events = Events()
    game = GameMain(display, events)
    
    # start event loop
    game.go()