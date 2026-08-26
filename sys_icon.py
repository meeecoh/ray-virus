
from PIL import Image
from pystray import Icon, Menu, MenuItem

from stores import AppState, AppStore, ConnectionState


class RaySystemIcon:
    """
    Window Manager for Ray Virus
    Opens ray viruses
    """
    def __init__(self,config,  manager, store:AppStore):
        self.config = config
        self.running = False
        self.manager = manager
        self._store = store
        self._status = ConnectionState.DISCONNECTED
        
        menu = Menu(
                MenuItem("Enabled",
                         checked=lambda x : self._store.state.enabled,
                         action=lambda x: self._store.update(enabled=(not self._store.state.enabled))),
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
        return f"Streamerbot Status : {self._status.name}"

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
        
    def on_state_update(self, new_state: AppState):
        self._status = new_state.connection
        self.icon.update_menu()
