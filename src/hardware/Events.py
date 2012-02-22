'''
Created on 2012-02-19

@author: ryan
'''
import pygame
from pygame.locals import *

class EventTypes:
    QUIT = 0

class QuitEvent:
    TYPE = EventTypes.QUIT



class Events:
    def __init__(self):
        pass
    
    def getPygameEvents(self):
        events = []
        for event in pygame.event.get():
            if event.type == QUIT:
                events.append(QuitEvent())
        return events
    
    def getHardwareEvents(self):
        return []
    
    def getEvents(self):
        events = self.getPygameEvents()
        events.extend(self.getHardwareEvents())
        return events