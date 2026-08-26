import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk


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
        
        #closing protocol
        root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.closed = False
    
    def create_window(self):
        raise NotImplementedError(f"Class {self.__name__} must define the create_window method")
    
    def on_close(self):
        print("window closed!")
        self.closed=True
        
        
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
        self.image_path=Path("asset/you_hacked.png")
        self.tk_image = ImageTk.PhotoImage(Image.open("asset/you_hacked.png").resize((300,300)))
        self.image_label = tk.Label(self.root, image=self.tk_image, bg='black').pack()
        
        #owned label
        tk.Label(self.root, text="YOU'VE BEEN OWNED", font=font, bg="black", fg="red").pack()

    
if __name__ == "__main__":
    base = tk.Tk()
    window = RayWindow(base, 500, 100)
    base.mainloop()