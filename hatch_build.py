"""Specifies a hatch build hook to create the wheel for mscl."""

import os
import shutil
from pathlib import Path
from typing import ClassVar

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

# This is specified here instead of in the constants since we get import errors:
MSCL_VERSION = "v67.0.1"
"""The mscl version to build the wheels from."""

BUILD_ARCH = os.getenv("BUILD_ARCH", "false")
"""The build architecture to use for the wheels. This determines the tag for the wheel.

This will be the arch in folder name (e.g., amd64, arm64, armhf, Windows-x64, Windows-x86).
"""

PYTHON_BUILD_VERSION = os.getenv("PYTHON_BUILD_VERSION", "false")
"""The Python build version to use for the wheels. This determines the tag for the wheel.

This will be the python version in folder name (e.g., Python3.9, Python3.11, etc).
"""


class CustomBuildHook(BuildHookInterface):
    """Build hook to build wheels from the extracted .deb/.zip files."""

    PYTHON_VER_MAPPING: ClassVar[dict[str, str]] = {
        "Python3.9": "cp39",
        "Python3.10": "cp310",
        "Python3.11": "cp311",
        "Python3.12": "cp312",
        "Python3.13": "cp313",
    }
    """The mapping of Python versions of the folder to the Python tags for the wheel."""

    PYTHON_BUILD_MAPPING: ClassVar[dict[str, str]] = {
        "amd64": "manylinux2014_x86_64",
        "arm64": "manylinux2014_aarch64",
        "armhf": "manylinux2014_armv7l",
        "Windows-x64": "win_amd64",
        "Windows-x86": "win32",
    }
    """The mapping of architectures (in the folder name) to the platform tags for the wheel."""

    def _python_tag(self) -> str | None:
        """Generate the Python tag (e.g., py39 for Python 3.9)."""
        try:
            return self.PYTHON_VER_MAPPING.get(PYTHON_BUILD_VERSION)
        except KeyError as e:
            raise RuntimeError(f"Unknown Python version: {PYTHON_BUILD_VERSION}") from e

    def _platform_tag(self) -> str | None:
        """Generate the platform tag (e.g., linux_x86_64)."""
        try:
            return self.PYTHON_BUILD_MAPPING.get(BUILD_ARCH)
        except KeyError as e:
            raise RuntimeError(f"Unknown platform: {BUILD_ARCH}") from e

    def _make_tag(self) -> str:
        """Generate the tag for the wheel (e.g., py39-linux_x86_64)."""
        return f"{self._python_tag()}-{self._python_tag()}-{self._platform_tag()}"

    def initialize(self, version, build_data):
        """
        Called before building the wheel/sdist.
        We can download & extract the .deb here, and place
        mscl.py and _mscl.so into src/mscl_pip/.
        """
        # Don't run build hook when a user is installing the wheel:
        if PYTHON_BUILD_VERSION == "false" and BUILD_ARCH == "false":
            return

        build_data["pure_python"] = False
        self.app.display_info(
            f"Running on {version=} on {build_data=}, with "
            f"{PYTHON_BUILD_VERSION=} and {BUILD_ARCH=}"
        )

        # --- STEP 1: Determine which python version and arch we are on: ---
        # Build the folder name based on the python version and arch in the environment variables.

        folder_name = f"mscl-{BUILD_ARCH}-{PYTHON_BUILD_VERSION}-{MSCL_VERSION}"

        build_data["tag"] = self._make_tag()

        # --- STEP 3: Copy the files ("_mscl.so" & "mscl.py") to the src/mscl/ directory: ---
        # Move from root (i.e. cwd) to src/mscl

        self.remove_existing_files(Path("src/python_mscl/"), ["_mscl.so", "_mscl.pyd", "mscl.py"])

        # Copy files from mscl_release_assets/folder_name to src/mscl/:
        p = Path("mscl_release_assets") / folder_name

        shutil.copy(p / "mscl.py", "src/python_mscl/")
        if BUILD_ARCH.startswith("Windows"):  # Windows uses _mscl.pyd
            shutil.copy(p / "_mscl.pyd", "src/python_mscl/")
            build_data["artifacts"] = ["_mscl.pyd", "mscl.py"]
        else:
            shutil.copy(p / "_mscl.so", "src/python_mscl/")
            build_data["artifacts"] = ["_mscl.so", "mscl.py"]

        self.app.display_success("Moved files to src/python_mscl/ successfully. Building wheel...")

    def remove_existing_files(self, directory: Path, files: list[str]) -> None:
        """Remove the existing files from the directory."""
        for file in files:
            file_path = directory / file
            if file_path.exists():
                file_path.unlink()
