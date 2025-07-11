# load_cell.py
# Copyright (c) 2025 Mohsen Khodaee, Oliver Wigger

import hardware.load_cell_bota as load_cell_bota
import config as cfg
import logging as log
import time
from gui import processFrame
import tkinter as tk

lc = None

def start():
    global lc
    
    try:
        lc = load_cell_bota.BotaSerialSensor(cfg.LC["PORT"])
        lc.start()
        log.info("LoadCell started")
        processFrame.bt_homing.config(state=tk.NORMAL, bg=cfg.COL["en"])
    except:
        print("error")
        log.error("LoadCell FAILED")
        
    lc._fx0.value = cfg.LC0F[0]
    lc._fy0.value = cfg.LC0F[1]
    lc._fz0.value = cfg.LC0F[2]
    
    lc._tx0.value = cfg.LC0T[0]
    lc._ty0.value = cfg.LC0T[1]
    lc._tz0.value = cfg.LC0T[2]
    
def stop():
    lc.stop()

def zero():
    time.sleep(3)
    log.debug("Zero LoadCell...")
    fx_sum = []
    fy_sum = []
    fz_sum = []
    tx_sum = []
    ty_sum = []
    tz_sum = []

    global lc
    for _ in range(cfg.LC["N_ZERO"]):
        fx_sum.append(lc._f[0])
        fy_sum.append(lc._f[1])
        fz_sum.append(lc._f[2])

        tx_sum.append(lc._t[0])
        ty_sum.append(lc._t[1])
        tz_sum.append(lc._t[2])

        time.sleep(0.1)
        
    fx_sum.sort()
    fy_sum.sort()
    fz_sum.sort()
    
    tx_sum.sort()
    ty_sum.sort()
    tz_sum.sort()
    
    start = int(cfg.LC["N_ZERO"]*0.15)
    end = int(cfg.LC["N_ZERO"]*0.85)
    
    fx_sum = fx_sum[start:end]
    fy_sum = fy_sum[start:end]
    fz_sum = fz_sum[start:end]
    
    tx_sum = tx_sum[start:end]
    ty_sum = ty_sum[start:end]
    tz_sum = tz_sum[start:end]
    
    cfg.LC0F = [round(sum(fx_sum) / len(fx_sum), 5), round(sum(fy_sum) / len(fy_sum), 5), round(sum(fz_sum) / len(fz_sum), 5)]
    cfg.LC0T = [round(sum(tx_sum) / len(tx_sum), 5), round(sum(ty_sum) / len(ty_sum), 5), round(sum(tz_sum) / len(tz_sum), 5)]
    
    lc._fx0.value = cfg.LC0F[0]
    lc._fy0.value = cfg.LC0F[1]
    lc._fz0.value = cfg.LC0F[2]
    
    lc._tx0.value = cfg.LC0T[0]
    lc._ty0.value = cfg.LC0T[1]
    lc._tz0.value = cfg.LC0T[2]
    
    log.info(
        "\nLOAD_CELL_ZERO \n"
        + "LC0F: "
        + str(cfg.LC0F)
        + " N,\n"
        + "LC0T: "
        + str(cfg.LC0T)
        + " Nm,\n"
    )

    log.debug("Zero LoadCell DONE")


def log_all():
    log.debug("Fx: " + str(lc._f[0]))
    log.debug("Fy: " + str(lc._f[1]))
    log.debug("Fz: " + str(lc._f[2]))

    log.debug("Mx: " + str(lc._t[0]))
    log.debug("My: " + str(lc._t[1]))
    log.debug("Mz: " + str(lc._t[2]))

def get_forces():
    return list(lc._f)  # Fx, Fy, Fz

def get_moments():
    return list(lc._t)  # Mx, My, Mz