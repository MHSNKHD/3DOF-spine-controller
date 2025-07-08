# encoder.py
# Copyright (c) 2025 Oliver Wigger


import time
import spidev
import config as cfg

spi_devices = None

def get_angle(axis):
    global spi_devices
    msg = [cfg.ENC_MSG["READ_CNTR"], 0x0, 0x0]
    
    reply = spi_devices[axis].xfer(msg)

    enc_val = reply[2] | reply[1] << 8
    enc_angle = enc_val / cfg.ENC_CPR * 90.0  # 360° x quadratur mode

    axis_angle = round(
        enc_angle / cfg.GEN["GEAR_RATIO"] - cfg.ENC_ZERO[axis] + cfg.ENC_OFFSET[axis], 3
    )
    return axis_angle


def zero():
    global spi_devices
    for axis in range(3):
        spi_devices[axis].writebytes([cfg.ENC_MSG["CLR_CNTR"]])
        time.sleep(0.02)


def init():
    for axis in range(3):
        spi = spidev.SpiDev(cfg.SPI["BUS"], axis)
        spi.max_speed_hz = cfg.SPI["MAX_SPEED"]

        spi.writebytes([cfg.ENC_MSG["WRITE_MDR0"], cfg.ENC_MSG["MDRO"]])
        time.sleep(0.02)

        spi.writebytes([cfg.ENC_MSG["WRITE_MDR1"], cfg.ENC_MSG["MDR1"]])
        time.sleep(0.02)
        spi.close()

    global spi_devices
    spi0 = spidev.SpiDev(1, 0)
    spi1 = spidev.SpiDev(1, 1)
    spi2 = spidev.SpiDev(1, 2)

    spi0.max_speed_hz = cfg.SPI["MAX_SPEED"]
    spi1.max_speed_hz = cfg.SPI["MAX_SPEED"]
    spi2.max_speed_hz = cfg.SPI["MAX_SPEED"]

    spi_devices = [spi0, spi1, spi2]
