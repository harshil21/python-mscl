"""Entry point for downloading and extracting mscl release assets."""

import os
import platform
import sys

from build_helpers.release_downloader import GithubDownloader, ReleaseAsset
from build_helpers.release_extractor import ReleaseExtractor
from constants import MACHINE_MAPPING_TO_ARCH


def main(github_actions: bool = False) -> None:
    """Entry point to fetch the latest release assets from the Github repository & extract them.

    :param github_actions: If the script is running in a Github Actions environment. If true,
        the script will download and extract the release asset of only the python version and
        architecture and OS type detected.
    """
    gh = GithubDownloader()
    if github_actions:
        gh.download_release_assets(
            ReleaseAsset(
                python_version=f"Python{sys.version_info.major}.{sys.version_info.minor}",
                arch=MACHINE_MAPPING_TO_ARCH.get(platform.machine()),
            )
        )
    else:
        gh.download_release_assets()

    re = ReleaseExtractor()
    re.extract_assets()


if __name__ == "__main__":
    if os.getenv("GITHUB_ACTIONS", "false") == "true":
        main(github_actions=True)
    else:
        main()
