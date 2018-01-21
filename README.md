impy
=============

**impy** is python bindings to [dear imgui](https://github.com/ocornut/imgui) distributed as a self-contained package bundled with [glfw](https://github.com/glfw/glfw) and [gl3w](https://github.com/skaslev/gl3w).

Features:
* Allows to create immediate mode UI with python easily. The API is kept as close to the original dear imgui as possible.

* **impy** already has all necessary functionality for window/OpenGL context creation and hides those details from the user.

* **impy** supports multiple contexts and allows creating multiple windows. 

* **impy** works on Windows, GNU Linux, and macOS

Hello-world with impy:

```python
import impy

ctx = impy.Context()
    
ctx.init(600, 600, "Hello")
 
str = impy.String()
f = impy.Float();
	
while(not ctx.should_close()):
	with ctx: 
		impy.text("Hello, world!")
		
		if impy.button("OK"):
		    print(str.value)
        
		impy.input_text('string', str, 256)
		
		impy.slider_float("float", f, 0.0, 1.0)
```

![hellowworld](https://i.imgur.com/rL7cFj7.png)


Install
=======

Installation is easy since the package does not have dependencies:

``pip install impy``

Or you can build and install from sources:

``python setup.py install``

All c/c++ sources are built with distutils. All you need is a compiler with C++11 support.

Windows users, who use python 2.7 may encounter problems, because on Windows, python 2.7 uses MSVC 9.0, which doesn't have support for c++11. However, you still can build it with more recent MSVC (for example MSVC 14.0, which is Visual C++ 2015) using the commands below:

```
call "%VS140COMNTOOLS%\VsDevCmd.bat"
set VS90COMNTOOLS=%VS140COMNTOOLS%
python setup.py install
```

How to use it?
==============

Intro
-----

**impy** is python binding for [dear imgui](https://github.com/ocornut/imgui) and tries to match the C++ API. Also, it has some additional functions to create a window and some other differences.

It has binding for the most functions from **dear imgui**. All functions are renamed from **CamelCase** to **snake_case**, which is more common for python. For example ``ImGui::InputText`` is mapped to ``impy.input_text``.

Context and window
------------------

First of all, you need to import **impy**

``import impy``

Distinctively from **dear imgui**, impy does not have global state (**dear imgui** has it by default, but it has an option not to have one). So, you will need to create a context.

``ctx = impy.Context(width, height, name)``

Where integers *width* and *height* specify the size of the window, and string *name* is a caption of the window.

All calls to **impy**'s API must be within *with* statement applied to the context object:

```python
with ctx: 
		impy.text("Hello, world!")
```

And there must be only one *with* statement applied to the context object per frame.

Or, a second option is to manualy call ``ctx.new_frame()`` before all API calls, and then ``ctx.render()`` after.

```python
ctx.new_frame()
impy.text("Hello, world!")
ctx.render()
```

You can have multiple *Context* objects for multiple windows, however, API is not thread-safe.

Variables
------------------

All **imgui** API that provides user input (such as *InputText*, *SliderFloat*, etc.) modifies the variable through the reference to it. However, in python, such objects as integers, floats and strings are passed always by value. Because of this, **impy** provides special wrappers, that allow passing those variables by reference.

For example, to use *slider_float*, you will need first to create a variable that will hold the state:

```python
f = impy.Float();
```

You can access the value in the following way: ``f.value``

To use it with *slider_float* simply pass it to that function:

```python
impy.slider_float("float slider", f, 0.0, 1.0)
```

All **imgui** input functions that provide multiple inputs, like *SliderFloat2*, *SliderInt4*, *InputInt3*, etc. are mapped to equivalent functions, but instead of passing an array of variables, you need to list all variables in the argument list:

```python
f1 = impy.Float();
f2 = impy.Float();
f3 = impy.Float();

while(not ctx.should_close()):
	with ctx: 
		impy.slider_float3("float", f1, f2, f3, 0.0, 1.0)
```
