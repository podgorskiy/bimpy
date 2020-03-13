from _bimpy import *
from bimpy import themes

# A hack to force sphinx to do the right thing
import sys
if 'sphinx' in sys.modules:
    del sys
    __all__ = dir()
else:
    del sys
