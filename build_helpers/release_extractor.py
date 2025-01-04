"""Extracts the .deb and .zip releases for the mscl library."""

import os
import subprocess
from pathlib import Path

MSCL_VERSION = "v67.0.0"
"""The mscl version to extract."""

class ReleaseExtractor:
    """Will extract the .deb and .zip releases for the mscl library."""

    def __init__(self):
        self.asset_dir = Path("mscl_release_assets")

    def extract_assets(self):
        """Extracts the .deb and .zip releases into the same directory."""

        for file in self.asset_dir.iterdir():
            if file.suffix == ".deb":
                self.extract_deb(file)
            elif file.suffix == ".zip":
                self.extract_zip(file)

    def extract_deb(self, file: Path):
        """Extracts the .deb release."""
        cwd = Path().cwd()

        # Create a directory to extract the .deb file. Syntax: mscl-<arch>-<python-ver>-<mscl-ver>
        parts = file.stem.split("_")
        arch, py_ver = parts[1], parts[2]
        mscl_versioned_name = f"mscl-{arch}-{py_ver}-{MSCL_VERSION}"
        mscl_versioned_dir = cwd / self.asset_dir / mscl_versioned_name

        # If output directory exists, remove it:
        if mscl_versioned_dir.exists():
            os.system(f"rm -rf {mscl_versioned_dir}")

        mscl_versioned_dir.mkdir(parents=True, exist_ok=True)
        file_relative = file.absolute().relative_to(mscl_versioned_dir, walk_up=True)

        # Extract the .deb file
        subprocess.run(["ar", "x", str(file_relative)], cwd=mscl_versioned_dir, check=True)

        # Extract the data.tar.gz file:
        data_tar = "data.tar.gz"

        subprocess.run(["tar", "-xzf", data_tar], cwd=mscl_versioned_dir, check=True)

        found_mscl_py = list(mscl_versioned_dir.rglob("mscl.py"))
        found_mscl_so = list(mscl_versioned_dir.rglob("_mscl.so"))

        if not found_mscl_py or not found_mscl_so:
            raise FileNotFoundError(f"Could not find mscl.py or _mscl.so in {mscl_versioned_dir}")

        # Move the extracted files to the root of the mscl_versioned_dir:
        mscl_py = found_mscl_py[0]
        mscl_so = found_mscl_so[0]

        mscl_py.rename(mscl_versioned_dir / mscl_py.name)
        mscl_so.rename(mscl_versioned_dir / mscl_so.name)

        # Delete the remaining files in mscl_versioned_dir:
        for f in mscl_versioned_dir.iterdir():
            if f.stem in (mscl_py.stem, mscl_so.stem):
                continue
            if f.is_dir():
                os.system(f"rm -rf {f}")
            else:
                f.unlink()

    def extract_zip(self, file: Path) -> None:
        """Extracts the .zip release."""

        cwd = Path().cwd()

        # Create a directory to extract the .zip file. Syntax: mscl-<arch>-<python-ver>-<mscl-ver>
        parts = file.stem.split("_")
        arch, py_ver = parts[2], parts[3]
        mscl_versioned_name = f"mscl-Windows-{arch}-{py_ver}-{MSCL_VERSION}"
        mscl_versioned_dir = cwd / self.asset_dir / mscl_versioned_name

        # If output directory exists, remove it:
        if mscl_versioned_dir.exists():
            os.system(f"rm -rf {mscl_versioned_dir}")

        mscl_versioned_dir.mkdir(parents=True, exist_ok=True)
        file_relative = file.absolute().relative_to(mscl_versioned_dir, walk_up=True)

        # Extract the .zip file
        subprocess.run(["unzip", str(file_relative)], cwd=mscl_versioned_dir, check=True)  # noqa: S603, S607

        found_mscl_py = list(mscl_versioned_dir.rglob("mscl.py"))
        found_mscl_pyd = list(mscl_versioned_dir.rglob("_mscl.pyd"))

        if not found_mscl_py or not found_mscl_pyd:
            raise FileNotFoundError(f"Could not find mscl.py or _mscl.pyd in {mscl_versioned_dir}")

        # Move the extracted files to the root of the mscl_versioned_dir:
        mscl_py = found_mscl_py[0]
        mscl_pyd = found_mscl_pyd[0]

        mscl_py.rename(mscl_versioned_dir / mscl_py.name)
        mscl_pyd.rename(mscl_versioned_dir / mscl_pyd.name)

        # Delete the remaining files in mscl_versioned_dir:
        for f in mscl_versioned_dir.iterdir():
            if f.stem in (mscl_py.stem, mscl_pyd.stem):
                continue
            if f.is_dir():
                os.system(f"rm -rf {f}")
            else:
                f.unlink()
