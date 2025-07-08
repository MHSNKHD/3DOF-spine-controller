# parameterFrame.py

import tkinter as tk
from tkinter import filedialog as fd
import config as cfg
import logging as log
import csv
import gui.logFrame as logFrame

if cfg.IS_DEBUG or cfg.IS_AUTOSTART:
    file_path = "/home/dss/Documents/xyz/data/protocols/debug.csv"
else:
    file_path = None

file_content = None
bt_load = None


class ParameterWindow:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame

        def _cb_load():
            global file_path, file_content
            file_path = fd.askopenfilename(
                title="Select a Protocol File",
                filetypes=(("protocol_file", "*.csv"), ("All Files", "*.csv*")),
                initialdir="./data/protocols/",
            )

            try:
                with open(file_path, "r") as f:
                    file_content = f.read()
                    txt_protocol.delete(1.0, tk.END)  # Clear any existing text
                    txt_protocol.insert(tk.END, "File path: ")
                    txt_protocol.insert(tk.END, file_path)
                    txt_protocol.insert(tk.END, "\n \n")
                    txt_protocol.insert(tk.END, file_content)
            except:
                log.error("Could not read from " + str(file_path))

        lb_protocol = tk.Label(frame, text="Protocol", font=("bold", 25))

        global bt_load
        bt_load = tk.Button(
            frame,
            text="Load Protocol",
            command=_cb_load,
            bg=cfg.COL["en"],
            # font=("Helvetica", FONT_SIZE),
            # height=bt_height,
            # width=bt_width,
        )
        txt_protocol = tk.Text(
            frame, font=("Arial Rounded MT Bold", 16)
        )  # Label for protocol

        # grid placement
        lb_protocol.grid(row=0, column=0)
        bt_load.grid(row=0, column=1)
        txt_protocol.grid(row=1, column=0, columnspan=2)

    def get_paramter():
        try:
            data = []
            with open(file_path, mode="r", newline="") as file:
                data = list(csv.reader(file, delimiter=";"))
            
            days = int(data[1][0])  # fixed in csv file
            movement = []

            for i in range(5, len(data)):  # iterate over all movements in the protocol
                movement.append(
                    [data[i][0], int(data[i][1]), float(data[i][2]), float(data[i][3])]
                )

            return (days, movement)
        except:
            log.debug("no protocol loaded")
            logFrame.LogWindow.write_log("no protocol loaded")