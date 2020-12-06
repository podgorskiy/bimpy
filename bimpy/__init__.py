# Copyright 2017-2020 Stanislav Pidhorskyi. All rights reserved.
# License: https://raw.githubusercontent.com/podgorskiy/bimpy/master/LICENSE.txt


import sys
import os


# For debugging using CMakelist build in an IDE
def _handle_debugging():
    # if running debug session
    if os.path.exists("cmake-build-debug/"):
        print('Running Debugging session!')
        sys.path.insert(0, "cmake-build-debug/")


_handle_debugging()


from _bimpy import *
from bimpy import themes
import bimpy.multilingual.unicode_ranges
import bimpy.utils
import bimpy.download
from bimpy.utils import begin_root
from bimpy.app import App
from bimpy.multilingual.load_fonts import load_fonts


class _IO_wrap():
    def __init__(self):
        pass

    def __getattr__(self, item):
        return getattr(getio(), item)

    def __setattr__(self, key, value):
        return setattr(getio(), key, value)


io = _IO_wrap()


_sphinx = 'sphinx' in sys.modules

# clean up namespace
del os
del sys
del app
del _IO_wrap
del _handle_debugging

# A hack to force sphinx to do the right thing
if _sphinx:
    __all__ = dir()
