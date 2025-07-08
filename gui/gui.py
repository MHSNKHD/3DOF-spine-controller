# gui.py
# oliverwigger

import tkinter as tk
import logging as log


import gui.processFrame as processFrame
import gui.logFrame as logFrame
import gui.parameterFrame as parameterFrame


class MainWindow:
    def start(self):
        log.info("Start tkinter mainloop()")
        self.root.mainloop()

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1600x1000')
        self.root.attributes("-fullscreen", False)
        self.root.title("DSS Dynamic Spine Simulator")

        # process frame
        self.processFrame = tk.Frame(self.root)
        self.processPanel = processFrame.ProcessWindow(self.root, self.processFrame)

        # parameter frame
        self.parameterFrame = tk.Frame(self.root)
        self.parameterPanel = parameterFrame.ParameterWindow(
            self.root, self.parameterFrame
        )

        # log frame
        self.logFrame = tk.Frame(self.root)
        self.logPanel = logFrame.LogWindow(self.root, self.logFrame)

        # plot frame
        # self.plotFrame = tk.Frame(self.root)
        # self.plotPanel = plotFrame.plotWindow(self.root, self.plotFrame)

        # Grid
        ############################
        self.processFrame.grid(row=0, column=1, rowspan=3, padx=(50, 50))
        self.logFrame.grid(row=1, column=0, pady=(25, 25))

        self.parameterFrame.grid(row=0, column=0, pady=10)

        # self.plotFrame.grid(row=1, column=0, pady=10)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)