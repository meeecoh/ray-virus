import os 
from PIL import Image
from pystray import Icon, Menu, MenuItem
from time import sleep


"""
Window Manager for Ray Virus
Opens ray viruses
"""
def on_action():
    pass

def on_exit():
    """Stops tray application loop"""
    icon.stop()
    global program_running
    program_running = False
    
    
def toggle_virus():
    global virus_enabled
    virus_enabled =  not virus_enabled

program_running = True
virus_enabled = True
virus_menu_toggle = MenuItem("Enable Virus", toggle_virus, checked=lambda x : virus_enabled)

# define menu
menu = Menu(
    virus_menu_toggle,
    MenuItem("Exit", on_exit)
)

# define icon
icon = Icon(
    name="RayVirusManager",
    icon=Image.open("you_hacked.png").resize((64, 64)),
    title="Ray Virus Manager",
    menu=menu
)

if __name__ == "__main__":
    icon.run_detached()
    
    while program_running:
        sleep(1/30)
        print(virus_enabled)