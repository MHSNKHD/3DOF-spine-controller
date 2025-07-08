# gui_processFrame.py
# oliverwigger

import tkinter as tk
from tkinter import messagebox
import logging as log
import threading as thread
import time
from hardware import load_cell

import hardware.motor as motor
import testing.sequence as sequence
import config as cfg
import hardware.init as init


import gui.logFrame as logFrame
import gui.parameterFrame as parameterFrame

# variables
bt_height = 2
bt_width = 16
FONT_SIZE = 25

is_test_on = 0

bt_start = None
bt_stop = None
bt_homing = None


class ProcessWindow:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame

        # functions
        ##########################################
        def _cb_init_DSS():
            if cfg.IS_AUTOSTART:
                logFrame.LogWindow.write_log("AUTOSTART ACTIVE")

            log.info("Initialize Dynamic Spine Simulator...")

            # GUI start
            if not cfg.IS_DEBUG:
                tk.messagebox.showinfo("Start Process", "1. do that \n 2. Do this \n 3. Do that")  # type: ignore
            logFrame.LogWindow.write_log("Initialization started ... (~10s)")  # type: ignore
            root.update_idletasks()
            
            # function
            th_init = thread.Thread(target=init.init, name="init")
            th_init.start()
            time.sleep(1)
            
            th_load_cell = thread.Thread(target=load_cell.start, name="init_load_cell")
            th_load_cell.start()
            time.sleep(5)
            
            if cfg.IS_LC_ZERO:
                load_cell.zero()
                time.sleep(5)

            # GUI end
            bt_init.config(bg=cfg.COL["done"], state=tk.DISABLED)
            bt_init.config(state=tk.DISABLED)
            root.update_idletasks()
            logFrame.LogWindow.write_log("Initialization DONE")
            log.info("Initialization DONE")

            if cfg.IS_AUTOSTART:
                _cb_homing()

        def _cb_homing():
            log.info("Start calibration...")

            # GUI start
            if not cfg.IS_DEBUG:
                tk.messagebox.showwarning("Start homing", "Machine will start to move")
            logFrame.LogWindow.write_log("Calibration started ... (~10s)")
            root.update_idletasks()

            # function
            if cfg.IS_MOTOR_CALIBRATE:
                motor.calibrate()

            # GUI end
            bt_homing.config(bg=cfg.COL["done"])
            bt_insert.config(state=tk.NORMAL, bg=cfg.COL["en"])
            bt_homing.config(state=tk.DISABLED)
            logFrame.LogWindow.write_log("Calibration DONE")
            log.info("Calibration DONE")

            if cfg.IS_AUTOSTART:
                _cb_insert_specimen()

        def _cb_insert_specimen():
            log.info("Insert Specimen...")

            # GUI start
            if not cfg.IS_DEBUG:
                tk.messagebox.showinfo(
                    "Insert Specimen",
                    "1. Insert Specimen \n 2. Insert Cover \n 3. Connect Instron",
                )
            root.update_idletasks()

            # function
            pass

            # GUI end
            bt_insert.config(bg=cfg.COL["done"])
            bt_parameter.config(state=tk.NORMAL, bg=cfg.COL["en"])
            bt_insert.config(state=tk.DISABLED)
            logFrame.LogWindow.write_log("Specimen inserted.")
            log.info("Insert Specimen ended")

            if cfg.IS_AUTOSTART:
                _cb_parameter()

        def _cb_parameter():
            # print(parameterFrame.ParameterWindow.get_paramter())

            # function
            parameterFrame.bt_load.config(state=tk.DISABLED, bg=cfg.COL["nen"])

            # GUI end
            logFrame.LogWindow.write_log("Parameter set.")
            bt_parameter.config(bg=cfg.COL["done"])
            bt_start.config(state=tk.NORMAL, bg=cfg.COL["en"])
            bt_parameter.config(state=tk.DISABLED)

            if cfg.IS_AUTOSTART:
                _cb_start_test()

        def _cb_start_test():
            log.info("Start testing...")

            # GUI start
            if not cfg.IS_DEBUG:
                tk.messagebox.showwarning("Start Test", "Machine will start to move.")
            logFrame.LogWindow.write_log("Test started ...")
            root.update_idletasks()

            # function
            global is_test_on
            is_test_on = 1
            t_testing = thread.Thread(target=sequence.start, name="test sequence")
            t_testing.start()

            # GUI end
            bt_start.config(bg=cfg.COL["done"])
            bt_stop.config(state=tk.NORMAL, bg=cfg.COL["en"])
            bt_parameter.config(state=tk.DISABLED)
            bt_start.config(state=tk.DISABLED)

        def _cb_stop_test():
            log.info("Stop testing...")

            # GUI start
            if not cfg.IS_DEBUG:
                tk.messagebox.showwarning("Stop Test", "Machine will stop to move.")

            logFrame.LogWindow.write_log("Test stopping ...")
            root.update_idletasks()

            # function
            global is_test_on
            is_test_on = 0
            time.sleep(1)
            motor.stop_all()

            # GUI end
            bt_start.config(bg=cfg.COL["en"], state=tk.ACTIVE)
            bt_stop.config(state=tk.DISABLED, bg=cfg.COL["nen"])
            logFrame.LogWindow.write_log("Test stopped.")

        # widgets
        ##########################################
        bt_init = tk.Button(
            frame,
            text="Initialize DSS",
            command=_cb_init_DSS,
            bg=cfg.COL["en"],
            font=("Helvetica", FONT_SIZE),
            height=bt_height,
            width=bt_width,
        )
        global bt_homing
        bt_homing = tk.Button(
            frame,
            text="Home Axis",
            command=_cb_homing,
            bg=cfg.COL["nen"],
            font=("Helvetica", FONT_SIZE),
            height=bt_height,
            width=bt_width,
            state=tk.DISABLED,
        )

        bt_insert = tk.Button(
            frame,
            text="Insert Specimen",
            command=_cb_insert_specimen,
            bg=cfg.COL["nen"],
            font=("Helvetica", FONT_SIZE),
            height=bt_height,
            width=bt_width,
            state=tk.DISABLED,
        )

        bt_parameter = tk.Button(
            frame,
            text="Test Parameter",
            command=_cb_parameter,
            bg=cfg.COL["nen"],
            font=("Helvetica", FONT_SIZE),
            height=bt_height,
            width=bt_width,
            state=tk.DISABLED,
        )

        global bt_start
        bt_start = tk.Button(
            frame,
            text="Start Test",
            command=_cb_start_test,
            bg=cfg.COL["nen"],
            font=("Helvetica", FONT_SIZE),
            height=bt_height,
            width=bt_width,
            state=tk.DISABLED,
        )
        global bt_stop
        bt_stop = tk.Button(
            frame,
            text="Stop Test",
            command=_cb_stop_test,
            bg=cfg.COL["nen"],
            font=("Helvetica", FONT_SIZE),
            height=bt_height,
            width=bt_width,
            state=tk.DISABLED,
        )

        # arrows
        arrow1 = tk.Canvas(frame)
        arrow1.configure(width=50, height=75)
        arrow1.create_line(
            25, 0, 25, 75, arrow=tk.LAST, width=4, arrowshape=(20, 21, 10)
        )

        arrow2 = tk.Canvas(frame)
        arrow2.configure(width=50, height=75)
        arrow2.create_line(
            25, 0, 25, 75, arrow=tk.LAST, width=4, arrowshape=(20, 21, 10)
        )

        arrow3 = tk.Canvas(frame)
        arrow3.configure(width=50, height=75)
        arrow3.create_line(
            25, 0, 25, 75, arrow=tk.LAST, width=4, arrowshape=(20, 21, 10)
        )

        arrow4 = tk.Canvas(frame)
        arrow4.configure(width=50, height=75)
        arrow4.create_line(
            25, 0, 25, 75, arrow=tk.LAST, width=4, arrowshape=(20, 21, 10)
        )

        arrow5 = tk.Canvas(frame)
        arrow5.configure(width=50, height=75)
        arrow5.create_line(
            25, 0, 25, 75, arrow=tk.LAST, width=4, arrowshape=(20, 21, 10)
        )

        arrow6 = tk.Canvas(frame)
        arrow6.configure(width=50, height=75)
        arrow6.create_line(
            25, 0, 25, 75, arrow=tk.LAST, width=4, arrowshape=(20, 21, 10)
        )

        arrow7 = tk.Canvas(frame)
        arrow7.configure(width=50, height=75)
        arrow7.create_line(
            25, 0, 25, 75, arrow=tk.LAST, width=4, arrowshape=(20, 21, 10)
        )

        # grid
        bt_init.grid(row=0, column=0)
        arrow1.grid(row=1, column=0)

        bt_homing.grid(row=2, column=0)
        arrow3.grid(row=3, column=0)

        bt_insert.grid(row=4, column=0)
        arrow4.grid(row=5, column=0)

        bt_parameter.grid(row=6, column=0)
        arrow6.grid(row=7, column=0)

        bt_start.grid(row=8, column=0)
        arrow7.grid(row=9, column=0)

        bt_stop.grid(row=10, column=0)

        if cfg.IS_AUTOSTART:
            bt_init.after(4000, bt_init.invoke)

    def stop():
        bt_start.config(bg=cfg.COL["en"])
        bt_stop.config(state=tk.DISABLED, bg=cfg.COL["nen"])
        logFrame.LogWindow.write_log("Test ended.")