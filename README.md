# matpower-pip

Make [MATPOWER](https://github.com/MATPOWER/matpower) installable from `pypi`. This package make MATPOWER copy (currently Version `7.1`) as `python package` and maintain MATPOWER version with custom pypi suffix such as `a`, `b`, `dev`, `post` , etc. You can than use [`oct2py`](https://github.com/blink1073/oct2py) or `mypower` to run MATPOWER using octave client.

## Installation

For callable `matpower` via `oct2py` (require octave on environment system `PATH`):

```plaintext
pip install matpower[octave]
```

For downloading MATPOWER only:

```plaintext
pip install matpower
```

## Extra (require `oct2py`)

If `oct2py` also installed, `matpower.start_instance` can be used as `Oct2Py()` class with MATPOWER path added.

```python
from matpower import start_instance

m = start_instance()
mpc = m.eval('case9', verbose=False)
mpc = m.runpf(mpc)
```

```python
from matpower import start_instance

m = start_instance()
m.runpf() 
```

```python
from matpower import path_matpower

print(path_matpower) # matpower installation location
```

## Build for developer

### Download matpower

#### Windows

MATPOWER 7.1

```plaintext
https://github.com/MATPOWER/matpower/releases/download/7.1/matpower7.1.zip
curl -L https://github.com/MATPOWER/matpower/archive/refs/tags/7.1.zip > matpower.zip
tar -xf matpower.zip
del matpower.zip
ren matpower-7.1 matpower
copy matpowerpip\__init__.py matpower\__init__.py
```

MATPOWER 7.0

```plaintext
curl -L https://github.com/MATPOWER/matpower/releases/download/7.0/matpower7.0.zip > matpower.zip
tar -xf matpower.zip
del matpower.zip
ren matpower7.0 matpower
copy matpowerpip\__init__.py matpower\__init__.py
```

Note: Sometimes it is not working from inside `vscode`. Try use it on `cmd`

#### Python

Directly use `downloader.py`:

```plaintext
cd matpowerpip
py downloader.py
```

With `matpowerpip` (require `oct2py`):

```python
import matpowerpip

matpowerpip.downloader.download()
```

### deployment to pypi

For testing, use `testpypi`:

```plaintext
py setup.py sdist
py -m twine upload --repository testpypi dist/* --verbose 
```

For actual push to `pypi`:

```plaintext
py setup.py sdist
twine upload dist/*
```

## TODO

1. Update `mypower` to make `matpower-pip` as default `matpower` path.

## Authors

* **Muhammad Yasirroni** - [yasirroni](https://github.com/yasirroni)

## Acknowledgement

This repository was supported by [Faculty of Engineering, Universitas Gadjah Mada](https://ft.ugm.ac.id/en/) under the supervision of [Mr. Sarjiya](https://www.researchgate.net/profile/Sarjiya_Sarjiya)
