# test_motor_nudge.py
# Copyright (c) 2025 Mohsen Khodaee

import config as cfg
import RPi.GPIO as GPIO
import time
from hardware import motor
from hardware import encoder

# === Initialize GPIO mode FIRST ===
GPIO.setmode(GPIO.BCM)

# === Initialize encoder and motor ===
encoder.init()
motor.init()

# === Calibrate motors ===
motor.calibrate()

# === Test motor directions ===
# Define motor test routine
def test_motor(pin_pos, pin_neg, label):
    print(f"Testing {label}+")
    GPIO.output(pin_neg, 0)
    GPIO.output(pin_pos, 1)
    time.sleep(1)
    GPIO.output(pin_pos, 0)
    time.sleep(2)

    print(f"Testing {label}-")
    GPIO.output(pin_pos, 0)
    GPIO.output(pin_neg, 1)
    time.sleep(1)
    GPIO.output(pin_neg, 0)
    time.sleep(2)

# Initialize all motor pins
pins = [24, 23, 4, 14, 27, 15]
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Test X
test_motor(24, 23, "X")
# Test Y
test_motor(4, 14, "Y")
# Test Z
test_motor(27, 15, "Z")

# Cleanup
GPIO.cleanup()