# config.py
# oliverwigger

IS_AUTOSTART = True
IS_DEBUG = True
IS_LC_ZERO = False
IS_MOTOR_CALIBRATE = False

# General
# -------------------------------------
AXIS = dict(
    X=0,
    Y=1,
    Z=2,
)

CAL_CYCLE = 0
ANGLE0 = [0, 0, 0]
TORQUE0 = [0, 0, 0]

GEN = dict(GEAR_RATIO=6.3333333, T_INSTRON=0.02)  # 190/30

# File
# -------------------------------------
DATA_FILE = dict(
    HEADER="SPINE CONTROLLER\n"
    + "Spine-Biomechanics\n"
)

# CONTROL
# -------------------------------------
SET_TORQUE = []
MAX_ANG = 13
CONTROL_ANGLE = 0.003

# TORQUE FILTER
# -------------------------------------
C_FILTER = 0.1

# GUI
# -------------------------------------
COL = dict(en="orange", done="limegreen", nen="dim grey")

# Communication
# -------------------------------------
SPI = dict(MAX_SPEED=8000000, BUS=1)  # 8Mhz


# Encoder
# -------------------------------------
ENC_MSG = dict(
    READ_CNTR=0x60,
    WRITE_MDR0=0x88,
    WRITE_MDR1=0x90,
    MDRO=0b00000011,
    MDR1=0b00000010,
    CLR_CNTR=0x20,
)

ENC_CPR = 2048

ENC_OFFSET = [0, 0, 0]
ENC_ZERO = [14.2, 14.2, 14.2]

# Motor
# -------------------------------------
MOT = dict(XP=24, XN=23, YP=4, YN=14, ZP=27, ZN=15)
MOT_T_HOMING = 5

# Fogger
# -------------------------------------
FOG = dict(PIN=26, ON_TIME=20, OFF_TIME=20)

# LoadCell
# -------------------------------------

LC = dict(
    PORT="/dev/ttyUSB0", ACCURACY=3, N_ZERO=100, 
)

LC0F = [-143.12794, 192.01763, 0.0] # zero forces x y z [-100, 150, 0]
LC0T = [7.82774, 6.71137, -0.22554] # zero torques x y z [5, 5, 0]

# LC0F = [0, 0, 0] # zero forces x y z [-100, 150, 0]
# LC0T = [-100, 0, 0] # zero torques x y z [5, 5, 0]

# LED
# -------------------------------------
LED = dict(
    RED=13,
    ORANGE=5,
    GREEN=6,
    N_BLINK=3,
    T_BLINK=0.15,
)

# Instron
# -------------------------------------
INSTRON = dict(
    IN1=2,
    IN2=3,
    IN3=22,
    IN4=10,
    OUT1=9,
    OUT2=25,
    OUT3=11,
    OUT4=8,
)