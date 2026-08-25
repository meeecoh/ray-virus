from PIL import Image
from pystray import Icon, Menu, MenuItem
from typing import Callable

class RaySystemIcon:
    """
    Window Manager for Ray Virus
    Opens ray viruses
    """
    def __init__(self, manager, websocket_client):
        self.virus_enabled = True
        self.running = False
        self._on_config_func : Callable = None
        self.manager = manager
        self.websocket_client = websocket_client
        
        menu = Menu(
                MenuItem("Enable", self._toggle_virus, checked=lambda x : self.virus_enabled),
                MenuItem("Streamerbot Status : Disconnected", action=None),
                MenuItem("Connect", action=None),
                MenuItem("Config", action=lambda : self.manager.cmd_queue.put("CREATE_CONFIG_WINDOW")),
                MenuItem("Exit", self._on_exit)
            )
        
        self.icon = Icon(
            name="RayVirusManager",
            icon=Image.open("asset/you_hacked.png").resize((64, 64)),
            title="Ray Virus Manager",
            menu=menu
        )
    

    def _on_exit(self):
        """Stops tray application loop"""
        self.icon.stop()
        self.running = False
        
    def run_detached(self):
        """Run loop handling events detached"""
        self.running = True
        self.icon.run_detached()
        
    def run(self):
        """Run icon events"""
        self.running = True
        self.icon.run()

    def _toggle_virus(self):
        self.virus_enabled =  not self.virus_enabled