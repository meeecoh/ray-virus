from PIL import Image
from pystray import Icon, Menu, MenuItem

class RaySystemIcon:
    """
    Window Manager for Ray Virus
    Opens ray viruses
    """
    def __init__(self):
        self.virus_enabled = True
        self.running = False
        
        menu = Menu(
                MenuItem("Enable", self._toggle_virus, checked=lambda x : self.virus_enabled),
                MenuItem("Streamerbot Status : Disconnected", action=None),
                MenuItem("Connect", action=None),
                MenuItem("Config", action=None),
                MenuItem("Exit", self.on_exit)
            )
        
        self.icon = Icon(
            name="RayVirusManager",
            icon=Image.open("you_hacked.png").resize((64, 64)),
            title="Ray Virus Manager",
            menu=menu
        )

    def on_exit(self):
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