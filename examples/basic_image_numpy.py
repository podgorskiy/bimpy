import sys
import os

if os.path.exists("../cmake-build-debug/"):
    print('Running Debugging session!')
    sys.path.insert(0, "../cmake-build-debug/")

import bimpy
from PIL import Image
import numpy as np

ctx = bimpy.Context()
ctx.init(800, 800, "Image")

image = np.asarray(Image.open("3.png"), dtype=np.uint8)
im = bimpy.Image(image)

while not ctx.should_close():
    with ctx:
        bimpy.text("Display Image of type:")
        bimpy.same_line()
        bimpy.text(str(type(image)))
        bimpy.image(im)
