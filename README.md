# python-mscl

Unofficial Python package for the [Microstrain Communication Library](https://github.com/LORD-MicroStrain/MSCL/tree/master).

This library just makes it so that we can install the MSCL library using pip. Wheels are not provided. This will fetch the necessary files for your architecture and python
version, and then build the wheel for you.

It is therefore recommended to use a cache for your CI or package manager, unless you're okay with the ~20MB download every time you run your CI.

### Installation

```bash
pip install python-mscl
```

### Usage

```python
from python_mscl import mscl

# ... use the MSCL library as you normally would
```

### Windows support:

The latest mscl version (v67.0.0) only has a .zip for python 3.11. It has been confirmed that it does not work on other python versions (You would get an import error). However the build itself would still go through.


### Versioning system:

This repository follows the same versioning system as the MSCL library. This is reflected in the tags of this repository.

The version reflected in PyPI is as follows:

```
<MSCL_VERSION>.<REPO_VERSION>
```

E.g, there could be a version: `67.0.0.3` which would mean that the MSCL version is `67.0.0` and this is the third release of the python-mscl package.

## Local Development:

The below steps assume you have [`uv`](https://docs.astral.sh/uv/) installed.

1. Clone the repo and `cd` into it.
2. Optional: Create a .env file and insert your GITHUB_TOKEN= to make requests to the GitHub API.
3. Edit & run `uv run main.py` to fetch the latest tagged MSCL releases and extract them.
4. Run `uv build`, which will build the source distribution and wheel for your python
version and architecture.

Notes for me, the maintainer:
5. Optional: Run `uv publish` to publish the package to PyPI. To upload to TestPyPI, uncomment lines in `pyproject.toml`, and run `uv publish --index testpypi dist/*.tar.gz`.
6. Optional: To check if the package worked correctly: `uv add --index https://test.pypi.org/simple/ --index-strategy unsafe-best-match python-mscl` in a new uv project directory.


## Issues:

If you encounter any issues, please open an issue on this repository. I would have to 
manually update this repository to the latest MSCL release. If it has been more than 48 hours since the latest release and I didn't update this repository, please open an issue. 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

