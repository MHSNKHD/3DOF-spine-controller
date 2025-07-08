# motor.py
# Copyright (c) 2025 Mohsen Khodaee, Oliver Wigger


import RPi.GPIO as GPIO
import time
import logging as log

import config as cfg
from hardware import load_cell  # or hardware.load_cell depending on your structure

# Control tolerances
FORCE_TOLERANCE = 5       # Newtons
MOMENT_TOLERANCE = 0.2    # Newton-meters
MAX_DURATION = 5          # Max seconds to try applying force/moment


def init():
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
