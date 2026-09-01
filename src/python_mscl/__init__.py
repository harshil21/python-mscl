from warnings import warn

# from . import mscl

warn(
    "The 'python_mscl' package is archived, please use the official `pymscl` package instead.",
    DeprecationWarning,
    stacklevel=2
)

# Intentionally make the user can do `from python_mscl import mscl` instead of `import mscl` which
# can be done by doing a from .mscl import * here.
# __all__ = ["mscl"]
