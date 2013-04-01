'''
Created on 2013-03-31

@author: Ryan
'''
try:
    import smbus
    from .Pca9673 import Pca9673
    _HW_ENABLED = True
except ImportError:
    _HW_ENABLED = False

from .Events import SwitchOpenEvent, SwitchClosedEvent
    
class IOController(object):
    '''
    classdocs
    '''

    def __init__(self, drivers, switches):
        '''
        Constructor
        '''
        self.events = []
        if not _HW_ENABLED:
            return
        self.bus = smbus.SMBus(0)
        self.drivers = drivers
        self.switches = switches
        
        self.devices = [Pca9673(self.bus, 0x24)]
    
    def shutdown(self):
        if not _HW_ENABLED:
            return
        for device in self.devices:
            device.shutdown()
    
    def update(self):
        if not _HW_ENABLED:
            return
        
        for driver in self.drivers:
            try:
                dev = self.devices[driver.device]
                dev.setPinValue(driver.offset, driver.active)
            except IndexError:
                continue # no device for that driver
        
        for device in self.devices:
            device.update()
        
        for switch in self.switches:
            try:
                dev = self.devices[switch.device]
            except IndexError:
                continue # no device for that switch
            val = dev.getPinValue(switch.offset)
            if val != switch.active:
                if not val:
                    # pin low = switch closed (pin pulled to ground)
                    event = SwitchClosedEvent(switch)
                else:
                    event = SwitchOpenEvent(switch)
                self.events.append(event)
    
    def getSwitchEvents(self):
        events = self.events
        self.events = []
        return events