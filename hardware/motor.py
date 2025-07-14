# motor.py
# Copyright (c) 2025 Mohsen Khodaee, Oliver Wigger


import RPi.GPIO as GPIO
import time
import logging as log
import hardware.encoder as encoder
import config as cfg
from hardware import load_cell  

# Control tolerances
FORCE_TOLERANCE = 5       # Newtons
MOMENT_TOLERANCE = 0.2    # Newton-meters
MAX_DURATION = 5          # Max seconds to try applying force/moment

def move_ang(axis, set_angle):
    if encoder.get_angle(cfg.AXIS[axis]) < set_angle:
        mot_pos(axis)
        while encoder.get_angle(cfg.AXIS[axis]) < set_angle:
            pass
        mot_stop(axis)

    elif encoder.get_angle(cfg.AXIS[axis]) > set_angle:
        mot_neg(axis)
        while encoder.get_angle(cfg.AXIS[axis]) > set_angle:
            pass
        mot_stop(axis)
        
def calibrate():
    angle_P = [0, 0, 0]
    angle_N = [0, 0, 0]
    cfg.ENC_ZERO = [0, 0, 0]

    # start
    #led.switch_to("ORANGE")

    # move to "n"-side and measure it
    move_all_time("N", cfg.MOT_T_HOMING)
    encoder.zero()
    for i in range(3):
        angle_N[i] = 0
    log.debug("Angle_N: " + str(angle_N))

    # move to "p"-side and measure it
    move_all_time("P", cfg.MOT_T_HOMING)
    time.sleep(0.2)
    for i in range(3):
        angle_P[i] = encoder.get_angle(i)
        if angle_P[i] < 28.0:
            log.error("Encoder slippage detected!")
        
    log.debug("Angle_P: " + str(angle_P))
    

    # calculate middle
    for i in range(3):
        cfg.ENC_ZERO[i] = angle_N[i] + (abs(angle_P[i] - angle_N[i]) / 2)

    # move to neutral position
    move_to_pos([0, 0, 0])

    # finish
    #led.switch_to("GREEN")
    log.info("Motor Homing DONE")
    log.info("               ")

def move_to_pos(pos):
    x, y, z = pos
    set_angle = [x, y, z]
    axis_on = [0, 0, 0]
    axis_str = ["X", "Y", "Z"]

    # start to move the motors accordingly
    for i in range(3):
        if set_angle[i] - encoder.get_angle(i) > 0.3:
            mot_pos(axis_str[i])

        elif set_angle[i] - encoder.get_angle(i) < -0.3:
            mot_neg(axis_str[i])

        axis_on[i] = 1

    n_moving = sum(axis_on)

    # stop to move the motors accordingly
    while n_moving > 0:
        for i in range(3):
            if axis_on[i] and abs(encoder.get_angle(i) - set_angle[i]) < 0.1:
                mot_stop(axis_str[i])
                axis_on[i] = 0

        n_moving = sum(axis_on)


def init():
    #GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    
    # Setup motor pins
    GPIO.setup(cfg.MOT["XP"], GPIO.OUT)
    GPIO.setup(cfg.MOT["XN"], GPIO.OUT)
    GPIO.setup(cfg.MOT["YP"], GPIO.OUT)
    GPIO.setup(cfg.MOT["YN"], GPIO.OUT)
    GPIO.setup(cfg.MOT["ZP"], GPIO.OUT)
    GPIO.setup(cfg.MOT["ZN"], GPIO.OUT)

    stop_all()
    log.info("Motor GPIO initialized.")


def mot_pos(axis):
    """Turn on motor in positive direction"""
    GPIO.output(cfg.MOT[axis + "P"], 1)
    GPIO.output(cfg.MOT[axis + "N"], 0)


def mot_neg(axis):
    """Turn on motor in negative direction"""
    GPIO.output(cfg.MOT[axis + "P"], 0)
    GPIO.output(cfg.MOT[axis + "N"], 1)


def mot_stop(axis):
    """Turn off both directions for a motor"""
    GPIO.output(cfg.MOT[axis + "P"], 0)
    GPIO.output(cfg.MOT[axis + "N"], 0)


def stop_all():
    """Stop all motors"""
    for axis in cfg.AXIS:
        mot_stop(axis)
    log.info("All motors stopped.")
    
def move_all_time(dir, move_time):
    log.debug("Move all Axis " + dir + " for " + str(move_time) + " seconds.")
    GPIO.output(cfg.MOT["X" + dir], 1)
    GPIO.output(cfg.MOT["Y" + dir], 1)
    GPIO.output(cfg.MOT["Z" + dir], 1)
    time.sleep(move_time)
    GPIO.output(cfg.MOT["X" + dir], 0)
    GPIO.output(cfg.MOT["Y" + dir], 0)
    GPIO.output(cfg.MOT["Z" + dir], 0)   
    

# this part bz me
def apply_force(axis, target_force):
    """
    Apply force along an axis (X, Y, Z) until target_force is reached.
    """
    idx = cfg.AXIS[axis]
    start_time = time.time()

    while True:
        fx, fy, fz = load_cell.get_forces()
        force = [fx, fy, fz][idx]
        error = target_force - force

        if abs(error) <= FORCE_TOLERANCE:
            mot_stop(axis)
            log.info(f"Force {axis}: Target {target_force}N reached.")
            break

        if error > 0:
            mot_pos(axis)
        else:
            mot_neg(axis)

        time.sleep(0.05)
        mot_stop(axis)

        if time.time() - start_time > MAX_DURATION:
            log.warning(f"Force {axis}: Max duration reached. Stopping.")
            mot_stop(axis)
            break


def apply_moment(axis, target_moment):
    """
    Apply moment around an axis (X, Y, Z) until target_moment is reached.
    """
    idx = cfg.AXIS[axis]
    start_time = time.time()

    while True:
        mx, my, mz = load_cell.get_moments()
        moment = [mx, my, mz][idx]
        error = target_moment - moment

        if abs(error) <= MOMENT_TOLERANCE:
            mot_stop(axis)
            log.info(f"Moment {axis}: Target {target_moment}Nm reached.")
            break

        if error > 0:
            mot_pos(axis)
        else:
            mot_neg(axis)

        time.sleep(0.05)
        mot_stop(axis)

        if time.time() - start_time > MAX_DURATION:
            log.warning(f"Moment {axis}: Max duration reached. Stopping.")
            mot_stop(axis)
            break
