#
# Copyright 2017-2020 Stanislav Pidhorskyi. All rights reserved.
# License: https://raw.githubusercontent.com/podgorskiy/impy/master/LICENSE.txt
#

from setuptools import setup, Extension, find_packages
from distutils.errors import *
from distutils.dep_util import newer_group
from distutils import log
from distutils.command.build_ext import build_ext

from codecs import open
import os
import sys
import platform
import re
import glob
from distutils.ccompiler import CCompiler
from multiprocessing.pool import ThreadPool as Pool


def compile(self, sources, output_dir=None, macros=None, include_dirs=None, debug=0, extra_preargs=None, extra_postargs=None, depends=None):
    macros, objects, extra_postargs, pp_opts, build = self._setup_compile(output_dir, macros, include_dirs, sources, depends, extra_postargs)
    cc_args = self._get_cc_args(pp_opts, debug, extra_preargs)

    def f(x):
        try:
            src, ext = build[x]
        except KeyError:
            return

        self._compile(x, src, ext, cc_args, extra_postargs, pp_opts)

    pool = Pool(processes=6)
    pool.map(f, objects)

    return objects


# Overwrite to enable multiprocess compilation
CCompiler.compile = compile

sys._argv = sys.argv[:]
sys.argv = [sys.argv[0], '--root', 'libs/gl3w/']

try:
    from libs.gl3w import gl3w_gen
except:
    sys.path.insert(0, './libs/gl3w')
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


def filter_sources(sources):
    """Filters sources into c, cpp and objc"""
    cpp_ext_match = re.compile(r'.*[.](cpp|cxx|cc)\Z', re.I).match
    c_ext_match = re.compile(r'.*[.](c|C)\Z', re.I).match
    objc_ext_match = re.compile(r'.*[.]m\Z', re.I).match

    c_sources = []
    cpp_sources = []
    objc_sources = []
    other_sources = []
    for source in sources:
        if c_ext_match(source):
            c_sources.append(source)
        elif cpp_ext_match(source):
            cpp_sources.append(source)
        elif objc_ext_match(source):
            objc_sources.append(source)
        else:
            other_sources.append(source)
    return c_sources, cpp_sources, objc_sources, other_sources


def build_extension(self, ext):
    """Modified version of build_extension method from distutils.
       Can handle compiler args for different files"""

    sources = ext.sources
    if sources is None or not isinstance(sources, (list, tuple)):
        raise DistutilsSetupError(
                "in 'ext_modules' option (extension '%s'), "
                "'sources' must be present and must be "
                "a list of source filenames" % ext.name)

    sources = list(sources)
    ext_path = self.get_ext_fullpath(ext.name)
    depends = sources + ext.depends
    if not (self.force or newer_group(depends, ext_path, 'newer')):
        log.debug("skipping '%s' extension (up-to-date)", ext.name)
        return
    else:
        log.info("building '%s' extension", ext.name)

    sources = self.swig_sources(sources, ext)

    extra_args = ext.extra_compile_args or []
    extra_c_args = getattr(ext, "extra_compile_c_args", [])
    extra_cpp_args = getattr(ext, "extra_compile_cpp_args", [])
    extra_objc_args = getattr(ext, "extra_compile_objc_args", [])
    macros = ext.define_macros[:]
    for undef in ext.undef_macros:
        macros.append((undef,))

    c_sources, cpp_sources, objc_sources, other_sources = filter_sources(sources)

    def _compile(src, args):
        return self.compiler.compile(src,
                                     output_dir=self.build_temp,
                                     macros=macros,
                                     include_dirs=ext.include_dirs,
                                     debug=self.debug,
                                     extra_postargs=extra_args + args,
                                     depends=ext.depends)

    objects = []
    objects += _compile(c_sources, extra_c_args)
    objects += _compile(cpp_sources, extra_cpp_args)
    objects += _compile(objc_sources, extra_objc_args)
    objects += _compile(other_sources, [])

    self._built_objects = objects[:]
    if ext.extra_objects:
        objects.extend(ext.extra_objects)

    extra_args = ext.extra_link_args or []

    language = ext.language or self.compiler.detect_language(sources)
    self.compiler.link_shared_object(
            objects, ext_path,
            libraries=self.get_libraries(ext),
            library_dirs=ext.library_dirs,
            runtime_library_dirs=ext.runtime_library_dirs,
            extra_postargs=extra_args,
            export_symbols=self.get_export_symbols(ext),
            debug=self.debug,
            build_temp=self.build_temp,
            target_lang=language)


# patching
build_ext.build_extension = build_extension

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
        ,"glfw/src/cocoa_time.c"
        ,"glfw/src/posix_thread.c"
        ,"glfw/src/nsgl_context.m"
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
        ,"glfw/src/linux_joystick.c"
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
    ,"imgui/imgui_widgets.cpp"
]

definitions = {
    'darwin': [("_GLFW_COCOA", 1)],
    'posix' : [("GLFW_USE_OSMESA", 0), ("GLFW_USE_WAYLAND", 0), ("GLFW_USE_MIR", 0), ("_GLFW_X11", 1)],
    'win32' : [("GLFW_USE_HYBRID_HPG", 0), ("_GLFW_WIN32", 1), ("_CRT_SECURE_NO_WARNINGS", 1), ("NOMINMAX", 1)],
}

libs = {
    'darwin': [],
    'posix' : ["rt", "m", "X11"],
    'win32' : ["gdi32", "opengl32", "Shell32"],
}

extra_link = {
    'darwin': ["-framework", "Cocoa", "-framework", "IOKit", "-framework", "Cocoa", "-framework", "CoreFoundation",
               "-framework", "CoreVideo"],
    'posix' : [],
    'win32' : [],
}

extra_compile_args = {
    'darwin': [],
    'posix' : [],
    'win32' : ['/MT', '/fp:fast', '/GL', '/GR-'],
}

extra_compile_cpp_args = {
    'darwin': ['-std=c++11'],
    'posix' : ['-std=c++11'],
    'win32' : [],
}

bimpy_sources = list(glob.glob('sources/*.cpp'))


def add_prefix(l, prefix):
    return [os.path.join(prefix, x) for x in l]


extension = Extension("_bimpy",
                      add_prefix(imgui + glfw + glfw_platform[target_os], "libs") + bimpy_sources + ["libs/gl3w/src/gl3w.c"],
                      define_macros=definitions[target_os] + [('IMGUI_USER_CONFIG', '"bimpy_imgui_config.h"')],
                      include_dirs=add_prefix([
                          "glfw/include",
                          "imgui",
                          "pybind11/include",
                          "backward-cpp",
                          "gl3w/include"], "libs") + ["sources/config", "sources"],
                      extra_compile_args=extra_compile_args[target_os],
                      extra_link_args=extra_link[target_os],
                      libraries=libs[target_os])

extension.extra_compile_cpp_args = extra_compile_cpp_args[target_os]

setup(
    name='bimpy',

    version='0.1.1',

    description='bimpy - bundled imgui for python',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/podgorskiy/bimpy',

    author='Stanislav Pidhorskyi',
    author_email='stanislav@podgorskiy.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='imgui ui',

    packages=['bimpy', 'bimpy.multilingual'],

    ext_modules=[extension],
)
