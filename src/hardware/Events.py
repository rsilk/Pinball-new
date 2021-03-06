'''
Created on 2012-02-19

@author: ryan
'''
import pygame
from pygame.locals import *

class EventTypes:
    QUIT = 0
    MOUSE_DOWN = 1
    MOUSE_UP = 2
    SWITCH_CLOSED = 3
    SWITCH_OPEN = 4
    MOUSE_MOVE = 5

class QuitEvent:
    TYPE = EventTypes.QUIT

class MouseDownEvent:
    TYPE = EventTypes.MOUSE_DOWN
    
    def __init__(self, pos, button):
        self.pos = pos
        self.button = button

class MouseUpEvent:
    TYPE = EventTypes.MOUSE_UP
    
    def __init__(self, pos, button):
        self.pos = pos
        self.button = button

class MouseMoveEvent:
    TYPE = EventTypes.MOUSE_MOVE
    
    def __init__(self, pos):
        self.pos = pos

class SwitchClosedEvent:
    TYPE = EventTypes.SWITCH_CLOSED
    
    def __init__(self, switch):
        self.switch = switch

class SwitchOpenEvent:
    TYPE = EventTypes.SWITCH_OPEN
    
    def __init__(self, switch):
        self.switch = switch


class Events:
    def __init__(self):
        self.queued_emulated_events = []
    
    def inject(self, event):
        self.queued_emulated_events.append(event)
    
    def setIOController(self, io_controller):
        self.io_controller = io_controller
    
    def getPygameEvents(self):
        events = []
        for event in pygame.event.get():
            if event.type == QUIT:
                events.append(QuitEvent())
            elif event.type == MOUSEBUTTONDOWN:
                events.append(MouseDownEvent(event.pos, event.button))
            elif event.type == MOUSEBUTTONUP:
                events.append(MouseUpEvent(event.pos, event.button))
            elif event.type == MOUSEMOTION:
                events.append(MouseMoveEvent(event.pos))
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    events.append(QuitEvent())
        return events
    
    def getEvents(self):
        events = self.getPygameEvents()
        events.extend(self.io_controller.getSwitchEvents())
        events.extend(self.queued_emulated_events)
        self.queued_emulated_events = []
        return events