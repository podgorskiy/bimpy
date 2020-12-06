import bimpy
from PIL import Image

ctx = bimpy.Context()
ctx.init(800, 800, "Image")

image = Image.open("3.png")
im = bimpy.Image(image)

while not ctx.should_close():
    with ctx:
        bimpy.text("Display PIL Image")
        bimpy.image(im)
