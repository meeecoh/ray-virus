
from PIL import Image
from pystray import Icon, Menu, MenuItem

from .config import Config
from .stores import AppState, AppStore, ConnectionState
from .manager import VirusManager


class RaySystemIcon:
    """
    Window Manager for Ray Virus
    Opens ray viruses
    """
    def __init__(self,config:Config,  manager:VirusManager, store:AppStore):
        self.manager : VirusManager = manager
        self._config : Config = config
        self._store : AppStore = store
        self._status : ConnectionState = ConnectionState.DISCONNECTED
        
        menu = Menu(
                MenuItem("Enable Redeems",
                         checked=lambda x : self._store.state.redeems_enabled,
                         action=lambda x: self._on_enable_redeems,
                ),
                MenuItem(self.get_status_string, action=None, enabled=False),
                MenuItem("Open Config", action=lambda : self.manager.cmd_queue.put("CREATE_CONFIG_WINDOW"), default=True),
                MenuItem("Quit", self._on_quit)
            )
        
        self.icon = Icon(
            name="RayVirusManager",
            icon=Image.open(self._config.ASSET_DIR/"img"/"you_hacked.png").resize((64, 64)),
            title="Ray Virus Manager",
            menu=menu
        )
        
    def _on_enable_redeems(self):
        self.manager.cmd_queue.put(("STORE_UPDATE", {"redeems_enabled" : not self._store.state.redeems_enabled}))
    
    def get_status_string(self, item) -> str:
        return f"Streamerbot Status : {self._status.name}"

    def _on_quit(self):
        """Stops tray application loop"""
        self.icon.stop()
        self.manager.cmd_queue.put(("STORE_UPDATE",{"running":False}))
        
    def run_detached(self):
        """Run loop handling events detached"""
        self.icon.run_detached()
    

    def _toggle_virus(self):
        self.virus_enabled =  not self.virus_enabled
        
    def on_state_update(self, new_state: AppState):
        self._status = new_state.connection
        self.icon.update_menu()
