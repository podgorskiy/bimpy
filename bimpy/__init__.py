import sys
import os

from bimpy.multilingual import unicode_ranges


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


class IO_wrap():
    def __init__(self):
        pass

    def __getattr__(self, item):
        return getattr(getio(), item)

    def __setattr__(self, key, value):
        return setattr(getio(), key, value)


io = IO_wrap()


def begin_root(name):
    set_next_window_pos(Vec2(0, 0))
    set_next_window_size(io.display_size)
    push_style_var(Style.WindowRounding, 0)
    begin("name", flags=WindowFlags.NoDecoration | WindowFlags.NoMove | WindowFlags.NoMove)
    pop_style_var()


# A hack to force sphinx to do the right thing
if 'sphinx' in sys.modules:
    del os
    del sys
    __all__ = dir()
else:
    del os
    del sys
