# gui_plot
# oliverwigger

from  matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class plotWindow:
    def __init__(self, root, frame):
        fig = Figure(figsize = (5, 5), dpi = 100) 
    
        # list of squares 
        y = [i**2 for i in range(11)] 
    
        # adding the subplot 
        plot1 = fig.add_subplot(111)
        plot1.plot(y) 
        
        canvas = FigureCanvasTkAgg(fig, root)
        root1 = root
        canvas.draw() 
    
        # placing the canvas on the Tkinter window 
        canvas.get_tk_widget().grid() 
        
        