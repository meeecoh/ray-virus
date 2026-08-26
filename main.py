
import asyncio
import tkinter as tk

import window
from config import Config
from manager import VirusManager
from socket_clients import StreamerBotClient
from stores import AppStore
from sys_icon import RaySystemIcon


async def event_loop(manager:VirusManager, icon):
    # custom event loop for updating tkinter
    while icon.running:
        try:
            manager.root.update_idletasks()
            manager.root.update()
            manager.check_queue()
            
            # remove already closed windows
            manager.clear_window_list()
            
            await asyncio.sleep(1/30) #30fps
        except tk.TclError:
            break

async def main():
        # setup manager, streamerbot, and systemIcons
        c = Config()
        s = AppStore()
        
        manager = VirusManager(config=c, store=s)
        sb_client = StreamerBotClient(config=c, store=s)
        icon = RaySystemIcon(config=c, manager=manager, store=s)
        
        s.subscribe(manager.on_state_update)
        s.subscribe(icon.on_state_update)
        
        
        ### register windows
        manager.register_window("ray_virus", window.RayWindow)
        
        ### register redeem events
        sb_client.register_redeem(c.get('redeem_name'), lambda x: manager.show_random_window())
        
        #run system icon in other thread
        icon.run_detached()
        
        # run tk event loop and websocket
        await asyncio.gather(
            event_loop(manager, icon),
            sb_client.run_client()
        )
        
        
if __name__ == "__main__":
    asyncio.run(main())
    