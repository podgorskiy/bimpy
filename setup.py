#
# Copyright 2017 Stanislav Pidhorskyi. All rights reserved.
# License: https://raw.githubusercontent.com/podgorskiy/impy/master/LICENSE.txt
#

from setuptools import setup, Extension, find_packages

from codecs import open
import os
import sys
import platform

sys._argv = sys.argv[:]
sys.argv=[sys.argv[0], '--root', 'gl3w/']

try:
    from gl3w import gl3w_gen
except:
    sys.path.insert(0, './gl3w')
    import gl3w_gen
	
sys.argv = sys._argv

target_os = 'none'

if sys.platform == 'darwin':
    target_os = 'darwin'
elif os.name == 'posix':
    target_os = 'posix'
elif platform.system() == 'Windows':
    target_os = 'win32'
    
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

glfw = [
     "glfw/src/context.c"
    ,"glfw/src/init.c"
    ,"glfw/src/input.c"
    ,"glfw/src/monitor.c"
    ,"glfw/src/vulkan.c"
    ,"glfw/src/window.c"
]

glfw_platform = {
    'darwin': [
         "glfw/src/cocoa_init.m"
        ,"glfw/src/cocoa_joystick.m"
        ,"glfw/src/cocoa_monitor.m"
        ,"glfw/src/cocoa_window.m"
        ,"glfw/src/cocoa_time.m"
        ,"glfw/src/posix_thread.c"
        ,"glfw/src/nsgl_context.c"
        ,"glfw/src/egl_context.c"
        ,"glfw/src/osmesa_context.c"
    ],
    'posix': [
         "glfw/src/x11_init.c"
        ,"glfw/src/x11_monitor.c"
        ,"glfw/src/x11_window.c"
        ,"glfw/src/xkb_unicode.c"
        ,"glfw/src/posix_time.c"
        ,"glfw/src/posix_thread.c"
        ,"glfw/src/glx_context.c"
        ,"glfw/src/egl_context.c"
        ,"glfw/src/osmesa_context.c"
        ,"glfw/src/null_joystick.c"
    ],
    'win32': [
         "glfw/src/win32_init.c"
        ,"glfw/src/win32_joystick.c"
        ,"glfw/src/win32_monitor.c"
        ,"glfw/src/win32_time.c"
        ,"glfw/src/win32_thread.c"
        ,"glfw/src/win32_window.c"
        ,"glfw/src/wgl_context.c"
        ,"glfw/src/egl_context.c"
        ,"glfw/src/osmesa_context.c"
    ]
}

imgui = [
     "imgui/imgui.cpp"
    ,"imgui/imgui_demo.cpp"
    ,"imgui/imgui_draw.cpp"
]

definitions = {
    'darwin': [("_GLFW_COCOA", 1)],
    'posix': [("GLFW_USE_OSMESA", 0), ("GLFW_USE_WAYLAND", 0), ("GLFW_USE_MIR", 0), ("_GLFW_X11", 1)],
    'win32': [("GLFW_USE_HYBRID_HPG", 0), ("_GLFW_WIN32", 1), ("_CRT_SECURE_NO_WARNINGS", 1), ("NOMINMAX", 1)],
}

libs = {
    'darwin': [],
    'posix': ["rt", "m", "X11"],
    'win32': ["gdi32", "opengl32", "Shell32"],
}

setup(
    name='impy',

    version='0.0.1',

    description='impy',
    long_description=long_description,

    url='https://github.com/podgorskiy/impy',

    author='Stanislav Pidhorskyi',
    author_email='stpidhorskyi@mix.wvu.edu',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
    ],

    keywords='imgui ui',

    packages = ['impy'],
    
    ext_modules = [Extension("_impy",
                             imgui + glfw + glfw_platform[target_os] + ['impy.cpp', "imgui_glfw.cpp", "gl3w/src/gl3w.c"],
                             define_macros = definitions[target_os],
                             include_dirs=["glfw/include", "imgui", "pybind11/include", "gl3w/include"],
                             libraries = libs[target_os],
                             extra_compile_args=['-std=c++11'],)]
)
