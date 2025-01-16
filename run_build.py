"""Script to run the hatch build for a given python version and architecture."""

import itertools
import os
import subprocess


def run_hatch_build(python_version: str, build_arch: str) -> None:
    """Run the hatch build for the given Python version and architecture."""

    # modify_pyproject_toml(python_version, build_arch)
    env = os.environ.copy()
    env["PYTHON_BUILD_VERSION"] = python_version
    env["BUILD_ARCH"] = build_arch

    # Run the hatch build with the environment variables set:
    subprocess.run(["uv", "build", "--wheel"], check=True, env=env)


def main() -> None:
    """Entry point to run the hatch build for the given Python version and architecture."""

    # Iterate through the Python versions and architectures:
    # See the file names in the extracted folder for the exact names:
    python_versions = ["Python3.9", "Python3.10", "Python3.11", "Python3.12", "Python3.13"]
    build_architectures = ["amd64", "arm64", "armhf", "Windows-x64", "Windows-x86"]

    for python_version, build_arch in itertools.product(python_versions, build_architectures):
        # Special case for windows:
        if "Windows" in build_arch:
            # Only Python 3.11 is supported for Windows:
            if python_version != "Python3.11":
                continue
            run_hatch_build(python_version, build_arch)
        else:
            run_hatch_build(python_version, build_arch)


if __name__ == "__main__":
    main()
