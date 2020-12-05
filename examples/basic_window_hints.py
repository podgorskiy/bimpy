import sys
import os

if os.path.exists("../cmake-build-debug/"):
    print('Running Debugging session!')
    sys.path.insert(0, "../cmake-build-debug/")
import bimpy

ctx = bimpy.Context()

ctx.init(600, 600, "Hello", decorated=False)

str = bimpy.String()
f = bimpy.Float()

while not ctx.should_close():
    with ctx:
        bimpy.text("Hello, world!")

        if bimpy.button("OK"):
            print(str.value)

        bimpy.input_text('string', str, 256)

        bimpy.slider_float("float", f, 0.0, 1.0)
