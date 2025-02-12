"""File to store common constants used in the project."""

from pathlib import Path
from typing import NamedTuple


# Named tuple to store the release asset information:
class ReleaseAsset(NamedTuple):
    """Named tuple to store the release asset information.

    Args:
        python_version: The Python version of the release asset. E.g. "Python3.9".
        arch: The architecture of the release asset. E.g. "amd64".
    """

    python_version: str
    arch: str


ASSET_DIRECTORY = Path("mscl_release_assets")
"""The directory to store the downloaded release assets."""


# Keep this the same as the one in `hatch_build.py`!
MSCL_VERSION = "v67.0.1"
"""The mscl version to extract from the `ASSET_DIRECTORY`. The
downloader will download the latest version despite this version number."""


MACHINE_MAPPING_TO_ARCH = {
    # Linux:
    "x86_64": "amd64",
    "aarch64": "arm64",
    "armv7l": "armhf",
    # Windows:
    "AMD64": "Windows_x64",
    "x86": "Windows_x86",
}
