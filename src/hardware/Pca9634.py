'''
Created on 2013-03-24

@author: ryan
'''
import smbus

# registers
MODE1 = 0x0
MODE2 = 0x1
PWM0 = 0x2
PWM1 = 0x3
PWM2 = 0x4
PWM3 = 0x5
PWM4 = 0x6
PWM5 = 0x7
PWM6 = 0x8
PWM7 = 0x9
GRPPWM = 0xA
GRPFREQ = 0xB
LEDOUT0 = 0xC
LEDOUT1 = 0xD
SUBADR1 = 0xE
SUBADR2 = 0xF
SUBADR3 = 0x10
ALLCALLADR = 0x11

class Pca9634(object):
    '''
    classdocs
    '''


    def __init__(self, bus, address):
        '''
        Constructor
        '''
        self.bus = bus # smbus.bus object
        self.address = address # hex address
        self.reset()
    
    def reset(self):
        mode1 = 0b00000001
        mode2 = 0b00001000
    
        # initialize mode1, mode2
        self.bus.write_byte_data(self.address, MODE1, mode1)
        self.bus.write_byte_data(self.address, MODE2, mode2)
    
        # turn on brightness control
        self.bus.write_byte_data(self.address, LEDOUT0, 0b10101010)
        self.bus.write_byte_data(self.address, LEDOUT1, 0b10101010)
    
        # turn off all the leds
        for i in range(8):
            self.bus.write_byte_data(self.address, PWM0+i, 0)
    
    def setValue(self, led, value):
        self.bus.write_byte_data(self.address, PWM0+led, self.brightness)
    
    def setAll(self, values):
        pass # TODO