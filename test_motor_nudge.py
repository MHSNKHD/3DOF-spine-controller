# Copyright (c) 2025 Mohsen Khodaee


import RPi.GPIO as GPIO
import time
from hardware import motor
from hardware import encoder

encoder.init()
motor.calibrate()

# Clean any previous state before beginning
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

# Motor pin list
pins = [24, 23, 4, 14, 27, 15]

# Initialize all pins and force LOW
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Let things settle
time.sleep(5)

# Now test motors (same as before)


# Test X motor
GPIO.setup(24, GPIO.OUT)  # XP 
GPIO.setup(23, GPIO.OUT)  # XN 


# Wait before starting
time.sleep(5)

print("Testing X+")
# Positive
GPIO.output(23,0)
GPIO.output(24,1)
time.sleep(1)
# Stop motor
GPIO.output(24,0)
time.sleep(5) 

print("Testing X-")
#Negative
GPIO.output(24, 0)
GPIO.output(23, 1)
time.sleep(1)

# Stop motor
GPIO.output(23, 0)
time.sleep(5)

# Test Y motor

GPIO.setup(4, GPIO.OUT)   # YP
GPIO.setup(14, GPIO.OUT)  # YN

print("Testing Y+")
# Positive
GPIO.output(14, 0)
GPIO.output(4, 1)
time.sleep(1)
# Stop motor
GPIO.output(4, 0)
time.sleep(5)


print("Testing Y-")
# Negative
GPIO.output(4, 0)
GPIO.output(14, 1)
time.sleep(1)
# Stop motor
GPIO.output(14, 0)
time.sleep(5)


# Test Z motor

GPIO.setup(27, GPIO.OUT)   # ZP
GPIO.setup(15, GPIO.OUT)  # ZN

print("Testing Z+")
# Positive
GPIO.output(15, 0)
GPIO.output(27, 1)
time.sleep(1)
# Stop motor
GPIO.output(27, 0)
time.sleep(5)

print("Testing Z-")
# Negative
GPIO.output(27, 0)
GPIO.output(15, 1)

time.sleep(1)
# Stop motor
GPIO.output(15, 0)
time.sleep(5)

GPIO.cleanup()
