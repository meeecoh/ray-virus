from screeninfo import get_monitors
from window import BaseWindow
from typing import Dict
import tkinter as tk
import random
import queue


class VirusManager:
    """Virus Window Manager"""
    def __init__(self, config):
        self._num_windows = 0
        self.opened_windows=[]
        self.window_types : Dict[str, BaseWindow] = {}
        
        self.config = config
        
        # tkinter
        self.root = tk.Tk()
        self.root.withdraw() # background parent tkinter window
        
        # get monitor positions
        self.monitors = get_monitors()
        self.target_monitor_idx = 1
        self.target_monitor = self.monitors[self.target_monitor_idx]
        
        # thread-safe queue
        self.cmd_queue = queue.Queue()
    
    def register_window(self, name, window:BaseWindow):
        self.window_types[name] = window
    
    def show_random_window(self):
        # calculate a random position on the screen
        x_offset = 100
        y_offset = 100
        window_values = list(self.window_types.values())
        window = random.choice(window_values)(self.root, x_offset, y_offset)
        
        # windows need to be kept in reference or else images don't show up
        # weird ass bug
        self.opened_windows.append(window)
        
    def create_config_window(self):
        window = tk.Toplevel(self.root)
        window.title("ray-virus-config")
        window.geometry("300x150")
        
        tk.Checkbutton(window, text="Enable Virus").pack()
        tk.Label(window, text=f"StreamerBot Status : disconnected").pack()
        tk.Entry(window, width=30).pack()
        tk.Button(window, text=f"Connect").pack()
    
    def show_config_window(self):
        self.root.after(0, self.create_config_window)
        
    def check_queue(self):
        """Runs on the Main Thread checking for cross-thread requests."""
        try:
            # Non-blocking pop to process all pending tray UI signals
            command = self.cmd_queue.get_nowait()
            
            if command == "CREATE_CONFIG_WINDOW":
                self.create_config_window()
                
            self.cmd_queue.task_done()
        except queue.Empty:
            pass

    def clear_window_list(self):
        """
        Clears window list of any closed windows
        
        Windows are kept in memory using the opened_windows attribute
        This function clears windows that have already closed
        """
        self.opened_windows = [w for w in self.opened_windows if w.closed == False]
        

    


   