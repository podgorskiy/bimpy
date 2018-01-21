bimpy - bundled imgui for python
================================

**bimpy** is a python module that provides bindings to `dear imgui <https://github.com/ocornut/imgui>`__ and distributed as a self-contained package bundled with `glfw <https://github.com/glfw/glfw>`__ and `gl3w <https://github.com/skaslev/gl3w>`__.

Features:
* Allows to create immediate mode UI with python easily. The API is kept as close to the original dear imgui as possible.

* **bimpy** already has all necessary functionality for window/OpenGL context creation and hides those details from the user.

* **bimpy** supports multiple contexts and allows creating multiple windows. 

* **bimpy** works on Windows, GNU Linux, and macOS.

* **bimpy** does not have dependencies and can be easely built from sources. Building relies only on distutils.

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

