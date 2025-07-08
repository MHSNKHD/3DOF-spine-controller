# gui_logFrame
# oliverwigger

import tkinter as tk
import gui

logbox = None

class LogWindow:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame

        self.logbox = tk.Text(
            frame,
            width=int(self.root.winfo_screenheight() * 0.15),
            font=("Arial Rounded MT Bold", 16)
        )
        self.logbox.insert(
            tk.END,
            "Dynamic Spine Simulator\n"
            + "oliverwigger\n"
            + "-----------------------\n",
        )
        self.logbox.see(tk.END)
        self.logbox.configure(state=tk.DISABLED)
        self.logbox.grid()
        
        global logbox
        logbox = self.logbox

    def write_log(text):
        global logbox
        logbox.configure(state="normal")
        logbox.insert(tk.END, text + "\n")
        logbox.configure(state="disabled")

        logbox.yview(tk.END)  # Autoscroll to the bottom