import sys 
import ctypes 
from tendo import singleton

appid = 'meeecoh.rayvirus'

if sys.platform == "win32":
    try :
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        ctypes.windll.user32.SetProcessDPIAware()
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
        
try : 
    ray_virus = singleton.SingleInstance()
except singleton.SingleInstanceException:
    print("Another instance of this program is already running. Exiting...")
    sys.exit(1)

import asyncio
import tkinter as tk
from pathlib import Path

from ray_virus import window
from ray_virus.config import Config
from ray_virus.manager import VirusManager
from ray_virus.socket_clients import StreamerBotClient
from ray_virus.stores import AppStore
from ray_virus.sys_icon import RaySystemIcon
from ray_virus.audio import SoundPlayer


async def event_loop(manager:VirusManager, store:AppStore):
    # custom event loop for updating tkinter
    while store.state.running:
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
        BASE_DIR = Path(__file__).resolve().parent
        c = Config(BASE_DIR)
        s = AppStore()
        
        sound = SoundPlayer(c.ASSET_DIR/"sounds")
        manager = VirusManager(config=c, store=s, sound=sound)
        sb_client = StreamerBotClient(config=c, store=s)
        icon = RaySystemIcon(config=c, manager=manager, store=s)
        
        # init data in store using config vals
        s.update(redeems_enabled=c.get("redeems_enabled"))
        s.update(redeem_name=c.get("redeem_name"))
        s.update(streamerbot_address = c.get("streamerbot_address"))
        s.update(streamerbot_pw = c.get("streamerbot_pw"))
        s.update(auto_start_socket = c.get("auto_start_socket"))
        s.update(target_monitor_idx = c.get("target_monitor_idx"))
        s.update(audio_lvl = c.get("audio_lvl"))
        
        
        # manage subscriptions
        s.subscribe(c.on_state_update)
        s.subscribe(manager.on_state_update)
        s.subscribe(icon.on_state_update)
        s.subscribe(sound.on_state_update)
        
        
        ### register windows
        manager.register_window("RayVirusOriginal", window.OriginalWindow)
        manager.register_window("RayVirus", window.RayWindow)
        manager.register_window("HotMochisRay", window.HotMochisRayWindow)
        manager.register_window("CongratsNewComputer", window.CongratsNewComputer)
        manager.register_window("ErrorWindow", window.ErrorWindow)
        
        ### register redeem events
        sb_client.register_redeem(c.get('redeem_name'), lambda x: manager.show_random_window())
        
        ### register callback on connect btn clicked
        manager.register_connect_callback(
            lambda: asyncio.create_task(sb_client.stop_and_restart())
        )
        
        #run system icon in other thread
        icon.run_detached()
        
        # run tk event loop and websocket
        if s.state.auto_start_socket:
            sb_client.start()
        await event_loop(manager=manager, store=s)
        await sb_client.stop()
        
        
if __name__ == "__main__":
    asyncio.run(main())
    