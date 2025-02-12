"""Downloads the Github release assets for the mscl library."""

import os
from pathlib import Path

import requests
from github import Github
from github.GitRelease import GitRelease
from github.GitReleaseAsset import GitReleaseAsset

from constants import ASSET_DIRECTORY, ReleaseAsset


class GithubDownloader:
    """Manages downloading the Github release assets for the mscl library, along with the
    extracted files from this repository."""

    def __init__(self):
        self.github = Github(os.getenv("GITHUB_TOKEN"))
        self.mscl_repo = "LORD-MicroStrain/MSCL"
        self.python_mscl_repo = "harshil21/python-mscl"
        self.latest_release = None
        self.asset_dir = Path(ASSET_DIRECTORY)

    def get_latest_release(self) -> GitRelease:
        """Returns the latest stable release for the given repo."""
        if self.latest_release:
            return self.latest_release

        releases = self.github.get_repo(self.mscl_repo).get_releases()
        for release in releases:
            if release.prerelease:
                continue
            if release.tag_name.startswith("v"):
                self.latest_release = release
                break
        return self.latest_release

    def download_release_assets(self, only_release: ReleaseAsset | None = None) -> None:
        """Downloads the release assets from the MSCL repository.

        Args:
            only_release: If set, only download the release asset for the given Python version and
                architecture. If not set, download all the release assets.
        """
        release = self.get_latest_release()
        output_path = Path(self.asset_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        asset: GitReleaseAsset
        print(f"Downloading release assets for {only_release=}")
        for asset in release.get_assets():
            # Don't download the "Documentation" or "Examples"
            if "Documentation" in asset.name or "Examples" in asset.name:
                continue
            # Don't download anything non-python:
            if "Python" not in asset.name:
                continue
            # Only python 3 and above:
            if "3" not in asset.name:
                continue

            # Extract the python version, arch, and platform from the only_release, if set:
            if only_release:
                if only_release.python_version not in asset.name:
                    continue
                if only_release.arch not in asset.name:
                    continue

            self.download_asset(output_path, asset)

    def download_asset(self, output_path: Path, asset: GitReleaseAsset) -> None:
        response = requests.get(asset.browser_download_url, timeout=15)
        asset_path = output_path / asset.name
        asset_path.write_bytes(response.content)
