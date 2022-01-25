# Commands

Place to save some commands related to matpower-pip development and maintenance.

## Download MATPOWER

```plaintext
https://github.com/MATPOWER/matpower/releases/download/7.1/matpower7.1.zip
curl -L https://github.com/MATPOWER/matpower/archive/refs/tags/7.1.zip > matpower.zip
tar -xf matpower.zip
del matpower.zip
ren matpower-7.1 matpower
copy matpowerpip\__init__.py matpower\__init__.py
```

## Delete dist

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
del matpower
Xcopy /E /I backups\matpower-7.1 matpower
copy matpowerpip\__init__.py matpower\__init__.py
```