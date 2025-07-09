# test_motor_direction.py
import time
import config as cfg
from hardware import motor

motor.init()
# Test X axis
print("Testing X+")
motor.mot_pos("X")
time.sleep(0.5)
motor.mot_stop("X")

time.sleep(0.5)

print("Testing X-")
motor.mot_neg("X")
time.sleep(0.5)
motor.mot_stop("X")


# Test Y axis
print("Testing Y+")
motor.mot_pos("Y")
time.sleep(0.5)
motor.mot_stop("Y")

time.sleep(0.5)

print("Testing Y-")
motor.mot_neg("Y")
time.sleep(0.5)
motor.mot_stop("Y")

time.sleep(0.5)

# Test Z axis
print("Testing Z+")
motor.mot_pos("Z")
time.sleep(0.5)
motor.mot_stop("Z")

time.sleep(0.5)

print("Testing Z-")
motor.mot_neg("Z")
time.sleep(0.5)
motor.mot_stop("Z")

motor.stop_all()