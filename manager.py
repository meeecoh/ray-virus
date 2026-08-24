import asyncio
import threading
from socket_clients import StreamerBotClient
from sys_icon import RaySystemIcon
from window import activate_virus, BaseWindow
import tkinter as tk
from tkinter import Label
from typing import Dict
from time import sleep

class VirusManager:
    def __init__(self):
        self._num_windows = 0
        self.display = ""
        self.window_types : Dict[str, BaseWindow] = {}
        self.root = tk.Tk()
        self.root.withdraw() # background parent tkinter window
    
    def register_window(self, name, window:BaseWindow):
        pass
    
    def create_random_window(self):
        pass
    
    def create_window(self, name:str):
        pass
        
    def create_config_window(self):
        window = tk.Toplevel(self.root)
        window.title("ray-virus-config")
        window.geometry("300x150")
        
        tk.Checkbutton(window, text="Enable Virus").pack()
        tk.Label(window, text=f"StreamerBot Status : disconnected").pack()
        tk.Entry(window, width=30).pack()
        tk.Button(window, text=f"Connect").pack()


if __name__ == "__main__":
    
    # create and run system icon
    icon = RaySystemIcon()
    icon.run_detached()
    
    # create manager
    manager = VirusManager()
    manager.create_config_window()
    
    # setup streamerbot client async
    sb_client = StreamerBotClient()
    
    #register redeem events
    sb_client.register_redeem("hydrate!", lambda x: print("hydrating!"))
    
    asyncio.run(sb_client.run_client())
    
    # custom event loop for updating tkinter
    while icon.running:
        try:
            manager.root.update_idletasks()
            manager.root.update()
            sleep(1/30) #30fps
        except tk.TclError:
            break

   