# test_motor_direction.py
import time
import config as cfg
from hardware import motor

motor.init()

print("Testing X+")
motor.mot_pos("X")
time.sleep(1)
motor.mot_stop("X")

time.sleep(1)

print("Testing X-")
motor.mot_neg("X")
time.sleep(1)
motor.mot_stop("X")

motor.stop_all()