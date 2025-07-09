import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)  # XP
GPIO.setup(23, GPIO.OUT)  # XN

print("Positive direction")
GPIO.output(24, 1)
GPIO.output(23, 0)
time.sleep(1)
GPIO.output(24, 0)

time.sleep(1)

print("Negative direction")
GPIO.output(24, 0)
GPIO.output(23, 1)
time.sleep(1)
GPIO.output(23, 0)

GPIO.cleanup()