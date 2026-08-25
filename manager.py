import asyncio
from socket_clients import StreamerBotClient
from sys_icon import RaySystemIcon
from window import activate_virus, BaseWindow
import tkinter as tk
from typing import Dict
import queue
from screeninfo import get_monitors
import random


class VirusManager:
    """Virus Window Manager"""
    def __init__(self):
        self._num_windows = 0
        self.window_types : Dict[str, BaseWindow] = {}
        
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
        random.choice(self.window_types.values())(self.root).create_window(x_offset, y_offset)
        
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

async def event_loop(manager, icon):
    # custom event loop for updating tkinter
    while icon.running:
        try:
            manager.root.update_idletasks()
            manager.root.update()
            manager.check_queue()
            await asyncio.sleep(1/30) #30fps
        except tk.TclError:
            break
    

async def main():
        # setup manager, streamerbot, and systemIcons
        manager = VirusManager()
        sb_client = StreamerBotClient()
        icon = RaySystemIcon(manager=manager, websocket_client=sb_client)
        
        ### register windows
        manager.register_window("ray_virus", )
        
        ### register redeem events
        sb_client.register_redeem("enable ray virus", lambda x: activate_virus())
        
        #run system icon and websocket client
        icon.run_detached()
        
        # run event loop async
        await asyncio.gather(
            event_loop(manager, icon),
            sb_client.run_client()
        )
        
        
        
    

if __name__ == "__main__":
    asyncio.run(main())
    

   