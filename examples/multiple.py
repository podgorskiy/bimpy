import bimpy

ctx = bimpy.Context()
ctx.init(600, 600, "First context")
ctx.clear_color = (0.0, 0.5, 0.0, 1.0)

while(not ctx.should_close()):
    with ctx:
        if bimpy.begin("First window"):
            bimpy.text("Hello, world!")

            if bimpy.button("Close"):
                break
        bimpy.end()

        bimpy.show_demo_window()
# Terminate the context to ensure the window is closed.
ctx.terminate()


ctx = bimpy.Context()
ctx.init(800, 800, "Second context")
ctx.clear_color = (0.0, 0.0, 0.5, 1.0)

while(not ctx.should_close()):
    with ctx:
        if bimpy.begin("Second window"):
            bimpy.text("Hello world, again!")

            if bimpy.button("Close"):
                break
        bimpy.end()
ctx.terminate()
