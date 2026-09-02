import queue
import random
from collections.abc import Callable
import webbrowser

import customtkinter as ctk
import tkinter as ttk
from screeninfo import Monitor, get_monitors

from ray_virus.audio import SoundPlayer

from .config import Config
from .stores import AppState, AppStore, ConnectionState
from .window import BaseWindow


class VirusManager:
    """Virus Window Manager"""
    def __init__(self, config : Config, store : AppStore, sound:SoundPlayer):
        self._num_windows = 0
        self.opened_windows=[]
        self.window_types : dict[str, BaseWindow] = {}
        
        self._config = config
        self._store = store
        self._sound = sound
        self._status = ConnectionState.DISCONNECTED
        self.status_label = None
        
        self.config_window = None
        
        # tkinter
        self.root = ctk.CTk()
        
        self.app_icon = ttk.PhotoImage(file=self._config.ASSET_DIR/"img"/"you_hacked.png")
        self.root.iconphoto(True, self.app_icon)
        
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
        x_pad, y_pad = (300, 300)
        win_width = window.root.winfo_reqwidth()
        win_height = window.root.winfo_reqheight()
        min_x = self.target_monitor.x + x_pad
        min_y = self.target_monitor.y + y_pad
        max_x = self.target_monitor.x + self.target_monitor.width - x_pad - win_width
        max_y = self.target_monitor.y + self.target_monitor.height - y_pad - win_height
        x_offset = random.randint(min_x, max_x)
        y_offset = random.randint(min_y, max_y)
        return (x_offset, y_offset)
    
    def show_window(self, window:BaseWindow):
        new_window : BaseWindow = window(self.root, self._config.ASSET_DIR, self._sound)
        
        x_offset, y_offset = self._generate_offset(window=new_window)
        new_window.set_offset(x_offset,y_offset)
        new_window.spawn()
        
        # windows need to be kept in reference or else images don't show up
        # weird ass bug
        self.opened_windows.append(new_window)
    
    def show_random_window(self):
        window_values = list(self.window_types.values())
        new_window : BaseWindow = random.choice(window_values)(self.root, self._config.ASSET_DIR, self._sound)
        x_offset, y_offset = self._generate_offset(window=new_window)
        new_window.set_offset(x_offset,y_offset)
        new_window.spawn()
        
        # windows need to be kept in reference or else images don't show up
        # weird ass bug
        self.opened_windows.append(new_window)
        
    def create_config_window(self):
        if self.config_window:
            self.config_window.focus_force()
            return
        
        window = ctk.CTkToplevel(self.root)
        window.after(200, lambda: window.wm_iconphoto(False, self.app_icon))
        window.withdraw()
        self.config_window = window
        
        window.title("ray-virus-config")
        window.protocol("WM_DELETE_WINDOW", lambda:(window.destroy(), setattr(self, "status_label",None), setattr(self, "config_window", None)))
        window.resizable(False, False)
        window.grid_columnconfigure(0,weight=1)
        
        # tab control
        tabControl = ctk.CTkTabview(master=window, fg_color="transparent")
        tabControl.add('General')
        tabControl.add("Streamerbot")
        tabControl.add("Windows")
        tabControl.add("Credits")
        tabControl.grid(row=0, column=0)
        
        gen_setting_tab = tabControl.tab("General")
        window_list_tab = tabControl.tab("Windows")
        sb_setting_tab = tabControl.tab("Streamerbot")
        credits_tab = tabControl.tab("Credits")
        
        
        
        # general settings        
        self.enabled_var = ctk.BooleanVar(value=self._store.state.redeems_enabled)
        ctk.CTkCheckBox(gen_setting_tab, text="Enable Redeems",
                       variable=self.enabled_var,
                       command=lambda: self._store.update(redeems_enabled=not self._store.state.redeems_enabled)
                       ).grid(row=1, column=0, pady=(20,0))
        
        # options grid
        grid_frame = ctk.CTkFrame(gen_setting_tab, fg_color="transparent")
        grid_frame.grid(row=2, column=0, padx=20, pady=10)
        
        ctk.CTkLabel(grid_frame, text="Redeem Name").grid(row=0, column=0, sticky="w")
        
        redeem_name_strvar = ctk.StringVar(gen_setting_tab, value=self._store.state.redeem_name)
        redeem_name_strvar.trace_add("write", lambda var_name, index, mode : (self._store.update(redeem_name=redeem_name_strvar.get())))
        ctk.CTkEntry(
            grid_frame, 
            placeholder_text="Redeem Name:", 
            textvariable=redeem_name_strvar
            ).grid(row=0, column=1, sticky="ew", padx=20)
        
        ctk.CTkLabel(master = grid_frame, text="Monitor:").grid(row=1, column=0, pady=10, sticky="w")
        option_menu = ctk.CTkOptionMenu(
                        master = grid_frame,
                        values=[str(x) for x in range(1, len(self.monitors)+1)],
                        command=self._on_change_monitor
                        )
        option_menu.grid(row=1, column=1, sticky="ew", padx=20)
        option_menu.set(f"{self._store.state.target_monitor_idx + 1}")
        
        ctk.CTkButton(
            master=gen_setting_tab, 
            text="clear all windows",
            command=lambda : [w.on_close() for w in self.opened_windows]
            ).grid(row=3, column=0)
        
        
        
        # window list
        self.window_scrollable = ctk.CTkScrollableFrame(master = window_list_tab, fg_color="transparent")
        self.window_scrollable.pack(expand=True, fill="both", anchor="center", padx=20, pady=10)
        for name, win in self.window_types.items():
            button = ctk.CTkButton(self.window_scrollable, text=name, command=lambda x=win:self.show_window(window=x))
            button.pack()
        
        
        # streamerbot settings
        sb_setting_frame = ctk.CTkFrame(sb_setting_tab, fg_color="transparent")
        sb_setting_frame.pack(expand=True, fill="both", padx=20, pady=10)
        sb_setting_frame.grid_columnconfigure((0,1), weight=1, pad=20)
        sb_setting_frame.grid_rowconfigure((0,1,2,3,4), weight=1, pad=10)
        
        self.status_label = ctk.CTkLabel(sb_setting_frame, text=self.get_status())
        self.status_label.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        ctk.CTkLabel(sb_setting_frame, text="Address : ").grid(row=1, column=0, sticky="w")
        socket_address_strvar = ctk.StringVar(sb_setting_frame, value=self._store.state.streamerbot_address)
        socket_address_strvar.trace_add("write", lambda var_name, index, mode: (self._store.update(streamerbot_address=socket_address_strvar.get())))
        ctk.CTkEntry(sb_setting_frame, 
                     placeholder_text="Websocket Address", 
                     textvariable=socket_address_strvar
                     ).grid(row=1, column=1)
        
        ctk.CTkLabel(sb_setting_frame, text="Password").grid(row=2, column=0, sticky="w")
        socket_pw_strvar = ctk.StringVar(sb_setting_frame, value=self._store.state.streamerbot_pw)
        socket_pw_strvar.trace_add("write", lambda var_name, index, mode: (self._store.update(streamerbot_pw=socket_pw_strvar.get())))
        ctk.CTkEntry(sb_setting_frame, 
                    placeholder_text="Websocket Address", 
                    textvariable=socket_pw_strvar, 
                    show="*").grid(row=2, column=1)
        
        
        self.auto_start = ctk.BooleanVar(value=self._store.state.auto_start_socket)
        ctk.CTkCheckBox(sb_setting_frame, text="Auto-Start Websocket",
                       variable=self.auto_start,
                       command=lambda : self._store.update(auto_start_socket=self.auto_start.get())
                       ).grid(row=3, column=0, columnspan=2)
        ctk.CTkButton(sb_setting_frame, 
                      text="Connect", 
                      command=lambda: self._on_connect_click()
                      ).grid(row=4, column=0, columnspan=2)
        
        #credits tab
        credit_frame = ctk.CTkFrame(credits_tab, fg_color="transparent")
        credit_frame.pack()
        
        credit_frame.grid_rowconfigure((0,1,2,3,4), weight=1)
        
        link_color = "#69a2ff"
        
        credit_label = ctk.CTkLabel(credit_frame, text="Created by meeecoh, 2026")
        credit_label.grid(row=0, column=0)
        ctk.CTkLabel(credit_frame, text="Thanks to all the mochis who got me this far").grid(row=1, column=0)
        
        youtube_link = ctk.CTkLabel(credit_frame, text="Youtube", text_color=link_color, cursor="hand2")
        youtube_link.grid(row=2, column=0)
        youtube_link.bind("<Button-1>", lambda e: self.hyperlink("https://www.youtube.com/@meeecoh"))
        
        twitch_link = ctk.CTkLabel(credit_frame, text="Twitch", text_color=link_color, cursor="hand2")
        twitch_link.grid(row=3, column=0)
        twitch_link.bind("<Button-1>", lambda e: self.hyperlink("https://www.twitch.tv/meeecoh"))
        
        discord_link = ctk.CTkLabel(credit_frame, text="Discord", text_color=link_color, cursor="hand2")
        discord_link.grid(row=4, column=0)
        discord_link.bind("<Button-1>", lambda e: self.hyperlink("https://discord.gg/PgHxkjFHv3"))
        
        github_link = ctk.CTkLabel(credit_frame, text="GitHub", text_color=link_color, cursor="hand2")
        github_link.grid(row=5, column=0)
        github_link.bind("<Button-1>", lambda e: self.hyperlink("https://github.com/Meeecoh"))
        
        #positioning
        window.update_idletasks()
        monitor = self.target_monitor
        x_offset = monitor.x +( monitor.width//2) - (window.winfo_reqwidth()//2)
        y_offset = monitor.y + (monitor.height//2) - (window.winfo_reqheight()//2)
        window.geometry(f"300x250+{x_offset}+{y_offset}")
        window.deiconify()
        
    def hyperlink(self, url):
        webbrowser.open_new(url)
    
    def show_config_window(self):
        self.root.after(0, self.create_config_window)
        
    def check_queue(self):
        """Runs on the Main Thread checking for cross-thread requests."""
        try:
            # Non-blocking pop to process all pending tray UI signals
            command = self.cmd_queue.get_nowait()
            
            if command == "CREATE_CONFIG_WINDOW":
                self.create_config_window()
                
            elif isinstance(command, tuple) and command[0] == "STORE_UPDATE":
                self._store.update(**command[1])
                
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
        

    


   