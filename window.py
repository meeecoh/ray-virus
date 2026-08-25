import tkinter as tk 
from screeninfo import get_monitors
from pathlib import Path
from PIL import Image, ImageTk
import pygame 

class BaseWindow:
    """
    Base class for all VirusWindows
    Implement the window using the create_window() method
    
    """
    def __init__(self, root, x_offset, y_offset):
        self.root = tk.Toplevel(root)
        self.title : str 
        self.width : int
        self.height : int 
        
        self.create_window()
        self.root.title(self.title)
        self.root.geometry(f"{self.width}x{self.height}+{x_offset}+{y_offset}")
        root.attributes("-topmost", True)
        root.focus_force()
    
    def create_window(self):
        raise NotImplemented(f"Class {self.__name__} must define the create_window method")
        
        
class RayWindow(BaseWindow):
    def __init__(self, root, x_offset, y_offset):
        self.root = root
        self.title="RAY HAS INVADED!"
        self.width = 600
        self.height = 450
        super().__init__(root, x_offset, y_offset)
        
    def create_window(self):
        font = ("Arial", 36)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        # window content
        tk.Label(self.root, text="THIS IS A VIRUS", font=font, bg="black", fg="red").pack()
        #image
        image_path=Path("asset/you_hacked.png")
        self.tk_image = ImageTk.PhotoImage(Image.open(image_path).resize((300,300)))
        self.image_label = tk.Label(self.root, image=self.tk_image, bg='black').pack()
        
        #owned label
        tk.Label(self.root, text="YOU'VE BEEN OWNED", font=font, bg="black", fg="red").pack()

    
if __name__ == "__main__":
    base = tk.Tk()
    window = RayWindow(base, 500, 100)
    base.mainloop()