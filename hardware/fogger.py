# fogger.py
# oliverwigger

import RPi.GPIO as GPIO
import config as cfg
import threading as th
import logging as log

IS_AUTO_FOGGER_ON = 0


def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(cfg.FOG["PIN"], GPIO.OUT)
    GPIO.output(cfg.FOG["PIN"], 0)


def auto_fogger_start():
    IS_AUTO_FOGGER_ON = 1
    _auto_fog_on()


def auto_fogger_stop():
    IS_AUTO_FOGGER_ON = 0
    log.debug("fogger stopped")


def _auto_fog_on():
    if IS_AUTO_FOGGER_ON:
        fog_on()
        S = th.Timer(cfg.FOG["ON_TIME"], _auto_fog_off)
        S.setName("t_fog_ON")
        S.start()


def _auto_fog_off():
    fog_off()
    S = th.Timer(cfg.FOG["OFF_TIME"], _auto_fog_on)
    S.setName("t_fog_OFF")
    S.start()


def fog_on():
    GPIO.output(cfg.FOG["PIN"], 1)


def fog_off():
    GPIO.output(cfg.FOG["PIN"], 0)