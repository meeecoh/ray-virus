import asyncio
import threading
from socket_clients import StreamerBotClient
from sys_icon import RaySystemIcon
from window import activate_virus, BaseWindow
import tkinter as tk
from tkinter import Label
from typing import Dict
from time import sleep
import queue


class VirusManager:
    """Virus Window Manager"""
    def __init__(self):
        self._num_windows = 0
        self.display = ""
        self.window_types : Dict[str, BaseWindow] = {}
        
        self.root = tk.Tk()
        self.root.withdraw() # background parent tkinter window
        
        self.cmd_queue = queue.Queue()
    
    def register_window(self, name, window:BaseWindow):
        pass
    
    def show_random_window(self):
        pass
    
    def show_window(self, name:str):
        pass
        
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
    

if __name__ == "__main__":
    
    # create and run system icon
    manager = VirusManager()
    icon = RaySystemIcon(manager=manager)
    
    
    # streamerbot websockets
    sb_client = StreamerBotClient()
    #register redeem events
    sb_client.register_redeem("enable ray virus", lambda x: activate_virus())
    
    #run system icon and websocket client
    icon.run_detached()
    # asyncio.run(sb_client.run_client())
    
    # custom event loop for updating tkinter
    while icon.running:
        try:
            manager.root.update_idletasks()
            manager.root.update()
            manager.check_queue()
            sleep(1/30) #30fps
        except tk.TclError:
            break

   