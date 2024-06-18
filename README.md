# matpower-pip

[![PyPI version](https://badge.fury.io/py/matpower.svg)](https://pypi.org/project/matpower/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/yasirroni/matpower-pip/blob/master/LICENSE)
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.11626845.svg)](https://doi.org/10.5281/zenodo.11626845)

matpower-pip: A Python Package for Easy Access to MATPOWER Power System Simulation Package

This package is intended to make [MATPOWER](https://github.com/MATPOWER/matpower) installable from [`PyPI`](https://pypi.org/project/matpower/). We did not change anything from `MATPOWER` package, instead, we used a copy of `MATPOWER` (currently Version `8.0`) and wrapped it as `python package` published on PyPI. Use this package with [`mypower`](https://github.com/yasirroni/mypower) (the recommended way) or [`oct2py`](https://github.com/blink1073/oct2py) to run `MATPOWER` using `octave` client. `matlab.engine` is also supported. For the latest docs, read [README on GitHub](https://github.com/yasirroni/matpower-pip#readme).

This project is also listed on [related links](https://matpower.org/related-links/) on `MATPOWER` official website. Please visit that site to find other useful resources.

## Installation

### `matpower`

For downloading `MATPOWER` only (maybe you will run it using `matlab.engine` or any other method, or simply want an easy `MATPOWER` downloader):

```plaintext
pip install matpower
```

### `oct2py` (Windows)

For callable `matpower` via `oct2py` (require octave on environment system `PATH`). You can follow the [oct2py instalation tutorial in mypower repository](https://github.com/yasirroni/mypower/blob/master/README_INSTALL_OCTAVE_AND_OCT2PY.md).

## Usage

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yasirroni/matpower-pip/blob/master)

See `notebooks/` for complete examples. All examples should be compatible with Google Colab.

## Running with an engine (require `oct2py` or `matlab.engine`)

If `oct2py` or `matlab.engine` is installed, `matpower.start_instance` can be used to run `octave` or `MATLAB` with `MATPOWER` path added. The default engine is `octave`. You also can use `mypower` for added functionality as shown in [`mypower tutorial`](https://github.com/yasirroni/mypower/blob/master/tutorial.py).

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
from matpower import Matpower

with Matpower(engine='octave') as m:  # run as context manager
    mpc = m.eval('case9', verbose=False)
    mpc = m.runpf(mpc)

print(m._engine is None)  # engine cleanly terminated
```

```python
from matpower import path_matpower

print(path_matpower) # matpower installation location
```

Since `mpc = m.runopf()` will make `mpc` contain unsupported `<object opf_model>`, we can avoid it by requesting a maximum number of outputs using `nout='max_nout'` in `octave`.

```python
from matpower import start_instance

m = start_instance()

mpc = m.loadcase('case9')
mpopt = m.mpoption('verbose', 2)
[baseMVA, bus, gen, gencost, branch, f, success, et] = m.runopf(mpc, mpopt, nout='max_nout')
```

Alternatively, it would be better to not parse back values that will not be used on python using `oct2py` `.eval` method. Combine it with the use of `;` to avoid octave print output on running the command.

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

# test if we can retrive pushed value
mpc = m.pull('mpc')

# test if our pushed variable can be used
m.eval("r1 = runopf(mpc, mpopt);")
```

`matpower-pip` also support using `matlab.engine`.

```python
from matpower import start_instance

m = start_instance(engine='matlab') # specify using `matlab.engine` instead of `oct2py`
mpc = m.runpf('case5', nargout=0)
```

## Known engine issue

### Octave

1. `m.runopf()` will make `mpc` contain unsupported `<object opf_model>`. See: <https://github.com/MATPOWER/matpower/issues/134#issuecomment-1007798733>

    Impacted case:

    ```python
    r1 = m.runopf(mpc)
    ```

    Solution:

    ```python
    m.push('mpc', mpc)
    m.eval("r1 = runopf(mpc, mpopt);")

    r1_mpc = {}
    r1_mpc['baseMVA'] = m.eval('r1.baseMVA;')
    r1_mpc['version'] = m.eval('r1.version;')
    r1_mpc['bus'] = m.eval('r1.bus;')
    r1_mpc['gen'] = m.eval('r1.gen;')
    r1_mpc['branch'] = m.eval('r1.branch;')
    r1_mpc['gencost'] = m.eval('r1.gencost;')
    ```

## Versioning

This package maintains `MATPOWER` version with an added version mark, i.e. `MATPOWER 7.1` becomes `7.1.0.x.x.x` where the `.x.x.x` comes from `matpower-pip` versioning. The `matpower-pip` versioning is not released on `pypi` since `matpower-pip` is restricted for development only (and development should use git instead).

## TODO

1. `conda` and `docker` installation that includes octave-cli installation.

## Authors

* **Muhammad Yasirroni** - [yasirroni](https://github.com/yasirroni)

## Cite

We do request that publications derived from the use of `matpower-pip` explicitly acknowledge that fact by including all related [MATPOWER publications](https://github.com/MATPOWER/matpower#citing-matpower) and the following citation:

> M. Yasirroni, Sarjiya, and L. M. Putranto, "matpower-pip: A Python Package for Easy Access to MATPOWER Power System Simulation Package," [Online]. Available: <https://github.com/yasirroni/matpower-pip>.
> M. Yasirroni, Sarjiya, and L. M. Putranto, “matpower-pip”. Zenodo, Jun. 13, 2024. doi: 10.5281/zenodo.11626845.

```bibtex
@misc{matpower-pip,
  author       = {Yasirroni, M. and Sarjiya and Putranto, L. M.},
  title        = {matpower-pip: A Python Package for Easy Access to MATPOWER Power System Simulation Package},
  year         = {2023},
  howpublished = {\url{https://github.com/yasirroni/matpower-pip}},
}

@software{yasirroni_2024_11626845,
  author       = {Yasirroni, Muhammad and
                  Sarjiya, Sarjiya and
                  Putranto, Lesnanto Multa},
  title        = {matpower-pip},
  month        = jun,
  year         = 2024,
  publisher    = {Zenodo},
  version      = {8.0.0.2.1.8},
  doi          = {10.5281/zenodo.11626845},
  url          = {https://doi.org/10.5281/zenodo.11626845}
}
```

If a journal publication from the author appears soon should be cited instead.

## Contributing

See the [CONTRIBUTING.md](CONTRIBUTING.md).

## Acknowledgment

This repository was supported by the [Faculty of Engineering, Universitas Gadjah Mada](https://ft.ugm.ac.id/en/) under the supervision of [Mr. Sarjiya](https://www.researchgate.net/profile/Sarjiya_Sarjiya). If you use this package, we would be very glad if you cite any relevant publication under Mr. Sarjiya's name that can be found in the [semantic scholar](https://www.semanticscholar.org/author/Sarjiya/2267414) or [IEEE](https://ieeexplore.ieee.org/author/37548066400) in the meantime, since publication related to this repository is ongoing. This work is also partly motivated after I found out that `oct2py` supports running `octave` client from `python`, but the only implementation for running `MATPOWER` that I know is [oct2pypower](https://github.com/rwl/oct2pypower) which requires `docker` and is not newbie-friendly. Nevertheless, I would like to say thank you to all the people who have contributed to `oct2py`, `oct2pypower`, and more importantly `MATPOWER`.
