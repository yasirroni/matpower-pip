# Commands

Place to save some commands related to matpower-pip development, deployment, and maintenance.

## Download MATPOWER

### Windows (`cmd`)

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

Note: Sometimes it is not working from inside `vscode` terminal, since `vscode` use `powershell` instead of `cmd`. Try use to use windows `cmd` instead.

<!-- 
TODO: 
    1. Powershell command
 -->

### Python

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

## Delete dist

Delete old dist if exist to avoid the unexpected.

```powershell
del dist -Recurse -Force
del matpower.egg-info -Recurse -Force
```

```plaintext
del dist
del matpower.egg-info
```

## Backups

```plaintext
Xcopy /E /I matpower backups\matpower-7.1
```

## Restore matpower from backup

```plaintext
del matpower -Recurse -Force
Xcopy /E /I backups\matpower-7.1 matpower
copy matpowerpip\__init__.py matpower\__init__.py
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

## Push update

```plaintext
del matpower -Recurse -Force
Xcopy /E /I backups\matpower-7.1 matpower
copy matpowerpip\__init__.py matpower\__init__.py
del dist -Recurse -Force
del matpower.egg-info -Recurse -Force
py setup.py sdist
twine upload dist/*
```
