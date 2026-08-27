import queue
import random
import customtkinter as ctk

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
        self.root = ctk.CTk()
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
            self.status_label.configure(text=self.get_status())
        
            
    def get_status(self) -> str:
        return  f"Status : {self._store.state.connection.name}"
    
    def show_window(self, window:BaseWindow):
        x_offset = 100
        y_offset = 100
        new_window = window(self.root, x_offset, y_offset, self._config.ASSET_DIR)
        self.opened_windows.append(new_window)
    
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
        window = ctk.CTkToplevel(self.root)
        window.title("ray-virus-config")
        window.protocol("WM_DELETE_WINDOW", lambda:(window.destroy(), setattr(self, "status_label",None)))
        
        # tab control
        tabControl = ctk.CTkTabview(master=window)
        tabControl.add('General')
        tabControl.add("Streamerbot")
        tabControl.add("Window List")
        tabControl.pack(expand=1, fill="both")
        
        gen_setting_tab = tabControl.tab("General")
        window_list_tab = tabControl.tab("Window List")
        sb_setting_tab = tabControl.tab("Streamerbot")
        
        # general settings
        self.enabled_var = ctk.BooleanVar(value=self._store.state.enabled)
        ctk.CTkCheckBox(gen_setting_tab, text="Enable Redeems",
                       variable=self.enabled_var,
                       command=lambda: self._store.update(enabled=not self._store.state.enabled)
                       ).pack()
        ctk.CTkLabel(gen_setting_tab, text="Redeem Name").pack()
        ctk.CTkEntry(gen_setting_tab).pack()
        
        # window list
        self.window_scrollable = ctk.CTkScrollableFrame(master = window_list_tab)
        self.window_scrollable.pack()
        for name, win in self.window_types.items():
            button = ctk.CTkButton(self.window_scrollable, text=name, command=lambda:self.show_window(win))
            button.pack()
        
        # streamerbot settings
        self.status_label = ctk.CTkLabel(sb_setting_tab, text=self.get_status())
        self.status_label.pack()
        
        ctk.CTkLabel(sb_setting_tab, text="Websocket Address : ").pack()
        ctk.CTkEntry(sb_setting_tab).pack()
        ctk.CTkLabel(sb_setting_tab, text="WebSocket Password : ").pack()
        ctk.CTkEntry(sb_setting_tab).pack()
        self.auto_start = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(sb_setting_tab, text="Auto-Start Websocket",
                       variable=self.auto_start,
                       command=None
                       ).pack()
        ctk.CTkButton(sb_setting_tab, text="Connect").pack()
    
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
        

    


   