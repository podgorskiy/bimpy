import io
import requests
import bimpy
from PIL import Image

img_urls = [
    "https://farm2.static.flickr.com/1080/1029412358_7ee17550fc.jpg",
    "https://farm5.static.flickr.com/4029/4332778219_472a339b0a.jpg",
    "https://bellard.org/bpg/3.png"
]

def download_image(url):
    r = requests.get(url, timeout=4.0)
    if r.status_code != requests.codes.ok:
        assert False, 'Status code error: {}.'.format(r.status_code)
    data = io.BytesIO(r.content)
    return Image.open(data)


ctx = bimpy.Context()

ctx.init(800, 800, "Image")

im = None

while(not ctx.should_close()):
    with ctx:
        bimpy.text("Example showing how to display images from PIL Image and numpy array")

        if bimpy.button("RGB image. Cat"):
            im = bimpy.Image(download_image(img_urls[0]))
        if bimpy.button("RGB image. Turtle"):
            im = bimpy.Image(download_image(img_urls[1]))
        if bimpy.button("RGB with alpha"):
            im = bimpy.Image(download_image(img_urls[2]))

        if bimpy.button("Generate mandelbrot set"):
            import numpy as np

            m = 480
            n = 320

            x = np.linspace(-2, 1, num=m).reshape((1, m))
            y = np.linspace(-1, 1, num=n).reshape((n, 1))
            C = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))

            Z = np.zeros((n, m), dtype=complex)
            M = np.full((n, m), True, dtype=bool)
            for i in range(100):
                Z[M] = Z[M] * Z[M] + C[M]
                M[np.abs(Z) > 2] = False

            im = bimpy.Image(np.uint8(np.flipud(1 - M) * 255))

        if bimpy.button("Checkerboard"):
            import numpy as np

            im = bimpy.Image(np.uint8(np.kron([[1, 0] * 16, [0, 1] * 16] * 16, np.ones((20, 20))) * 255))
            im.grayscale_to_alpha()

        y = bimpy.get_cursor_pos_y()
        bimpy.set_cursor_pos_y(250)

        window_pos = bimpy.get_window_pos()
        center = bimpy.Vec2(150, 350) + window_pos

        bimpy.text("Some text behind image. See 'Checkerboard' and 'RGB with alpha' options.")
        bimpy.add_circle_filled(center, 50, 0xaf4bb43c, 255)
        bimpy.set_cursor_pos_y(y)


        if im is not None:
            bimpy.image(im)
