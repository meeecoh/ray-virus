import queue
import random
from collections.abc import Callable

import customtkinter as ctk
from screeninfo import Monitor, get_monitors

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
        
        self.config_window = None
        
        # tkinter
        self.root = ctk.CTk()
        ctk.deactivate_automatic_dpi_awareness()
        self.root.withdraw() # background parent tkinter window
        
        # get monitor positions
        self.monitors = get_monitors()
        self.target_monitor_idx = self._store.state.target_monitor_idx
        
        # thread-safe queue
        self.cmd_queue = queue.Queue()
        
        # sub/pub
        self.connect_callback : Callable = None
        
    @property
    def target_monitor(self) -> Monitor:
        return self.monitors[self.target_monitor_idx]
        
    def on_state_update(self, new_state: AppState):
        self._status = new_state.connection
        self.target_monitor_idx = new_state.target_monitor_idx
        self._update_window()

    def register_window(self, name, window:BaseWindow):
        self.window_types[name] = window
        
    def register_connect_callback(self, callable:Callable):
        self.connect_callback = callable
        
    def _on_connect_click(self):
        self.connect_callback()
        
    def _on_change_monitor(self, choice):
        self.target_monitor_idx = int(choice) - 1
        self._store.update(target_monitor_idx = self.target_monitor_idx)
        
        
    def _update_window(self):
        if self.status_label and self.status_label.winfo_exists():
            self.status_label.configure(text=self.get_status())
                    
            
    def get_status(self) -> str:
        return  f"Status : {self._store.state.connection.name}"
    
    def _generate_offset(self, window:BaseWindow):
        #calculate offset
        min_x = self.target_monitor.x + 100
        min_y = self.target_monitor.y + 100
        max_x = self.target_monitor.x + self.target_monitor.width - 100 - window.width
        max_y = self.target_monitor.y + self.target_monitor.height - 100 - window.height
        x_offset = random.randint(min_x, max_x)
        y_offset = random.randint(min_y, max_y)
        return (x_offset, y_offset)
    
    def show_window(self, window:BaseWindow):
        new_window : BaseWindow = window(self.root, self._config.ASSET_DIR)
        
        x_offset, y_offset = self._generate_offset(window=new_window)
        new_window.set_offset(x_offset,y_offset)
        new_window.spawn()
        
        # windows need to be kept in reference or else images don't show up
        # weird ass bug
        self.opened_windows.append(new_window)
    
    def show_random_window(self):
        window_values = list(self.window_types.values())
        new_window : BaseWindow = random.choice(window_values)(self.root, self._config.ASSET_DIR)
        x_offset, y_offset = self._generate_offset(window=new_window)
        new_window.set_offset(x_offset,y_offset)
        new_window.spawn()
        
        # windows need to be kept in reference or else images don't show up
        # weird ass bug
        self.opened_windows.append(new_window)
        
    def create_config_window(self):
        if self.config_window:
            return
        
        window = ctk.CTkToplevel(self.root)
        self.config_window = window
        
        window.title("ray-virus-config")
        window.protocol("WM_DELETE_WINDOW", lambda:(window.destroy(), setattr(self, "status_label",None), setattr(self, "config_window", None)))
        
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
        self.enabled_var = ctk.BooleanVar(value=self._store.state.redeems_enabled)
        ctk.CTkCheckBox(gen_setting_tab, text="Enable Redeems",
                       variable=self.enabled_var,
                       command=lambda: self._store.update(redeems_enabled=not self._store.state.redeems_enabled)
                       ).pack()
        ctk.CTkLabel(gen_setting_tab, text="Redeem Name").pack()
        
        redeem_name_strvar = ctk.StringVar(gen_setting_tab, value=self._store.state.redeem_name)
        redeem_name_strvar.trace_add("write", lambda var_name, index, mode : (self._store.update(redeem_name=redeem_name_strvar.get())))
        ctk.CTkEntry(gen_setting_tab, placeholder_text="Redeem Name", textvariable=redeem_name_strvar).pack()
        
        ctk.CTkLabel(master = gen_setting_tab, text="Monitor:").pack()
        option_menu = ctk.CTkOptionMenu(master = gen_setting_tab,
                          values=[str(x) for x in range(1, len(self.monitors)+1)],
                          command=self._on_change_monitor
                          )
        option_menu.pack()
        option_menu.set(f"{self._store.state.target_monitor_idx + 1}")
        
        
        
        # window list
        self.window_scrollable = ctk.CTkScrollableFrame(master = window_list_tab)
        self.window_scrollable.pack()
        for name, win in self.window_types.items():
            button = ctk.CTkButton(self.window_scrollable, text=name, command=lambda x=win:self.show_window(window=x))
            button.pack()
        
        # streamerbot settings
        self.status_label = ctk.CTkLabel(sb_setting_tab, text=self.get_status())
        self.status_label.pack()
        
        ctk.CTkLabel(sb_setting_tab, text="Websocket Address : ").pack()
        socket_address_strvar = ctk.StringVar(sb_setting_tab, value=self._store.state.streamerbot_address)
        socket_address_strvar.trace_add("write", lambda var_name, index, mode: (self._store.update(streamerbot_address=socket_address_strvar.get())))
        ctk.CTkEntry(sb_setting_tab, placeholder_text="Websocket Address", textvariable=socket_address_strvar).pack()
        
        ctk.CTkLabel(sb_setting_tab, text="WebSocket Password (empty if no pw): ").pack()
        socket_pw_strvar = ctk.StringVar(sb_setting_tab, value=self._store.state.streamerbot_pw)
        socket_pw_strvar.trace_add("write", lambda var_name, index, mode: (self._store.update(streamerbot_pw=socket_pw_strvar.get())))
        ctk.CTkEntry(sb_setting_tab, placeholder_text="Websocket Address", textvariable=socket_pw_strvar, show="*").pack()
        
        
        self.auto_start = ctk.BooleanVar(value=self._store.state.auto_start_socket)
        ctk.CTkCheckBox(sb_setting_tab, text="Auto-Start Websocket",
                       variable=self.auto_start,
                       command=lambda : self._store.update(auto_start_socket=self.auto_start.get())
                       ).pack()
        ctk.CTkButton(sb_setting_tab, text="Connect", command=lambda: self._on_connect_click()).pack()
    
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
        

    


   