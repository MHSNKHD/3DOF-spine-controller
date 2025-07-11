# cycle.py
# oliverwigger

import logging as log
import time

import hardware.motor as motor
import hardware.instron as instron
import hardware.encoder as encoder
import config as cfg
import hardware.load_cell as load_cell
import threading as thread
import statistics as sta
import csv
import testing.calibration as cal
from scipy.signal import butter, filtfilt

t, angle, torque, force = [], [], [], []
t_s, angle_s, torque_s, force_s = [], [], [], []

IS_CYCLE_ON = 0
n = 0

def single_cycle(axis, a0, a1, n_abs):
    #log.debug("Cycle -> Axis: " + axis + " A1: " + str(a1) + " A0: " + str(a0))

    global IS_CYCLE_ON, n
    n = n_abs
    
    global t_s, angle_s, torque_s, force_s
    t_s, angle_s, torque_s, force_s = [], [], [], []
    
    if IS_CYCLE_ON == 0:
        IS_CYCLE_ON = 1
        th_cycle = thread.Thread(
            target=_start_data_aquisition_cyc,
            args=(axis),
            name="_cycle",
        )
        th_cycle.start()


    # move to angle1
    ########################################
    motor.move_ang(axis, a1)

    # wait for signal by instron
    #_wait_instron()
    
    # move to angle0
    #########################################
    motor.move_ang(axis, a0)
    
    # wait for signal by instron
    #_wait_instron()

    # position reached by machine
    # motor.adjust_set_value(T0)
    
    if IS_CYCLE_ON == 0:
        time.sleep(0.05)
        th_cycle.join()
    
    # return values
    #########################################
    
    #filtering torque
    torque_s = _filter(torque_s)
    
    a0 = min(angle_s)
    a1 = max(angle_s)
    
    # torque
    
    #min_index = torque_s.index(min(torque_s)) # index min torque
    #t0 = round(sta.mean(torque_s[min_index:min_index+2]),3)
    t0 = round(min(torque_s),3)
    
    #max_index = torque_s.index(max(torque_s)) # index max torque
    #t1 = round(sta.mean(torque_s[max_index:max_index+2]),3)
    t1 = round(max(torque_s),3)

    return (a0, a1, t0, t1)


# bad time wait function -> FIX
def _wait_instron():
    t_elapsed = 0
    t = time.time()
    while not instron.read("OUT2") and t_elapsed < cfg.GEN["T_INSTRON"]:
        t_elapsed = time.time() - t
    return


def _start_data_aquisition_cyc(axis):
    t_start = time.time()
    
    global t, angle, torque, force, t_s, angle_s, torque_s, force_s
    t, angle, torque, force = [], [], [], []  
    
    while IS_CYCLE_ON:
        t_temp = round(time.time() - t_start, 3)
        t.append(t_temp)
        t_s.append(t_temp)
        
        a_temp = encoder.get_angle(cfg.AXIS[axis])
        angle.append(a_temp)
        angle_s.append(a_temp)
        
        f_temp = load_cell.lc._f[cfg.AXIS[axis]]
        force.append(f_temp)
        force_s.append(f_temp)
        
        tor_temp = round(load_cell.lc._t[cfg.AXIS[axis]] + f_temp*0.065 - cfg.TORQUE0[cfg.AXIS[axis]], 3)
        torque.append(tor_temp)
        torque_s.append(tor_temp)
        
        time.sleep(0.002)
    
    #filter torque
    force = _filter(force)
    torque = _filter(torque)
    
    #calibrate
    try:
        if cfg.CAL_CYCLE == 0:
            angle0, torque0 = cal.calibrate(angle, torque)
            cfg.ANGLE0[cfg.AXIS[axis]] = round(float(angle0[0]),5)
            #cfg.TORQUE0[cfg.AXIS[axis]] = round(float(torque0[0]),5)
            
            log.info('Calibration DONE')
            log.info(f"Axis: {axis}, Angle0: {angle0}, Torque0: {torque0}")
    except Exception as e:
        log.error(e)
        log.error('___Calibration FAILED___')
    
    try:
        with open("data/cycles/" + str(n) + ".csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Time [s]", "Angle [°]", "Torque [Nm]", "Force [N]"])
            
            for i in range(len(t)):
                writer.writerow([t[i], angle[i], torque[i], force[i]])
            log.info("Wrote data to: data/cycles/" + str(n) + ".csv")
    except Exception as e:
        log.error("Could not write: data/cycles/" + str(n) + ".csv")
        log.error(e)

def _filter(data):
    b, a = butter(1, 0.1)
    filtered_signal = filtfilt(b, a, data)
    filtered_signal = filtered_signal.tolist()
    
    return filtered_signal