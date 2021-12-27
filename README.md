# matpower-pip

Make MATPOWER installable from `pypi`. This package maintain MATPOWER version with custom pypi suffix such as `a`, `b`, `dev`, `post` , etc.

## Installation

```plaintext
pip install matpower
```

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

### Python

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

## Authors

* **Muhammad Yasirroni** - [yasirroni](https://github.com/yasirroni)

## Acknowledgement

This repository was supported by [Faculty of Engineering, Universitas Gadjah Mada](https://ft.ugm.ac.id/en/) under the supervision of [Mr. Sarjiya](https://www.researchgate.net/profile/Sarjiya_Sarjiya)
