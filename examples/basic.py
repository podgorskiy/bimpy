import bimpy

ctx = bimpy.Context()

ctx.init(600, 600, "Hello")

str = bimpy.String()
f = bimpy.Float()

while not ctx.should_close():
    with ctx:
        bimpy.text("Hello, world!")

        if bimpy.button("OK"):
            print(str.value)

        bimpy.input_text('string', str, 256)

        bimpy.slider_float("float", f, 0.0, 1.0)
