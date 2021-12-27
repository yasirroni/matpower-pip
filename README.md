# matpower-pip

Make MATPOWER installable from `pypi`. This package make MATPOWER copy (currently Version `7.1`) as `python package` and maintain MATPOWER version with custom pypi suffix such as `a`, `b`, `dev`, `post` , etc. You can than use `oct2py` or `mypower` to run MATPOWER using octave client.

## Installation

```plaintext
pip install matpower
```

## Usage

Use `oct2py` or `mypower` on `matpower`.

## Build for developer

### Download matpower

#### Windows

```plaintext
curl -L https://github.com/MATPOWER/matpower/archive/refs/tags/7.1.zip > matpower.zip
tar -xf matpower.zip
del matpower.zip
ren matpower-7.1 matpower
copy NUL matpower\__init__.py
```

Note: Sometimes it is not working from inside `vscode`. Try use it on `cmd`

#### Python

```plaintext
py matpower_dowloader.py
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

1. Add dynamic "__version__"

2. Make importable using `oct2py`

3. Update `mypower` to make `matpower-pip` as default `matpower` path.

## Authors

* **Muhammad Yasirroni** - [yasirroni](https://github.com/yasirroni)

## Acknowledgement

This repository was supported by [Faculty of Engineering, Universitas Gadjah Mada](https://ft.ugm.ac.id/en/) under the supervision of [Mr. Sarjiya](https://www.researchgate.net/profile/Sarjiya_Sarjiya)
