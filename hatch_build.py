"""Specifies a hatch build hook to create the wheel for mscl."""

import platform
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

from build_helpers.release_downloader import GithubDownloader


class CustomBuildHook(BuildHookInterface):
    """Build hook to build wheels from the extracted .deb/.zip files."""

    def _python_tag(self) -> str:
        """Generate the Python tag (e.g., py39 for Python 3.9)."""
        major = sys.version_info.major
        minor = sys.version_info.minor
        return f"cp{major}{minor}"

    def _platform_tag(self) -> str:
        """Generate the platform tag (e.g., linux_x86_64)."""
        return platform.system().lower() + "_" + platform.machine()

    def initialize(self, version, build_data):
        """
        Called before building the wheel/sdist.
        We can download & extract the .deb here, and place
        mscl.py and _mscl.so into src/mscl_pip/.
        """
        build_data["pure_python"] = False
        self.app.display_info(f"Running on {version=} and {build_data=}")
        self.app.display_info(self.target_name)

        # --- STEP 1: Determine which python version and arch we are on: ---
        # a) Python version:
        # syntax: Python<MAJOR>.<MINOR>

        py_version = f"Python{sys.version_info.major}.{sys.version_info.minor}"

        # b) Architecture:
        # possible values: amd64, arm64, armhf.

        arch = platform.machine()
        if arch == "x86_64":
            arch = "amd64"
        elif arch == "aarch64":
            arch = "arm64"
        elif arch == "armv7l":
            arch = "armhf"
        else:
            # TODO: Windows support
            raise RuntimeError(f"Unknown architecture: {arch}")

        # c) mscl version to download:
        mscl_ver = "v67.0.0"

        build_data["tag"] = f"{self._python_tag()}-{self._python_tag()}-{self._platform_tag()}"
        # --- STEP 2: Download the 2 mscl files (mscl.py and _mscl.so) from the git repo: ---
        # Folder name: mscl-<arch>-<python-ver>-<mscl-ver>

        # a) Create the folder name:
        folder_name = f"mscl-{arch}-{py_version}-{mscl_ver}"

        # b) Use PyGithub to download the files from the folder:
        self.app.display_waiting(f"Downloading files for {folder_name}...")

        gh = GithubDownloader()
        gh.download_assets_from_folder(
            tag=mscl_ver,
            folder_name=f"mscl_release_assets/{folder_name}",
        )

        self.app.display_success("Downloaded files successfully.")
        build_data["artifacts"] = ["_mscl.so", "mscl.py"]

        # Show all files in the current directory:
        # self.app.display_info(f"Files in {Path().cwd()}: {list(Path().cwd().iterdir())}")

        # --- STEP 3: Copy the files ("_mscl.so" & "mscl.py") to the src/mscl/ directory: ---
        # Move from root (i.e. cwd) to src/mscl
        subprocess.run(["mv", "mscl.py", "src/mscl/"], check=True)  # noqa: S603, S607
        subprocess.run(["mv", "_mscl.so", "src/mscl/"], check=True)  # noqa: S603, S607
        self.app.display_success("Moved files to src/mscl/ successfully. Building wheel...")
