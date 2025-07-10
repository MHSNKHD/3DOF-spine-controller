import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Set up both motor pins
GPIO.setup(24, GPIO.OUT)  # XP (must be LOW)
GPIO.setup(23, GPIO.OUT)  # XN (we'll set HIGH)

# Wait before starting
time.sleep(1)

print("Testing negative direction (X-)")

# XP LOW, XN HIGH = Negative rotation
GPIO.output(24, 0)
GPIO.output(23, 1)

time.sleep(1)  # Rotate for 1 second

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
