import asyncio
import threading
from socket_clients import StreamerBotClient
from sys_icon import RaySystemIcon
from window import activate_virus, BaseWindow
import tkinter as tk
from tkinter import Label
from typing import Dict
from time import sleep

class Manager:
    def __init__(self):
        self._num_windows = 0
        self.display = ""
        self.window_types : Dict[str, BaseWindow] = {}
        self.root = tk.Tk()
        self.root.withdraw()
    
    def register_window(self, name, window:BaseWindow):
        pass
        
    def create_config_window(self):
        window = tk.Toplevel(self.root)
        window.title("ray-virus-config")
        window.geometry("300x150")
        
        tk.Checkbutton(window, text="")


if __name__ == "__main__":
    
    icon = RaySystemIcon()
    icon.run_detached()
    manager = Manager()
    
    manager.create_config_window()
    
    # custom event loop
    while icon.running:
        try:
            manager.root.update_idletasks()
            manager.root.update()
            sleep(1/30) #30fps
        except tk.TclError:
            break
        
    
    # register window types in a list
    
    # # run system icon in separate thread
    
    
    # # setup streamerbot client
    # sb_client = StreamerBotClient()
    
    
    # asyncio.run(sb_client.run_client())
    pass
   