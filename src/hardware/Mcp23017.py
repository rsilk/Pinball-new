'''
Created on 2013-06-11

@author: ryan
'''

# pin states
ON = 1
OFF = 0
INPUT = 1

# registers
IODIRA = 0x0 # IO direction - 1 means input (default 11111111)
IODIRB = 0x1 # IO direction - 1 means input (default 11111111)
IPOLA = 0x2 # input polarity - 1 means input will be inverted
IPOLB = 0x3
GPINTENA = 0x4 # interrupt-on-change enable - 1 means enabled
GPINTENB = 0x5
DEFVALA = 0x6 # default value (use for int-on-change comparison)
DEFVALB = 0x7
INTCONA = 0x8 # interrupt control - if 1, compare pin against DEFVAL. if 0, compare against previous value
INTCONB = 0x9
IOCON = 0xA # (BANK MIRROR SEQOP DISSLW HAEN ODR INTPOL -)
IOCON2 = 0xB # alias for above (both addresses access IOCON)
GPPUA = 0xC # pull-up configuration - 1 means enable 100k pullup
GPPUB = 0xD
INTFA = 0xE # interrupt flag - reads 1 for pin(s) that caused interrupt
INTFB = 0xF
INTCAPA = 0x10 # interrupt capture - captures input state when interrupt occurred
INTCAPB = 0x11
GPIOA = 0x12 # GPIO - reads from the port. writing writes to OLAT
GPIOB = 0x13
OLATA = 0x14 # output latch
OLATB = 0x15

class Mcp23017(object):
    '''
    Usage:
    
    setPinValue(pin, val)
    ...
    update()
    ...
    getPinValue(pin)
    '''


    def __init__(self, bus, address, default_pin_state=INPUT):
        '''
        Constructor
        '''
        self.bus = bus # smbus.bus object
        self.address = address # hex address
        self.default_pin_state = default_pin_state
        self.pullups_enabled = True
        self.output_states = 0b0000000000000000
        self.directions = 0b0000000000000000
        self.pullups_enabled = 0b1111111111111111
        self.last_read_values = 0b1111111111111111
        
        self.reset()

    def shutdown(self):
        self.reset()
    
    def reset(self):
        if self.default_pin_state == INPUT:
            self.directions = 0b1111111111111111
            self.output_states = 0b1111111111111111
        elif self.default_pin_state == ON:
            self.directions = 0b0000000000000000
            self.output_states = 0b1111111111111111
        else:
            self.directions = 0b0000000000000000
            self.output_states = 0b0000000000000000
        
        self.pullups_enabled = 0b1111111111111111
            
        self.bus.write_byte_data(self.address, IODIRA, self.directions & 0x00FF)
        self.bus.write_byte_data(self.address, IODIRB, (self.directions & 0xFF00) >> 8)
        
        self.bus.write_byte_data(self.address, GPIOA, self.output_states & 0x00FF)
        self.bus.write_byte_data(self.address, GPIOB, (self.output_states & 0xFF00) >> 8)
        
        self.bus.write_byte_data(self.address, GPPUA, self.pullups_enabled & 0x00FF)
        self.bus.write_byte_data(self.address, GPPUB, (self.pullups_enabled & 0xFF00) >> 8)
        
        # initialize all pins to default
        self.update()
    
    def setPinValue(self, pin, value):
        if value:
            mask = 1 << pin
            self.state = self.state | mask
        else:
            mask = ~(1 << pin)
            self.state = self.state & mask
            
    def getPinValue(self, pin):
        mask = 1 << pin
        return bool(self.last_read_values & mask)
    
    def update(self):
        # set value
        self.bus.write_byte_data(self.address, GPIOA, self.output_states & 0x00FF)
        self.bus.write_byte_data(self.address, GPIOB, (self.output_states & 0xFF00) >> 8)
        
        # then read back value
        gpio1 = self.bus.read_byte_data(self.address, GPIOA)
        gpio2 = self.bus.read_byte_data(self.address, GPIOB)
        
        self.last_read_values = gpio1 | (gpio2 << 8)
    
    def setAll(self, values):
        pass # TODO

if __name__ == '__main__':
    print "1+1 = %s" % bin(0b1+0b1)
    p = Mcp23017(None, 1, INPUT)
    print "pin0"
    print p.getPinValue(0)
    p.setPinValue(0, OFF)
    p.update()
    print p.getPinValue(0)
    
    
    print "pin5"
    print p.getPinValue(5)
    p.setPinValue(5, OFF)
    p.update()
    print p.getPinValue(5)
    
    print "pin15"
    print p.getPinValue(15)
    p.setPinValue(15, OFF)
    p.update()
    print p.getPinValue(15)
