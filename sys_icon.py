from PIL import Image
from pystray import Icon, Menu, MenuItem
from typing import Callable
from socket_clients import StreamerBotClient

class RaySystemIcon:
    """
    Window Manager for Ray Virus
    Opens ray viruses
    """
    def __init__(self,config,  manager, websocket_client):
        self.config = config
        self.virus_enabled = True
        self.running = False
        self._on_config_func : Callable = None
        self.manager = manager
        self.websocket_client : StreamerBotClient = websocket_client
        
        menu = Menu(
                MenuItem("Enable", self._toggle_virus, checked=lambda x : self.virus_enabled),
                MenuItem(self.get_status_string, action=None),
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
    
    def get_status_string(self, item) -> str:
        return f"Streamerbot Status : {self.websocket_client.get_status().name}"

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
        
    def update(self):
        self.icon.update_menu()