bimpy - bundled imgui for python 
================================

.. |Downloads| image:: https://pepy.tech/badge/bimpy
   :target: https://pepy.tech/project/bimpy

.. |Build| image:: https://travis-ci.org/podgorskiy/bimpy.svg?branch=master
   :target: https://api.travis-ci.com/podgorskiy/bimpy.svg?branch=master

.. |License| image:: https://img.shields.io/badge/License-MIT-yellow.svg


:Downloads:     |Downloads|
:Build status:  |Build|
:License:       |License|


**bimpy** is a python module that provides bindings to `dear imgui <https://github.com/ocornut/imgui>`__ and distributed as a self-contained package bundled with `glfw <https://github.com/glfw/glfw>`__ and `gl3w <https://github.com/skaslev/gl3w>`__.

Features:

* Allows to create immediate mode UI with python easily. The API is kept as close to the original dear imgui as possible.

* **bimpy** already has all necessary functionality for window/OpenGL context creation and hides those details from the user.

* **bimpy** supports multiple contexts and allows creating multiple windows. 

* **bimpy** works on Windows, GNU Linux, and macOS.

* **bimpy** does not have dependencies and can be easely built from sources. Building relies only on distutils.

* **bimpy** can display images from ndarrays, PIL Images, numpy arrays, etc., 

Hello-world with bimpy:

.. code:: python

	import bimpy

	ctx = bimpy.Context()
		
	ctx.init(600, 600, "Hello")
	 
	str = bimpy.String()
	f = bimpy.Float();
		
	while(not ctx.should_close()):
		with ctx: 
			bimpy.text("Hello, world!")
			
			if bimpy.button("OK"):
				print(str.value)
			
			bimpy.input_text('string', str, 256)
			
			bimpy.slider_float("float", f, 0.0, 1.0)



.. figure:: https://i.imgur.com/rL7cFj7.png
   :alt: hello-world
   

Display image:
   
.. code:: python

    import bimpy
    from PIL import Image

    ctx = bimpy.Context()

    ctx.init(800, 800, "Image")

    image = Image.open("test.png")

    im = bimpy.Image(image)

    while(not ctx.should_close()):
        with ctx:
            bimpy.text("Display PIL Image")

            bimpy.image(im)


.. figure:: https://i.imgur.com/wiDGRpr.png
   :alt: hello-world

Similarly, numpy arrays with 2 dimensions, 3 dimensions (2, 3 or 4 channels) of type **np.uint8** can be displayed.
More examples here: https://github.com/podgorskiy/bimpy/blob/master/examples/image.py


Install
=======

Installation is easy since the package does not have dependencies:

.. code:: shell

	pip install bimpy

Or you can build and install from sources:

.. code:: shell

	python setup.py install

All c/c++ sources are built with distutils. All you need is a compiler with C++11 support.

Windows users, who use python 2.7 may encounter problems, because on Windows, python 2.7 uses MSVC 9.0, which doesn't have support for c++11. However, you still can build it with more recent MSVC (for example MSVC 14.0, which is Visual C++ 2015) using the commands below:

.. code:: shell

	call "%VS140COMNTOOLS%\VsDevCmd.bat"
	set VS90COMNTOOLS=%VS140COMNTOOLS%
	python setup.py install

If building on Linux, the following dependencies will be needed:

.. code:: shell

	sudo apt-get install mesa-common-dev libxi-dev libxinerama-dev libxrandr-dev libxcursor-dev


How to use it?
==============

Intro
-----

**bimpy** is python binding for `dear imgui <https://github.com/ocornut/imgui>`__ and tries to match the C++ API. Also, it has some additional functions to create a window and some other differences.

It has binding for the most functions from **dear imgui**. All functions are renamed from **CamelCase** to **snake_case**, which is more common for python. For example ``ImGui::InputText`` is mapped to ``bimpy.input_text``.

Context and window
------------------

First of all, you need to import **bimpy**

.. code:: python

	import bimpy

Distinctively from **dear imgui**, bimpy does not have global state (**dear imgui** has it by default, but it has an option not to have one). So, you will need to create a context.

.. code:: python

	ctx = bimpy.Context(width, height, name)

Where integers *width* and *height* specify the size of the window, and string *name* is a caption of the window.

All calls to **bimpy**'s API must be within *with* statement applied to the context object:

.. code:: python

	with ctx: 
		bimpy.text("Hello, world!")


And there must be only one *with* statement applied to the context object per frame.

Or, a second option is to manualy call ``ctx.new_frame()`` before all API calls, and then ``ctx.render()`` after.

.. code:: python
	
	ctx.new_frame()
	bimpy.text("Hello, world!")
	ctx.render()


You can have multiple *Context* objects for multiple windows, however, API is not thread-safe.

Variables
------------------

All **imgui** API that provides user input (such as *InputText*, *SliderFloat*, etc.) modifies the variable through the reference to it. However, in python, such objects as integers, floats and strings are passed always by value. Because of this, **bimpy** provides special wrappers, that allow passing those variables by reference.

For example, to use *slider_float*, you will need first to create a variable that will hold the state:

.. code:: python

	f = bimpy.Float();

You can access the value in the following way: ``f.value``

To use it with *slider_float* simply pass it to that function:

.. code:: python

	bimpy.slider_float("float slider", f, 0.0, 1.0)


All **imgui** input functions that provide multiple inputs, like *SliderFloat2*, *SliderInt4*, *InputInt3*, etc. are mapped to equivalent functions, but instead of passing an array of variables, you need to list all variables in the argument list:

.. code:: python
	
	f1 = bimpy.Float();
	f2 = bimpy.Float();
	f3 = bimpy.Float();

	while(not ctx.should_close()):
		with ctx: 
			bimpy.slider_float3("float", f1, f2, f3, 0.0, 1.0)

Draw commands
------------------
Some draw commands are exposed. In contrast to C++ API, the exposed functions are not methods of **ImDrawList**, but global functions. All drawing functions should be called inside the *begin/end* calls of a window. 

List of exposed drawing functions:

.. code:: python

    add_circle(centre: _bimpy.Vec2, radius: float, col: int, num_segments: int=12, thickness: float=1.0) -> None
    add_circle_filled(centre: _bimpy.Vec2, radius: float, col: int, num_segments: int=12) -> None
    add_line(a: _bimpy.Vec2, b: _bimpy.Vec2, col: int, thickness: float=1.0) -> None
    add_quad(a: _bimpy.Vec2, b: _bimpy.Vec2, c: _bimpy.Vec2, d: _bimpy.Vec2, col: int, thickness: float=1.0) -> None
    add_quad_filled(a: _bimpy.Vec2, b: _bimpy.Vec2, c: _bimpy.Vec2, d: _bimpy.Vec2, col: int) -> None
    add_rect(a: _bimpy.Vec2, b: _bimpy.Vec2, col: int, rounding: float=0.0, rounding_corners_flags: int=Corner.All, thickness: float=1.0) -> None
    add_rect_filled(a: _bimpy.Vec2, b: _bimpy.Vec2, col: int, rounding: float=0.0, rounding_corners_flags: int=Corner.All) -> None
    add_rect_filled_multicolor(a: _bimpy.Vec2, b: _bimpy.Vec2, col_upr_left: int, col_upr_right: int, col_bot_right: int, col_bot_lefs: int) -> None
    add_triangle(a: _bimpy.Vec2, b: _bimpy.Vec2, c: _bimpy.Vec2, col: int, thickness: float=1.0) -> None
    add_triangle_filled(a: _bimpy.Vec2, b: _bimpy.Vec2, c: _bimpy.Vec2, col: int) -> None

Simple usage example below:

.. figure:: https://i.imgur.com/MU5Vhfl.png
   :alt: hello-world

.. code:: python

	import bimpy
	import numpy as np

	ctx = bimpy.Context()

	ctx.init(1200, 1200, "Draw Commands Test")

	with ctx:
		bimpy.themes.set_light_theme()

	DATA_POINTS = bimpy.Int(30)
	CLASTERS = bimpy.Int(4)

	std = bimpy.Float(0.5)

	colors = [0x4b19e6, 0x4bb43c, 0x19e1ff, 0xc88200, 0x3182f5, 0xb41e91, 0xf0f046, 0xf032e6, 0xd2f53c,
			  0xfabebe, 0x008080, 0xe6beff, 0xaa6e28, 0xfffac8, 0x800000, 0xaaffc3, 0x808000, 0xffd8b1,
			  0x000080, 0x808080, 0xFFFFFF, 0x000000]

	datapoints = []


	def generate_fake_data():
		datapoints.clear()
		for i in range(CLASTERS.value):
			x = np.random.normal(size=(DATA_POINTS.value, 2))
			alpha = np.random.rand()
			scale = std.value * np.random.rand(2) * np.eye(2, 2)
			position = np.random.rand(2) * 5
			rotation = np.array([[np.cos(alpha), np.sin(alpha)], [-np.sin(alpha), np.cos(alpha)]])
			x = np.matmul(x, scale)
			x = np.matmul(x, rotation)
			x += position
			datapoints.append((x, rotation, position, scale))

	axis = x = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])

	while not ctx.should_close():
		ctx.new_frame()

		bimpy.set_next_window_pos(bimpy.Vec2(20, 20), bimpy.Condition.Once)
		bimpy.set_next_window_size(bimpy.Vec2(800, 600), bimpy.Condition.Once)
		bimpy.begin("Drawings")

		window_pos = bimpy.get_window_pos()

		center = bimpy.Vec2(100, 100) + window_pos
		m = 100.0
		for i in range(len(datapoints)):
			(x, R, P, S) = datapoints[i]

			for j in range(x.shape[0]):
				point = bimpy.Vec2(x[j, 0], x[j, 1])
				bimpy.add_circle_filled(point * m + center, 5, 0xAF000000 + colors[i], 100)

			axis_ = np.matmul(axis, S * 2.0)
			axis_ = np.matmul(axis_, R) + P

			bimpy.add_line(
				center + bimpy.Vec2(axis_[0, 0], axis_[0, 1]) * m,
				center + bimpy.Vec2(axis_[1, 0], axis_[1, 1]) * m,
				0xFFFF0000, 1)

			bimpy.add_line(
				center + bimpy.Vec2(axis_[2, 0], axis_[2, 1]) * m,
				center + bimpy.Vec2(axis_[3, 0], axis_[3, 1]) * m,
				0xFFFF0000, 1)

		bimpy.end()

		bimpy.set_next_window_pos(bimpy.Vec2(20, 640), bimpy.Condition.Once)
		bimpy.set_next_window_size(bimpy.Vec2(800, 140), bimpy.Condition.Once)
		bimpy.begin("Controls")

		bimpy.input_int("Data points count", DATA_POINTS)
		bimpy.input_int("Clasters count", CLASTERS)

		bimpy.slider_float("std", std, 0.0, 3.0)

		if bimpy.button("Generate data"):
			generate_fake_data()

		bimpy.end()

		ctx.render()


Acknowledgements
================

* robobuggy https://github.com/gfannes
* njazz https://github.com/njazz
* Florian Rott https://github.com/sauberfred
