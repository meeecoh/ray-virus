import customtkinter as ctk
from PIL import Image, ImageOps
from ray_virus.audio import SoundPlayer
import pygame 
from typing import List


class BaseWindow:
    """
    Base class for all VirusWindows
    Implement the window using the create_window() method
    
    """
    def __init__(self, root, asset_dir, sound:SoundPlayer):
        self.root : ctk.CTkToplevel = ctk.CTkToplevel(root)
        self.title : str 
        self.width : int
        self.height : int
        self.ASSET_DIR = asset_dir
        self.sound = sound
        self._played_sounds :List[pygame.Channel] = []
        
        self.root.title(self.title)
        
        self.root.attributes("-topmost", True)
        self.root.focus_force()
        
        #closing protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.closed = False
        
        # hide initial window creation
        self.root.withdraw()
        self.create_window()
        self.root.update_idletasks()
        
    def set_offset(self, xoffset:int, yoffset:int):
        self.x_offset = xoffset
        self.y_offset = yoffset
        
    def set_geometry(self):
        self.root.geometry(f"{self.width}x{self.height}+{self.x_offset}+{self.y_offset}")
    
    def spawn(self):
        # show the window
        self.root.geometry(f"+{self.x_offset}+{self.y_offset}")
        self.root.deiconify()
        self.audio()
        
    def play_audio(self, name):
        self._played_sounds.append(self.sound.play(name))
    
    def audio(self):
        raise NotImplementedError(f"Class {type(self).__name__} must define the audio method")
    
    def create_window(self):
        raise NotImplementedError(f"Class {type(self).__name__} must define the create_window method")
    
    def on_close(self):
        self.closed=True
        for channel in self._played_sounds:
            channel.stop()
        self.root.destroy()
        
        
class RayWindow(BaseWindow):
    def __init__(self, root, ASSET_DIR, sound):
        self.root = root
        self.title="SYSTEM FAILURE"
        self.width = 600
        self.height = 450
        super().__init__(root, ASSET_DIR, sound)
        
    def audio(self):
        self.play_audio("alarm.mp3")
        
    def create_window(self):
        #disable resizing
        self.root.resizable(False, False)
        
        img_max_size = (600,600)
        image_asset = Image.open(self.ASSET_DIR/"img"/"RayVirusOriginal.png")
        resized = ImageOps.contain(image_asset, img_max_size, method=Image.Resampling.LANCZOS)
        ctk_image = ctk.CTkImage(light_image=resized, dark_image=resized, size=(resized.width, resized.height))
        ctk.CTkLabel(master=self.root, text="", image=ctk_image).pack()
        
class HotMochisRayWindow(BaseWindow):
    def __init__(self, root, ASSET_DIR, sound):
        self.root = root
        self.title="HOT MOCHIS IN YOUR AREA!"
        self.width = 600
        self.height = 450
        super().__init__(root, ASSET_DIR, sound)
        
    def audio(self):
        return
        
    def create_window(self):
        #disable resizing
        self.root.resizable(False, False)
        
        img_max_size = (600,600)
        image_asset = Image.open(self.ASSET_DIR/"img"/"HotMochisRay.png")
        resized = ImageOps.contain(image_asset, img_max_size, method=Image.Resampling.LANCZOS)
        ctk_image = ctk.CTkImage(light_image=resized, dark_image=resized, size=(resized.width, resized.height))
        ctk.CTkLabel(master=self.root, text="", image=ctk_image).pack()
        
class CongratsNewComputer(BaseWindow):
    def __init__(self, root, ASSET_DIR, sound):
        self.root = root
        self.title="HOT MOCHIS IN YOUR AREA!"
        self.width = 600
        self.height = 450
        super().__init__(root, ASSET_DIR, sound)
    
    def audio(self):
            return
        
    def create_window(self):
        #disable resizing
        self.root.resizable(False, False)
        
        img_max_size = (600,600)
        image_asset = Image.open(self.ASSET_DIR/"img"/"CongratsNewComputer.png")
        resized = ImageOps.contain(image_asset, img_max_size, method=Image.Resampling.LANCZOS)
        ctk_image = ctk.CTkImage(light_image=resized, dark_image=resized, size=(resized.width, resized.height))
        ctk.CTkLabel(master=self.root, text="", image=ctk_image).pack()