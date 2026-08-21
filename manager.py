import os 
from PIL import Image
from pystray import Icon, Menu, MenuItem
from time import sleep


class RaySystemIcon:
    """
    Window Manager for Ray Virus
    Opens ray viruses
    """
    def __init__(self):
        self.virus_enabled = True
        self.running = False
        
        virus_menu_toggle = MenuItem("Enable Virus", self.toggle_virus, checked=lambda x : self.virus_enabled)
        menu = Menu(
                virus_menu_toggle,
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
        
        
    def toggle_virus(self):
        self.virus_enabled =  not self.virus_enabled
        
    def run_detached(self):
        """Run loop handling events detached"""
        self.running = True
        self.icon.run_detached()
        
    def run(self):
        """Run icon events"""
        self.running = True
        self.icon.run()



if __name__ == "__main__":
    icon = RaySystemIcon()
    icon.run_detached()
    
    while icon.running:
        sleep(1/12)
        print(icon.virus_enabled)