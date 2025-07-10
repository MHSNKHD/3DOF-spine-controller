# init.py
# Copyright (c) 2025 Mohsen Khodaee, Oliverwigger

from hardware import encoder
from hardware import fogger
#from hardware import led
from hardware import motor
#from hardware import instron


def init():
    #led.init()
    motor.init()
    #instron.init()
    encoder.init()
    fogger.init()
    #led.switch_to("GREEN")
    motor.stop_all()