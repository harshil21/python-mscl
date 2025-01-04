from . import mscl

# Intentionally make the user can do `from python_mscl import mscl` instead of `import mscl` which
# can be done by doing a from .mscl import * here.
__all__ = ["mscl"]
