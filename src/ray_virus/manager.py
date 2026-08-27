import queue
import random
import tkinter as tk
from tkinter import ttk

from screeninfo import get_monitors

from .config import Config
from .stores import AppState, AppStore, ConnectionState
from .window import BaseWindow


class VirusManager:
    """Virus Window Manager"""
    def __init__(self, config : Config, store : AppStore):
        self._num_windows = 0
        self.opened_windows=[]
        self.window_types : dict[str, BaseWindow] = {}
        
        self._config = config
        self._store = store
        self._status = ConnectionState.DISCONNECTED
        self.status_label = None
        
        # tkinter
        self.root = tk.Tk()
        self.root.withdraw() # background parent tkinter window
        
        # get monitor positions
        self.monitors = get_monitors()
        self.target_monitor_idx = 1
        self.target_monitor = self.monitors[self.target_monitor_idx]
        
        # thread-safe queue
        self.cmd_queue = queue.Queue()
        
    def on_state_update(self, new_state: AppState):
        self._status = new_state.connection
        self._update_window()

    def register_window(self, name, window:BaseWindow):
        self.window_types[name] = window
        
    def _update_window(self):
        if self.status_label and self.status_label.winfo_exists():
            self.status_label.config(text=self.get_status())
        
            
    def get_status(self) -> str:
        return  f"Status : {self._store.state.connection.name}"
        
    
    def show_random_window(self):
        # calculate a random position on the screen
        x_offset = 100
        y_offset = 100
        window_values = list(self.window_types.values())
        window = random.choice(window_values)(self.root, x_offset, y_offset, self._config.ASSET_DIR)
        
        # windows need to be kept in reference or else images don't show up
        # weird ass bug
        self.opened_windows.append(window)
        
    def create_config_window(self):
        window = tk.Toplevel(self.root)
        window.title("ray-virus-config")
        window.geometry("400x400")
        window.protocol("WM_DELETE_WINDOW", lambda:(window.destroy(), setattr(self, "status_label",None)))
        
        # tab control
        tabControl = ttk.Notebook(window)
        gen_setting_frame = ttk.Frame(tabControl)
        sb_setting_frame = ttk.Frame(tabControl)
        tabControl.add(gen_setting_frame, text='General Settings')
        tabControl.add(sb_setting_frame, text="Streamerbot Settings")
        tabControl.pack(expand=1, fill="both")
        
        # general settings
        self.enabled_var = tk.BooleanVar(value=self._store.state.enabled)
        tk.Checkbutton(gen_setting_frame, text="Enable Redeems",
                       variable=self.enabled_var,
                       command=lambda: self._store.update(enabled=not self._store.state.enabled)
                       ).pack()
        tk.Label(gen_setting_frame, text="Redeem Name").pack()
        tk.Entry(gen_setting_frame, width=30).pack()
        
        # streamerbot settings
        tk.Label(sb_setting_frame, text="Websocket Address : ").pack()
        tk.Entry(sb_setting_frame, width=30).pack()
        tk.Label(sb_setting_frame, text="WebSocket Password : ").pack()
        tk.Entry(sb_setting_frame, width=30).pack()
        self.auto_start = tk.BooleanVar(value=True)
        tk.Checkbutton(sb_setting_frame, text="Auto-Start Websocket",
                       variable=self.auto_start,
                       command=None
                       ).pack()
        tk.Button(sb_setting_frame, text="Connect").pack()
    
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
        

    


   