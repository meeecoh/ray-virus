import tkinter as tk 
from screeninfo import get_monitors
from pathlib import Path
from PIL import Image, ImageTk
import pygame 

class BaseWindow:
    def __init__(self):
        pass

def activate_virus():
    window_width = 600
    window_height = 450
    
    #init pygame
    pygame.init()
    pygame.mixer.init()

    #play sound
    alarm_sound_path = Path("asset/alarm.mp3")
    alarm_sound = pygame.mixer.Sound(alarm_sound_path)
    alarm_sound.play()

    #window is created
    root = tk.Tk()
    root.title("VIRUS INBOUND!!!!")
    font = ("Arial", 36)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    #get position of monitors
    monitors = get_monitors()
    monitor_index = 1
    target_monitor = monitors[monitor_index]
    x_offset = target_monitor.x + (target_monitor.width - window_width) //2
    y_offset = target_monitor.y + (target_monitor.height - window_height) //2
    
    #set window position
    root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

    # window content
    tk.Label(root, text="THIS IS A VIRUS", font=font, bg="black", fg="red").grid(row=0, column=0, sticky="nsew")

    #image
    image_path=Path("asset/you_hacked.png")
    pil_image = Image.open(image_path).resize((300,300))
    tk_image = ImageTk.PhotoImage(pil_image)
    image_label = tk.Label(root, image=tk_image, bg="black").grid(row=1, column=0, sticky="nsew")

    #owned label
    tk.Label(root, text="YOU'VE BEEN OWNED", font=font, bg="black", fg="red").grid(row=2, column=0, sticky="nsew")

    root.attributes("-topmost", True)
    root.focus_force()
    root.configure(bg="black")
    root.iconphoto(True, tk_image)

    root.mainloop()
    
if __name__ == "__main__":
    activate_virus()