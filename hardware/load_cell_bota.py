# load_cell_bota.py
# oliverwigger

import struct
import time
import threading

from collections import namedtuple

import serial
import logging as log
import gui.logFrame as logFrame
from multiprocessing import Process
import multiprocessing
import ctypes
from crc import Calculator, Configuration


class BotaSerialSensor:
    BOTA_PRODUCT_CODE = 123456
    BAUDERATE = 460800
    SINC_LENGTH = 512  # 512
    CHOP_ENABLE = 0
    FAST_ENABLE = 0
    FIR_DISABLE = 1
    TEMP_COMPENSATION = 0  # 0: Disabled (recommended), 1: Enabled
    USE_CALIBRATION = 1  # 1: calibration matrix active, 0: raw measurements
    DATA_FORMAT = 0  # 0: binary, 1: CSV
    BAUDERATE_CONFIG = 4  # 0: 9600, 1: 57600, 2: 115200, 3: 230400, 4: 460800
    FRAME_HEADER = b"\xAA"
    # Note that the time step is set according to the sinc filter size!
    time_step = 0.01
    proc_thread = None

    def __init__(self, port):
        self._port = port
        self._ser = serial.Serial(timeout=0.1)
        self._pd_thread_stop_event = threading.Event()
        DeviceSet = namedtuple("DeviceSet", "name product_code config_func")
        self._expected_device_layout = {
            0: DeviceSet(
                "BFT-LAXS-SER-M8", self.BOTA_PRODUCT_CODE, self.bota_sensor_setup
            )
        }
        self._status = None

        # Multiprocess Arrays
        # self._f = multiprocessing.Array(ctypes.c_double, (0.0, 0.0, 0.0))
        # self._t = multiprocessing.Array(ctypes.c_double, (0.0, 0.0, 0.0))

        # self._fx0 = multiprocessing.Value(ctypes.c_float, 0.0)
        # self._fy0 = multiprocessing.Value(ctypes.c_float, 0.0)
        # self._fz0 = multiprocessing.Value(ctypes.c_float, 0.0)
        
        # self._tx0 = multiprocessing.Value(ctypes.c_float, 0.0)
        # self._ty0 = multiprocessing.Value(ctypes.c_float, 0.0)
        # self._tz0 = multiprocessing.Value(ctypes.c_float, 0.0)
        # the followung part is added bz me to replace the above commented part
        self._f = [0.0, 0.0, 0.0]
        self._t = [0.0, 0.0, 0.0]

        self._fx0 = 0.0
        self._fy0 = 0.0
        self._fz0 = 0.0

        self._tx0 = 0.0
        self._ty0 = 0.0
        self._tz0 = 0.0
        
        
        # added variables
        self._n_measured = 0
        self._lc_is_on = 0
    
    
    #sub process
    #####################################################
    def _processdata_thread_nocrc(self):
        i = 0
        t_start = time.time()
        tm = 0
        IS_TM_RESET = 0 
        
        while not self._pd_thread_stop_event.is_set():
            frame_synced = False
            crc16X25Configuration = Configuration(
                16, 0x1021, 0xFFFF, 0xFFFF, True, True
            )
            crc_calculator = Calculator(crc16X25Configuration)

            while not frame_synced and not self._pd_thread_stop_event.is_set():
                possible_header = self._ser.read(1)
                if self.FRAME_HEADER == possible_header:
                    data_frame = self._ser.read(34)
                    crc16_ccitt_frame = self._ser.read(2)
                    
                    crc16_ccitt = struct.unpack_from("H", crc16_ccitt_frame, 0)[0]
                    checksum = crc_calculator.checksum(data_frame)
                    if checksum == crc16_ccitt:
                        #print("Frame synced")
                        frame_synced = True
                    else:
                        self._ser.read(1)
                        
                    while frame_synced and not self._pd_thread_stop_event.is_set():
                        frame_header = self._ser.read(1)

                        if frame_header != self.FRAME_HEADER:
                            #print("Lost sync")
                            frame_synced = False
                            break

                        data_frame = self._ser.read(34)
                        crc16_ccitt_frame = self._ser.read(2)

                        crc16_ccitt = struct.unpack_from("H", crc16_ccitt_frame, 0)[0]
                        checksum = crc_calculator.checksum(data_frame)
                        if checksum != crc16_ccitt:
                            #print("CRC mismatch received")
                            break
                        
                        self._status = struct.unpack_from("H", data_frame, 0)[0]
                        
                        fx_temp = round(struct.unpack_from("f", data_frame, 2)[0] - self._fx0,6)
                        if abs(fx_temp) < 500: #filter heavy outliers
                            if abs(fx_temp) - abs(self._f[0]) < 300:
                                self._f[0] = fx_temp
                        
                        fy_temp = round(struct.unpack_from("f", data_frame, 6)[0] - self._fy0,6)
                        if abs(fy_temp) < 500: #filter heavy outliers
                            if abs(fy_temp) - abs(self._f[1]) < 300:
                                self._f[1] = fy_temp
                        
                        fz_temp = round(struct.unpack_from("f", data_frame, 10)[0] - self._fz0,6)
                        if abs(fz_temp) < 500: #filter heavy outliers
                            if abs(fz_temp) - abs(self._f[2]) < 300:
                                self._f[2] = 0 #fz_temp
                        
                        #torque
                        tx_temp = -round(struct.unpack_from("f", data_frame, 18)[0] - self._tx0,6)
                        if abs(tx_temp) < 20: #filter heavy outliers
                            if abs(tx_temp) - abs(self._t[0]) < 10:
                                self._t[0] = tx_temp
                        
                        ty_temp = round(struct.unpack_from("f", data_frame, 14)[0] - self._ty0,6)
                        if abs(ty_temp) < 20: #filter heavy outliers
                            if abs(ty_temp) - abs(self._t[1]) < 10:
                                self._t[1] = ty_temp
                            
                        tz_temp = round(struct.unpack_from("f", data_frame, 22)[0] - self._tz0,6)
                        if abs(tz_temp) < 20: #filter heavy outliers
                            if abs(tz_temp) - abs(self._t[2]) < 10:
                                self._t[2] = tz_temp

                        i = i+1
                        '''
                        print('\n ------------------')
                        print(f"Fx: {self._f[0]}")
                        print(f"Fy: {self._f[1]}")
                        print(f"Fz: {self._f[2]}")
                        
                        print(f"Tx: {self._t[0]}")
                        print(f"Ty: {self._t[1]}")
                        print(f"Tz: {self._t[2]}")
                        time.sleep(0.001)
                        '''
                        
                        if i >= 1000:
                            #log.debug(f"LoadCell: {round(i/(time.time()-t_start),2)} Hz")
                            i = 0
                            t_start = time.time()
                        
                        
    def bota_sensor_setup(self):
        log.debug("BOTA: Trying to setup the sensor.")
        # Wait for streaming of data
        out = self._ser.read_until(bytes("App Init", "ascii"))
        if not self.contains_bytes(bytes("App Init", "ascii"), out):
            log.debug("BOTA: Sensor not streaming, check if correct port selected!")
            return False
        time.sleep(0.5)
        self._ser.reset_input_buffer()
        self._ser.reset_output_buffer()

        # Go to CONFIG mode
        cmd = bytes("C", "ascii")
        self._ser.write(cmd)
        out = self._ser.read_until(bytes("r,0,C,0", "ascii"))
        if not self.contains_bytes(bytes("r,0,C,0", "ascii"), out):
            log.debug("BOTA: Failed to go to CONFIG mode.")
            return False

        # Communication setup
        comm_setup = f"c,{self.TEMP_COMPENSATION},{self.USE_CALIBRATION},{self.DATA_FORMAT},{self.BAUDERATE_CONFIG}"
        # print(comm_setup)
        cmd = bytes(comm_setup, "ascii")
        self._ser.write(cmd)
        out = self._ser.read_until(bytes("r,0,c,0", "ascii"))
        if not self.contains_bytes(bytes("r,0,c,0", "ascii"), out):
            log.debug("BOTA: Failed to set communication setup.")
            return False
        time_step = 0.00001953125 * self.SINC_LENGTH
        log.debug("BOTA: Timestep: {}".format(time_step))

        # Filter setup
        filter_setup = f"f,{self.SINC_LENGTH},{self.CHOP_ENABLE},{self.FAST_ENABLE},{self.FIR_DISABLE}"
        # print(filter_setup)
        cmd = bytes(filter_setup, "ascii")
        self._ser.write(cmd)
        out = self._ser.read_until(bytes("r,0,f,0", "ascii"))
        if not self.contains_bytes(bytes("r,0,f,0", "ascii"), out):
            log.debug("BOTA: Failed to set filter setup.")
            return False

        # Go to RUN mode
        cmd = bytes("R", "ascii")
        self._ser.write(cmd)
        out = self._ser.read_until(bytes("r,0,R,0", "ascii"))
        if not self.contains_bytes(bytes("r,0,R,0", "ascii"), out):
            log.debug("BOTA: Failed to go to RUN mode.")
            return False

        return True

    def contains_bytes(self, subsequence, sequence):
        return subsequence in sequence

    def start(self):
        global _lc_is_on

        self._ser.baudrate = self.BAUDERATE
        self._ser.port = self._port
        self._ser.timeout = 10

        try:
            self._ser.open()
            log.debug("BOTA: Opened serial port {}".format(self._port))
        except serial.SerialException as var:
            logFrame.LogWindow.write_log("Load Cell not connected")
            print("An Exception Occured")
            print("Exception Details-> ", var)
            # log.debug('BOTA: Could not open port')
            # raise BotaSerialSensorError('Could not open port')

        if not self._ser.is_open:
            log.debug("BOTA: Could not open port")
            raise BotaSerialSensorError("Could not open port")

        if not self.bota_sensor_setup():
            log.debug("Could not setup sensor!")
            return
        
        self._lc_is_on = 1
        
        # multiprocess
        # proc = Process(target=self._processdata_thread_nocrc, name="load_cell_multiprocess")
        # proc.start()
        # the following part is added be me, to replace the above two lines *(changing the process to thread)
        self.proc_thread = threading.Thread(target=self._processdata_thread_nocrc, name="load_cell_thread", daemon=True)
        self.proc_thread.start()

        time.sleep(1)
        
        #proc_thread = threading.Thread(
        #    target=self._processdata_thread_nocrc, name="LoadCell"
        #)
        #proc_thread.start()
        
        

    def stop(self):
        self._lc_is_on = 0
        self._pd_thread_stop_event.set()
        self.proc_thread.join()

        self._ser.close()

    @staticmethod
    def _sleep(duration, get_now=time.perf_counter):
        now = get_now()
        end = now + duration
        while now < end:
            now = get_now()


class BotaSerialSensorError(Exception):
    def __init__(self, message):
        super(BotaSerialSensorError, self).__init__(message)
        self.message = message


#my helper function ;-)
def _is_in_range(new, old, tolerance):
    return int(abs(new - old) <= tolerance)