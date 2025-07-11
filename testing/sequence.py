# sequence.py
# oliverwigger

import logging as log
import time
import tracemalloc

#import hardware.led as led
from datetime import datetime
import hardware.fogger as fogger
import hardware.motor as motor
import gui.processFrame as processFrame
import gui.logFrame as logFrame
import config as cfg
import testing.cycle as cycle
import gui.parameterFrame as parameterFrame


def start():
    #led.switch_to("ORANGE")

    #get & set parameters 
    parameter = parameterFrame.ParameterWindow.get_paramter()
    _init_test_data_file(parameter)

    c = parameter[1]

    fogger.auto_fogger_start()

    # debug
    tracemalloc.start()
    t_start_abs = time.time()

    set_angle = []
    set_axis = []

    for i in range(0, len(c)):
        cfg.SET_TORQUE.append(c[i][2])
        cfg.SET_TORQUE.append(c[i][3])
        set_angle.append(round(c[i][2],3))
        set_angle.append(0)
        set_angle.append(round(c[i][3],3))
        set_axis.append(c[i][0])


    cfg.SET_TORQUE = [-1.0, 7.0, -5.0, 5.0, -3.0, 3.0]
    set_angle = [-1.0, 0, 4.0, -3.0, 0, 3.0, -1.0, 0, 1.0]
    set_axis = ['Y', 'X', 'Z']

    log.debug("SET_TORQUE: " + str(cfg.SET_TORQUE))
    log.debug("set_angle: " + str(set_angle))
    log.debug("set_axis:" + str(set_axis))

    time.sleep(3) 

    #data read by system
    days = parameter[0]
    
    # test running
    while processFrame.is_test_on:
        n_abs = 0
        for n_day in range(days):
            if processFrame.is_test_on:
                log.debug(" ")
                log.debug("Day: " + str(n_day + 1) + "/" + str(days))
                # debug.log_malloc()

            # MOVEMENT
            for n_mov in range(0, len(c)):
                if processFrame.is_test_on:
                    log.debug("Movement: " + str(n_mov+1) + "/" + str(len(c)))

                    #start position
                    #motor.move_ang(axis, set_angle)
                    motor.move_ang(set_axis[n_mov], set_angle[3*n_mov])
                    
                    # CYCLE
                    t_start = time.time()
                    for n_cyc in range(0, c[n_mov][1]):
                        if processFrame.is_test_on:
                            # debugging
                            n_abs = n_abs + 1
                            # single_cycle(axis, a0, a1, n_mov)
                            a0, a1, t0, t1 = cycle.single_cycle(
                                set_axis[n_mov], set_angle[3*n_mov], set_angle[3*n_mov+2], n_abs
                            )
                            
                            t_passed = time.time() - t_start

                            # logger
                            #########################################
                            t_rel = int(time.time() - t_start_abs)
                            t_abs = datetime.now().strftime("%H:%M:%S")
                            t_start = time.time()


                            # save data to file
                            _save_to_file(
                                f"{n_abs};{n_day};{n_mov};{n_cyc};{a0};{t0};{a1};{t1};{t_abs};{t_rel};{round(1 / t_passed, 2)}"
                            )
                            
                            #print torque control
                            if t1 < cfg.SET_TORQUE[2*n_mov+1]:
                                set_angle[3*n_mov+2] = round(set_angle[3*n_mov+2] + cfg.CONTROL_ANGLE, 3) # 0.007
                            else: 
                                set_angle[3*n_mov+2] = round(set_angle[3*n_mov+2] - cfg.CONTROL_ANGLE, 3) # 0.007
                                
                            #print torque control
                            if t0 < cfg.SET_TORQUE[2*n_mov]:
                                set_angle[3*n_mov] = round(set_angle[3*n_mov] + cfg.CONTROL_ANGLE, 3) # 0.007
                            else: 
                                set_angle[3*n_mov] = round(set_angle[3*n_mov] - cfg.CONTROL_ANGLE, 3) # 0.007
                            
                            set_angle[3*n_mov] = _is_in_range(set_angle[3*n_mov])
                            set_angle[3*n_mov+2] = _is_in_range(set_angle[3*n_mov+2])
                        else:
                            return
                    
                    #zero position
                    motor.move_ang(set_axis[n_mov], set_angle[3*n_mov+1])
                       
                    cycle.IS_CYCLE_ON = 0 # turn off measurement
                    time.sleep(0.2)
                    
                    # GUI Move Update %
                    logFrame.LogWindow.write_log(
                        "     Move: "
                        + str(n_mov+1)
                        + "/"
                        + str(len(c))
                        + " -> "
                        + str(round((n_mov+1) / len(c) * 100))
                        + "%"
                    )
                else:
                    return

            # GUI Day Update %
            logFrame.LogWindow.write_log(
                "Day: "
                + str(n_day + 1)
                + "/"
                + str(parameter[0])
                + " -> "
                + str(round((n_day + 1) / parameter[0] * 100))
                + "%"
            )
            cfg.CAL_CYCLE = 1
            
            for i in range (0, len(c)):
                set_angle[3*i+1] = cfg.ANGLE0[i]

        # stop testing
        processFrame.is_test_on = 0
        fogger.auto_fogger_stop()
        processFrame.ProcessWindow.stop()

    #led.switch_to("GREEN")
    log.info(" ")
    log.info("Test finished")
    


def _is_in_range(angle):
    return max(-cfg.MAX_ANG, min(angle, cfg.MAX_ANG))

def _init_test_data_file(parameter):
    try:
        # Header
        f = open("data/test_data.csv", "w")
        _save_to_file(cfg.DATA_FILE["HEADER"])

        # Parameter
        _save_to_file("Test Parameter:")
        _save_to_file(str(parameter))

        # CSV Description
        _save_to_file("n_abs; n_Day; n_Mov; n_Cyc; a0; t0; a1; t1; t_abs; t_rel; f")
    except:
        log.error("Could not initiate data_file.csv")


def _save_to_file(text):
    try:
        with open("data/test_data.csv", "a") as f:
            f.write(text + "\n")
    except:
        log.error("Could not append to data/test_data.csv file.")