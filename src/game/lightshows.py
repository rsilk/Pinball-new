'''
Created on 2013-05-03

@author: rsilk
'''
import math
import pygame
import colorsys

MAX_X = 722
MAX_Y = 349

class Fade:
    def __init__(self, lights, period):
        self.lights = lights
        self.period = period
        self.current = 0
    
    def frame(self, delta):
        self.current += delta
        self.current %= self.period
        value = int((math.sin(self.current/self.period*math.pi*2) / 2.0 + 0.5) * 255)
        
        color = pygame.Color(value, value, value)
        
        for light in self.lights:
            light.on(color)

class Rainbow:
    def __init__(self, lights, period):
        self.lights = lights
        self.period = period
        self.current = 0
    
    def frame(self, delta):
        self.current += delta
        self.current %= self.period
        offset = 1 - self.current/self.period
        
        for light in self.lights:
            h = (light.x/float(MAX_X) + offset) % 1
            s = 1.0
            v = 1.0
            r,g,b = colorsys.hsv_to_rgb(h, s, v)
            
            color = pygame.Color(int(r*255),int(g*255),int(b*255))
            
            light.on(color)

class Searchlight:
    def __init__(self, lights, period):
        self.lights = lights
        self.period = period
        self.current = 0
        self.max_distance = 75.0
    
    def frame(self, delta):
        self.current += delta
        self.current %= self.period
        ratio = self.current/self.period
        
        center_x = MAX_X * ratio
        center_y = MAX_Y / 2.0
        
        for light in self.lights:
            distance = math.sqrt(abs((light.x - center_x)*(light.x - center_x) + (light.y - center_y)*(light.y - center_y)))
            if distance > self.max_distance:
                value = 0
            else:
                value = int(distance/self.max_distance*255)
            
            color = pygame.Color(value, value, value)
            
            light.on(color)