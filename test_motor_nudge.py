# Copyright (c) 2025 Mohsen Khodaee

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


# Test X motor
GPIO.setup(24, GPIO.OUT)  # XP 
GPIO.setup(23, GPIO.OUT)  # XN 


# Wait before starting
time.sleep(1)

# Positive
GPIO.output(24,1)
GPIO.output(23,0)
time.sleep(1)
GPIO.output(24,0)
time.sleep(1) 

#Negative
GPIO.output(24, 0)
GPIO.output(23, 1)
time.sleep(1)
GPIO.output(23, 0)

# Stop motor
GPIO.output(23, 0)

# Test Y motor

GPIO.setup(4, GPIO.OUT)   # YP
GPIO.setup(14, GPIO.OUT)  # YN

# Positive
GPIO.output(4, 1)
GPIO.output(14, 0)
time.sleep(1)
GPIO.output(4, 0)
time.sleep(1)

# Negative
GPIO.output(4, 0)
GPIO.output(14, 1)
time.sleep(1)
GPIO.output(14, 0)


# Test Z motor

GPIO.setup(27, GPIO.OUT)   # ZP
GPIO.setup(15, GPIO.OUT)  # ZN

# Positive
GPIO.output(27, 1)
GPIO.output(15, 0)
time.sleep(1)
GPIO.output(27, 0)
time.sleep(1)

# Negative
GPIO.output(27, 0)
GPIO.output(15, 1)
time.sleep(1)
GPIO.output(15, 0)

GPIO.cleanup()
