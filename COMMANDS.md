# Commands

Place to save some commands related to matpower-pip development, deployment, and maintenance.

## Download MATPOWER

### Python

Directly use `downloader.py`:

```powershell
cd matpowerpip
py downloader.py
```

With `matpowerpip`:

```python
from matpowerpip.downloader import download_matpower, copy_init

download_matpower(matpower_version='8.0')
copy_init()
```

### Windows (`cmd`)

<!-- TODO: MATPOWER 8.0 -->

Note: Sometimes it is not working from inside `vscode` terminal, since `vscode` use `powershell` instead of `cmd`. Try use to use windows `cmd` instead.

<!-- 
TODO: 
    1. Powershell command for curl and tar
-->

<!-- 
### Mac (zsh)

```shell
cp matpowerpip/__init__.py matpower/__init__.py
```

-->

## Delete dist

Delete old dist if exist to avoid the unexpected.

```powershell
del dist -Recurse -Force
del matpower.egg-info -Recurse -Force
```

```powershell
del dist -Recurse -Force
del matpower.egg-info
```

## Backups

```powershell
Xcopy /E /I matpower backups\matpower-7.1
```

## Restore matpower from backup

```powershell
del matpower -Recurse -Force
Xcopy /E /I backups\matpower-7.1 matpower
copy matpowerpip\__init__.py matpower\__init__.py
```

### deployment to pypi

For testing, use `testpypi`:

```powershell
py setup.py sdist
py -m twine upload --repository testpypi dist/* --verbose 
```

For actual push to `pypi`:

```powershell
py setup.py sdist
twine upload dist/*
```

Using build

```powershell
python -m build
twine upload dist/*
```

```powershell
twine check dist/*
```

## Push update

```powershell
del matpower -Recurse -Force
Xcopy /E /I backups\matpower-7.1 matpower
copy matpowerpip\__init__.py matpower\__init__.py
del dist -Recurse -Force
del matpower.egg-info -Recurse -Force
py setup.py sdist
twine upload dist/*
```

## Developer install

```powershell
del matpower -Recurse -Force
Xcopy /E /I backups\matpower-7.1 matpower
copy matpowerpip\__init__.py matpower\__init__.py
pip install -e .
```

## Tags

```powershell
git tag -a v2.1.4 -m "v2.1.4: Fix start instance and install"
```

## Pandoc

```powershell
pandoc README.md -o README.pdf
```

## Zip repo

```shell
alias gitzip="git archive HEAD -o ${PWD##*/}.zip"
gitzip
```
