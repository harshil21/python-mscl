"""Downloads the Github release assets for the mscl library."""

import os
from pathlib import Path

import requests
from github import Github
from github.GitRelease import GitRelease
from github.GitReleaseAsset import GitReleaseAsset


class GithubDownloader:
    """Manages downloading the Github release assets for the mscl library, along with the
    extracted files from this repository."""

    def __init__(self):
        self.github = Github(os.getenv("GITHUB_TOKEN"))
        self.mscl_repo = "LORD-MicroStrain/MSCL"
        self.python_mscl_repo = "harshil21/python-mscl"
        self.latest_release = None

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

    def download_release_assets(self, output_dir: str):
        """Downloads the release assets for the given repo and tag."""
        release = self.get_latest_release()
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        asset: GitReleaseAsset
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

            self.download_asset(output_path, asset)

    def download_asset(self, output_path: Path, asset: GitReleaseAsset) -> None:
        response = requests.get(asset.browser_download_url, timeout=15)
        asset_path = output_path / asset.name
        asset_path.write_bytes(response.content)

    def download_assets_from_folder(self, tag: str, folder_name: str) -> None:
        """Downloads all the files under the `folder_name` for the given tag, from the
        root of the repository."""

        repo = self.github.get_repo(self.python_mscl_repo)
        contents = repo.get_contents(folder_name, ref=tag)

        for content in contents:
            if content.type == "file":
                response = requests.get(content.download_url, timeout=15)
                file_path = Path(content.name)
                file_path.write_bytes(response.content)
