'''
Created on 2013-03-24

@author: ryan
'''
#import smbus

# pin states
ON = 1
OFF = 0
INPUT = 1

class Pca9673(object):
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
        self.last_read_values = 0b1111111111111110
        
        self.reset()

    def shutdown(self):
        self.reset()
    
    def reset(self):
        if self.default_pin_state == INPUT:
            self.state = 0b1111111111111111
        else:
            self.state = 0b0000000000000000
    
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
        state0 = self.state & 0x00FF
        state1 = (self.state & 0xFF00) >> 8

        # set value
        self.bus.write_byte_data(self.address, state0, state1)
        
        # then read back value. pass in state0 because read_word_data tries
        # to set a register value, which the chip interprets as setting the first
        # bit. send what the value should be so we don't mess things up.
        self.last_read_values = self.bus.read_word_data(self.address, state0)
    
    def setAll(self, values):
        pass # TODO

if __name__ == '__main__':
    print "1+1 = %s" % bin(0b1+0b1)
    p = Pca9673(None, 1, INPUT)
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
