import glob
from os.path import basename, dirname, isfile, join

__modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in __modules if isfile(f)
           and not f.endswith('__init__.py')]

# this is not formatted, it should come after __all__
# fmt: off
from . import *

# fmt: on
