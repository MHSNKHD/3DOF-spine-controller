# Test X- (Negative Direction)
# Copyright (c) 2025 Mohsen Khodaee

import RPi.GPIO as GPIO
import time

# Clean up any previous GPIO settings
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

# Set up X motor pins
XP = 24  # Positive direction pin
XN = 23  # Negative direction pin

GPIO.setup(XP, GPIO.OUT)
GPIO.setup(XN, GPIO.OUT)

print("Testing X-axis in NEGATIVE direction")

# Make sure XP is LOW
GPIO.output(XP, 0)

# Set XN HIGH to rotate in negative direction
GPIO.output(XN, 1)
time.sleep(1)  # Rotate for 1 second

# Stop motor
GPIO.output(XN, 0)

# Clean up
GPIO.cleanup()
