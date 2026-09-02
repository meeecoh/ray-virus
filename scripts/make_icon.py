from PIL import Image 
from pathlib import Path

img = Image.open("../src/assets/img/you_hacked.png")

icon_sizes = [
    (16,16),
    (32,32),
    (64,64),
    (128,128),
    (256,256)
]
img.save("../src/assets/img/ray_icon.ico", format="ICO", sizes=icon_sizes)