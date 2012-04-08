'''
Created on 2012-04-07

@author: Ryan
'''
import ui.fonts
import pygame
from game.modes.Mode import Mode
from hardware.Events import *

class TestDisplayMode(Mode):
    
    def __init__(self, *args):
        Mode.__init__(self, *args)
        
        self.switch_clicked = None
        
        upper_display = self.game.display.upper
        self.surface = pygame.Surface((upper_display.width, upper_display.height))
        for switch in self.game.switches.values():
            surf = ui.fonts.TEST_DISPLAY_FONT.render(switch.name, True, (255,255,255))
            self.surface.blit(surf, (switch.x, switch.y))
        
        for light in self.game.lights.values():
            surf = ui.fonts.TEST_DISPLAY_FONT.render(light.name, True, (255,255,255))
            self.surface.blit(surf, (light.x, light.y))
    
    def event(self, event):
        if event.TYPE == EventTypes.MOUSE_DOWN:
            # check to see if a switch label was clicked
            for switch in self.game.switches.values():
                sw_rect = pygame.Rect(switch.x, switch.y, 30, 10)
                if sw_rect.collidepoint(event.pos):
                    print "clicked %s" % switch.name
                    self.switch_clicked = switch
                    self.game.events.inject(SwitchClosedEvent(switch))
        elif event.TYPE == EventTypes.MOUSE_UP:
            if self.switch_clicked:
                print "released %s" % self.switch_clicked.name
                self.game.events.inject(SwitchOpenEvent(self.switch_clicked))
                self.switch_clicked = None
    
    def frame(self, delta):
        game_upper_display = self.game.display.upper
        game_upper_display.blit(self.surface, (0,0))
        
        fps = 1/delta
        fps_surf = ui.fonts.TEST_DISPLAY_FONT.render('%0.2d FPS' % fps, True, (255,255,255))
        game_upper_display.blit(fps_surf, (950,10))
        
        for light in self.game.lights.itervalues():
            pygame.draw.rect(game_upper_display.surface, (light.r, light.g, light.b), (light.x-12, light.y+1, 10, 10))
