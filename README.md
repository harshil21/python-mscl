# python-mscl

[![PyPI Downloads](https://static.pepy.tech/badge/python-mscl/week)](https://pepy.tech/projects/python-mscl)

Unofficial Python package for the [Microstrain Communication Library](https://github.com/LORD-MicroStrain/MSCL/tree/master).

This library just makes it so that we can install the MSCL library using pip, and directly provides the wheels!

Only Python 3.x wheels are provided. If you need Python 2.x wheels, please open an issue.

### Installation

```bash
pip install python-mscl
```

### Usage

```python
from python_mscl import mscl

# ... use the MSCL library as you normally would
```

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
3. Edit & run `uv run download_and_extract_assets.py` to fetch the latest tagged MSCL releases and extract them.
4. Run `uv run run_build.py`, which will build the source distribution and wheel for your python
version and architecture. The wheels will be placed in the `dist/` directory.

Notes for me, the maintainer:

5. Make sure that the constants in `constants.py` are updated, and that the MSCL repo still follows their
versioning system. If not, update rest of the files accordingly.

6. Optional: Run `uv publish` to publish the package to PyPI. To upload to TestPyPI, uncomment lines in `pyproject.toml`, and run `uv publish --index testpypi dist/*.whl`.

7. Optional: To check if the package worked correctly: `uv add --index https://test.pypi.org/simple/ --index-strategy unsafe-best-match python-mscl` in a new uv project directory.


## Issues:

If you encounter any issues, please open an issue on this repository. I would have to 
manually update this repository to the latest MSCL release. If it has been more than 48 hours since the latest release and I didn't update this repository, please open an issue. 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

