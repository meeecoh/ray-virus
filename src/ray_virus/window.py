import customtkinter as ctk
from PIL import Image


class BaseWindow:
    """
    Base class for all VirusWindows
    Implement the window using the create_window() method
    
    """
    def __init__(self, root, x_offset, y_offset, ASSET_DIR):
        self.root = ctk.CTkToplevel(root)
        self.title : str 
        self.width : int
        self.height : int
        self.ASSET_DIR = ASSET_DIR
        
        self.create_window()
        self.root.title(self.title)
        self.root.geometry(f"{self.width}x{self.height}+{x_offset}+{y_offset}")
        self.root.attributes("-topmost", True)
        self.root.focus_force()
        
        #closing protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.closed = False
    
    def create_window(self):
        raise NotImplementedError(f"Class {self.__name__} must define the create_window method")
    
    def on_close(self):
        self.closed=True
        self.root.destroy()
        
        
class RayWindow(BaseWindow):
    def __init__(self, root, x_offset, y_offset, ASSET_DIR):
        self.root = root
        self.title="RAY HAS INVADED!"
        self.width = 600
        self.height = 450
        super().__init__(root, x_offset, y_offset, ASSET_DIR)
        
    def create_window(self):
        font = ("Arial", 36)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        # window content
        ctk.CTkLabel(self.root, text="THIS IS A VIRUS", font=font, fg_color="black", text_color="red").pack()
        #image
        image_asset = Image.open(self.ASSET_DIR/"you_hacked.png")
        self.ctk_image = ctk.CTkImage(light_image=image_asset, dark_image=image_asset, size=(300,300))
        self.image_label = ctk.CTkLabel(self.root, text="", image=self.ctk_image, fg_color="black").pack()
        
        #owned label
        ctk.CTkLabel(self.root, text="YOU'VE BEEN OWNED", font=font, fg_color="black", text_color="red").pack()