"""Entry point for scripts."""

from build_helpers.release_downloader import GithubDownloader
from build_helpers.release_extractor import ReleaseExtractor


def main():
    GithubDownloader()
    # gh.download_release_assets("mscl_release_assets")
    re = ReleaseExtractor()
    re.extract_assets()


if __name__ == "__main__":
    main()
