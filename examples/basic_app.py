import bimpy as bp


class App(bp.App):
    def __init__(self):
        super(App, self).__init__(title='Test')
        self.string = bp.String()
        self.f = bp.Float()

    def on_update(self):
        bp.text("Hello, world!")

        if bp.button("OK"):
            print(self.string.value)

        bp.input_text('string', self.string, 256)

        bp.slider_float("float", self.f, 0, 1)


app = App()
app.run()
