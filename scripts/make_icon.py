from PIL import Image 
from pathlib import Path

img_path = Path("../src/assets/img/you_hacked.png")
img = Image.open(img_path)

icon_sizes = [
    (16,16),
    (32,32),
    (64,64),
    (128,128),
    (256,256)
]
img.save("ray_icon.ico", format="ICO", sizes=icon_sizes)