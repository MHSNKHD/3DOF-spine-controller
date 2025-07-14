# Copyright (c) 2025 Mohsen Khodaee




# # this could help, i took it from oli motor.py
# def calibrate():
#     angle_P = [0, 0, 0]
#     angle_N = [0, 0, 0]
#     cfg.ENC_ZERO = [0, 0, 0]

#     # start
#     led.switch_to("ORANGE")

#     # move to "n"-side and measure it
#     move_all_time("N", cfg.MOT_T_HOMING)
#     encoder.zero()
#     for i in range(3):
#         angle_N[i] = 0
#     log.debug("Angle_N: " + str(angle_N))

#     # move to "p"-side and measure it
#     move_all_time("P", cfg.MOT_T_HOMING)
#     time.sleep(0.2)
#     for i in range(3):
#         angle_P[i] = encoder.get_angle(i)
#         if angle_P[i] < 28.0:
#             log.error("Encoder slippage detected!")
        
#     log.debug("Angle_P: " + str(angle_P))
    

#     # calculate middle
#     for i in range(3):
#         cfg.ENC_ZERO[i] = angle_N[i] + (abs(angle_P[i] - angle_N[i]) / 2)

#     # move to neutral position
#     move_to_pos([0, 0, 0])

#     # finish
#     led.switch_to("GREEN")
#     log.info("Motor Homing DONE")
#     log.info("               ")






import RPi.GPIO as GPIO
import time

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
time.sleep(3)

print("Testing X+")
# Positive
GPIO.output(24,1)
GPIO.output(23,0)
time.sleep(1)
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
GPIO.output(4, 1)
GPIO.output(14, 0)
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
GPIO.output(27, 1)
GPIO.output(15, 0)
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
