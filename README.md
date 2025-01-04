#python-mscl

Unofficial Python bindings for the [Microstrain Communication Library](https://www.microstrain.com/developers/microstrain-communication-library).

This library just makes it so that we can install the MSCL library using pip. Wheels are not provided. This will fetch the necessary files for your architecture and python
version, and then build the wheel for you.

It is therefore recommended to use a cache for your CI or package manager, unless you're okay with the ~20MB download every time you run your CI.

## Note: NOT PUBLISHED TO PYPI YET - STILL A WIP! CHECK BACK IN A FEW DAYS!

### Installation

```bash
pip install python-mscl
```

### Usage

```python
import mscl

# ... use the MSCL library as you normally would
```

## Local Development:

TODO