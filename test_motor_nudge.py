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
GPIO.cleanup()
