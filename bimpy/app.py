# Copyright 2019-2020 Stanislav Pidhorskyi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import bimpy


class App:
    r"""A base class for the application.

    .. note::
        You need to implement your own application class that derives from this class.

    .. warning::
        You will need to call `set_image` before you can run it

    Arguments:
        width (int): width of the window. Default: 600.
        height (int): height of the window. Default: 600.
        title (str): title of the window. Default: "Hello".


    Example:
        >>> import bimpy
        >>>
        >>> class App(anntoolkit.App):
        >>>     def __init__(self):
        >>>         # Calling constructor of base class
        >>>         super(App, self).__init__(title='Test')
        >>>
        >>>         # set image to view
        >>>         im = imageio.imread('test_image.jpg')
        >>>         self.set_image(im)
        >>>
        >>> # Run app
        >>> app = App()
        >>> app.run()
    """

    def __init__(self, width=600, height=600, title="Hello", **kwargs):
        self._ctx = bimpy.Context()
        self._ctx.init(width, height, title, **kwargs)

        def mouse_button(down, x, y, lx, ly):
            self.on_mouse_button(down, x, y, lx, ly)

        self._ctx.set_mouse_button_callback(mouse_button)

        def mouse_pos(x, y, lx, ly):
            self.on_mouse_position(x, y, lx, ly)

        self._ctx.set_mouse_position_callback(mouse_pos)

        def keyboard(key, action, mods):
            if key < 255:
                key = chr(key)
            if action == 1:
                self.keys[key] = 1
            elif action == 0:
                if key in self.keys:
                    del self.keys[key]
            self.on_keyboard(key, action == 1, mods)

        self._ctx.set_keyboard_callback(keyboard)
        self.keys = {}
        self.image = None

    def run(self):
        """Runs the application.

        .. note::
            This is a blocking call. It won't return until the window is closed

        Runs an event loop, where it process user input and updates window.
        Call callback method  :meth:`on_update`.

        Example:
            >>> app = App()
            >>> app.run()
        """
        while not self._ctx.should_close():
            with self._ctx:
                for k, v in self.keys.items():
                    self.keys[k] += 1
                    if v > 50:
                        self.on_keyboard(k, True, 0)
                        self.keys[k] = 45

                self.on_update()

    def on_update(self):
        """Is called each frame from the event loop that is run in :meth:`run` method

        Empty method, you need to overwrite it.
        Do all drawing from here.

        .. note::
            * Calls to draw API are valid only from within this method. Draw API: :meth:`point`,  :meth:`box`,  :meth:`text`, etc.

        .. warning::
            * Don't call it, this is callback

        """
        pass

    def on_mouse_button(self, down, x, y, lx, ly):
        """Is called on left mouse button event from event loop that is run in :meth:`run` method
        If the user presses left button on the mouse, this method is called

        Empty method, you need to overwrite it

        .. warning::
            * Don't call it, this is callback

        Arguments:
            down (bool): True if left mouse button is pressed. False if left mouse button is released.
            x (float): x coordinate of mouse cursor in window coordinate system
            y (float): y coordinate of mouse cursor in window coordinate system
            lx (float): x coordinate of mouse cursor in image coordinate system
            ly (float): y coordinate of mouse cursor in image coordinate system

        """
        pass

    def on_mouse_position(self, x, y, lx, ly):
        """Is called on mouse move event from event loop that is run in :meth:`run` method
        If the user moves mouse, this method is called

        Empty method, you need to overwrite it

        .. warning::
            * Don't call it, this is callback

        Arguments:
            x (float): x coordinate of mouse cursor in window coordinate system
            y (float): y coordinate of mouse cursor in window coordinate system
            lx (float): x coordinate of mouse cursor in image coordinate system
            ly (float): y coordinate of mouse cursor in image coordinate system

        """
        pass

    def on_keyboard(self, key, down, mods):
        """Is called on keybord key event from event loop that is run in :meth:`run` method

        Empty method, you need to overwrite it

        .. warning::
            * Don't call it, this is callback

        Arguments:
            key (int): The key that generated even. Can be `anntoolkit.KeyEscape`, `anntoolkit.KeyTab`,
                `anntoolkit.KeyBackspace`, `anntoolkit.KeyInsert`, `anntoolkit.KeyDelete`, `anntoolkit.KeyRight`, `anntoolkit.KeyLeft`, `anntoolkit.KeyDown`, `anntoolkit.KeyUp` or any char from 'A' to 'Z'
            down (bool): True if key is pressed. False if key is released.
            mods (int): Indicates additional modifing keys, such as Ctrl, Shift, Alt

        Example:
            >>> def on_keyboard(self, key, down, mods):
            >>>     if down:
            >>>         if key == anntoolkit.KeyLeft:
            >>>             ...
            >>>         if key == anntoolkit.KeyRight:
            >>>             ...
            >>>         if key == anntoolkit.KeyUp:
            >>>             ...
            >>>         if key == anntoolkit.KeyDown:
            >>>             ...
            >>>         if key == anntoolkit.KeyDelete:
            >>>             ...
            >>>         if key == anntoolkit.KeyBackspace:
            >>>             ...
            >>>         if key == 'R':
            >>>             ...
            >>>         if key == 'A':
            >>>             ...
            >>>         if key == 'Q':
            >>>             ...
        """
        pass

    @property
    def width(self):
        """Width of the window
        """
        return self._ctx.width()

    @property
    def height(self):
        """Height of the window

        """
        return self._ctx.height()
