# matpower-pip

Make [MATPOWER](https://github.com/MATPOWER/matpower) installable from `pypi`. This package make MATPOWER copy (currently Version `7.1`) as `python package`. You can than use [`oct2py`](https://github.com/blink1073/oct2py) or `mypower` to run MATPOWER using octave client. `matlab.engine` also supported. For the latest docs, read [README on GitHub](https://github.com/yasirroni/matpower-pip#readme).

## Installation

For callable `matpower` via `oct2py` (require octave on environment system `PATH`):

```plaintext
pip install matpower[octave]
```

For downloading MATPOWER only:

```plaintext
pip install matpower
```

## Extra (require `oct2py` or `matlab.engine`)

If `oct2py` or `matlab.engine` is installed, `matpower.start_instance` can be used as `Oct2Py()` or `matlab.engine.start_matlab()` class with MATPOWER path added. Default engine is `octave`.

```python
from matpower import start_instance

m = start_instance()
m.runpf() 
```

```python
from matpower import start_instance

m = start_instance()
mpc = m.eval('case9', verbose=False)
mpc = m.runpf(mpc)
```

```python
from matpower import path_matpower

print(path_matpower) # matpower installation location
```

Since `[result] = runopf()` will make `result` contain unsupported `<object opf_model>`, we can avoid it by request maximum number of outputs using `nout='max_nout'` in `octave`.

```python
from matpower import start_instance

m = start_instance()

mpc = m.loadcase('case9');
mpopt = m.mpoption('verbose', 2);
[baseMVA, bus, gen, gencost, branch, f, success, et] m.runopf(mpc, mpopt, nout='max_nout')
```

Alternatively, it would be better to not parse back value that will not be use on python using `oct2py` `.eval` method. Use `;` to avoid octave print output on running the command.

```python
# import start_instance to start matpower instance
from matpower import start_instance

# start instance
m = start_instance()

# use octave native to run some commands
m.eval("mpopt = mpoption('verbose', 2);")
m.eval("mpc = loadcase('case9');")
m.eval("r1 = runopf(mpc, mpopt);") # we avoid parse `r1` that containts unsupported `<object opf_model>`

# fech data to python (.eval is used because .pull is not working in acessing field)
r1_mpc = {}
r1_mpc['baseMVA'] = m.eval('r1.baseMVA;')
r1_mpc['version'] = m.eval('r1.version;')
r1_mpc['bus'] = m.eval('r1.bus;')
r1_mpc['gen'] = m.eval('r1.gen;')
r1_mpc['branch'] = m.eval('r1.branch;')
r1_mpc['gencost'] = m.eval('r1.gencost;')

# modify variable if necessary
[GEN_BUS, PG, QG, QMAX, QMIN, VG, MBASE, GEN_STATUS, PMAX, PMIN, MU_PMAX, 
 MU_PMIN, MU_QMAX, MU_QMIN, PC1, PC2, QC1MIN, QC1MAX, QC2MIN, QC2MAX, 
 RAMP_AGC, RAMP_10, RAMP_30, RAMP_Q, APF] = m.idx_gen(nout='max_nout')
gen_index = 2 # index of generator to be changed
gen_index_ = int(gen_index - 1) # -1 due to python indexing start from 0
PMAX_ = int(PMAX -1) # -1 due to python indexing start from 0
r1_mpc['gen'][gen_index_,PMAX_] = 110 # in this example, we modify PMAX to be 110

[PQ, PV, REF, NONE, BUS_I, BUS_TYPE, PD, QD, GS, BS, 
 BUS_AREA, VM, VA, BASE_KV, ZONE, VMAX, VMIN, LAM_P, 
 LAM_Q, MU_VMAX, MU_VMIN] = m.idx_bus(nout='max_nout')
bus_index = 7 # index of bus to be changed
bus_index_ = int(bus_index - 1) # -1 due to python indexing start from 0
PD_ = int(PD-1) # -1 due to python indexing start from 0
r1_mpc['bus'][bus_index_,int(PD-1)] = 80 # in this example, we modify PD to be 150

# push back value to octave client
m.push('mpc', r1_mpc) # push r1_mpc in python to mpc in octave

# test if our pushed variable can be used
m.eval("r1 = runopf(mpc, mpopt);")

# test if we can retrive pushed value
mpc = m.pull('mpc')
```

Also support using `matlab.engine`.

```python
from matpower import start_instance

m = start_instance(engine='matlab') # specify using `matlab.engine` instead of `oct2py`
r = m.runpf('case5', nargout=0)
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

Delete old dist if exist to avoid the unexpected.

```powershell
del dist -Recurse -Force
del matpower.egg-info -Recurse -Force
```

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

## Versioning

This package maintain MATPOWER version with added version mark, i.e. `MATPOWER 7.1` become `7.1.0.x` where `x` come from `matpower-pip`. Furthermore `matpower-pip` also has its own versioning, but is not released on `pypi` since `matpower-pip` is restricted for development only (and development should use git instead).

## TODO

1. Update `mypower` to make `matpower-pip` as default `matpower` path.

## Authors

* **Muhammad Yasirroni** - [yasirroni](https://github.com/yasirroni)

## Acknowledgement

This repository was supported by [Faculty of Engineering, Universitas Gadjah Mada](https://ft.ugm.ac.id/en/) under the supervision of [Mr. Sarjiya](https://www.researchgate.net/profile/Sarjiya_Sarjiya)
