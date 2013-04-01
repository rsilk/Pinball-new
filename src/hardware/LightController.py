'''
Created on 2013-03-24

@author: ryan
'''
try:
    import smbus
    from .Pca9634 import Pca9634
    _HW_ENABLED = True
except ImportError:
    _HW_ENABLED = False
    
class LightController(object):
    def __init__(self, lights):
        if not _HW_ENABLED:
            return
        self.bus = smbus.SMBus(0)
        self.lights = lights
        
        self.devices = [Pca9634(self.bus, 0x3f)]

    def shutdown(self):
        if not _HW_ENABLED:
            return
        for device in self.devices:
            device.shutdown()
    
    def update(self):
        if not _HW_ENABLED:
            return
        
        for light in self.lights:
            try:
                r_dev = self.devices[light.deviceR]
                r_dev.setValue(light.offsetR, light.r)
                g_dev = self.devices[light.deviceG]
                g_dev.setValue(light.offsetG, light.g)
                b_dev = self.devices[light.deviceB]
                b_dev.setValue(light.offsetB, light.b)
            except IndexError:
                continue # no device for that light
