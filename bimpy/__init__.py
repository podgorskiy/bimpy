import sys
import os


def _handle_debugging():
    # if running debug session
    if os.path.exists("cmake-build-debug/"):
        print('Running Debugging session!')
        sys.path.insert(0, "cmake-build-debug/")


_handle_debugging()


from _bimpy import *
from bimpy import themes

# A hack to force sphinx to do the right thing
if 'sphinx' in sys.modules:
    del os
    del sys
    __all__ = dir()
else:
    del os
    del sys
