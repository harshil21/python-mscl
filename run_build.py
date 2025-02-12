"""Script to run the hatch build for a given python version and architecture."""

import itertools
import os
import platform
import subprocess
import sys

from constants import MACHINE_MAPPING_TO_ARCH


def run_hatch_build(python_version: str, build_arch: str) -> None:
    """Run the hatch build for the given Python version and architecture."""

    # modify_pyproject_toml(python_version, build_arch)
    env = os.environ.copy()
    env["PYTHON_BUILD_VERSION"] = python_version
    env["BUILD_ARCH"] = build_arch

    # Run the hatch build with the environment variables set:
    subprocess.run(["uv", "build", "--wheel"], check=True, env=env)


def main(github_actions: bool = False) -> None:
    """Entry point to run the hatch build for the given Python version and architecture.

    Make sure to have first downloaded and extracted the release assets from the Github repository.
    i.e. run `uv run download_and_extract_assets.py` before running this script.

    Args:
        github_actions: If the script is running in a Github Actions environment. If true, the
            script will run the hatch build for only the Python version and architecture detected.
    """

    # Iterate through the Python versions and architectures:
    # See the file names in the extracted folder for the exact names:
    # This must be the same as the dictionary in the hatch_build.py file
    python_versions = ["Python3.9", "Python3.10", "Python3.11", "Python3.12", "Python3.13"]
    build_architectures = ["amd64", "arm64", "armhf", "Windows-x64", "Windows-x86"]

    if github_actions:
        detected_python_version = f"Python{sys.version_info.major}.{sys.version_info.minor}"
        detected_arch = MACHINE_MAPPING_TO_ARCH.get(platform.machine())
        run_hatch_build(detected_python_version, detected_arch)

    else:
        for python_version, build_arch in itertools.product(python_versions, build_architectures):
            run_hatch_build(python_version, build_arch)


if __name__ == "__main__":
    if os.getenv("GITHUB_ACTIONS", "false") == "true":
        print("Building in Github Actions environment.")
        main(github_actions=True)
    else:
        print("Building locally")
        main()
