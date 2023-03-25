import numpy as np
from oct2py import Oct2Py

import matpower
from matpower import __MATPOWER_VERSION__, __MATPOWERPIP_VERSION__, Matpower

"""Test using pytest
    # normal test
    copy matpowerpip\__init__.py matpower\__init__.py
    pytest -n auto -rA -c pyproject.toml --cov-report term-missing --cov=matpower

    # complete test, including example notebooks
    copy matpowerpip\__init__.py matpower\__init__.py
    pytest -n auto -rA -c pyproject.toml --cov-report term-missing --cov=matpower --nbmake

    # only run last failed test
    copy matpowerpip\__init__.py matpower\__init__.py
    pytest -n auto --lf -rA -c pyproject.toml --cov-report term-missing --cov=matpower --nbmake
"""


def check_path_matpower_in_path(m):
    MATPOWER_IN_PATH = False
    for i in m.path().split(';'):
        if matpower.path_matpower in i:
            MATPOWER_IN_PATH = True
            break
    return MATPOWER_IN_PATH


def run_matpower(m):
    mpc = m.loadcase('case9')
    case9_gencost_val = np.array(
        [[2.000e+00, 1.500e+03, 0.000e+00, 3.000e+00, 1.100e-01, 5.000e+00, 1.500e+02],
         [2.000e+00, 2.000e+03, 0.000e+00, 3.000e+00, 8.500e-02, 1.200e+00, 6.000e+02],
         [2.000e+00, 3.000e+03, 0.000e+00, 3.000e+00, 1.225e-01, 1.000e+00, 3.350e+02]]
    )
    assert np.allclose(mpc.gencost, case9_gencost_val)

    # TODO: test runpf able to change mpc
    mpc = m.runpf(mpc)

    return mpc

def test_version():
    print(f"matpower.__version__: {matpower.__version__}")
    assert len(matpower.__version__.split(".")) == 6
    assert matpower.__version__.startswith(__MATPOWER_VERSION__)
    assert matpower.__version__.endswith(__MATPOWERPIP_VERSION__)


def test_path():
    assert matpower.__path__[0] == matpower.path_matpower


def test_instance_octave():
    m = matpower.start_instance(engine='octave')
    run_matpower(m)


def test_matpower_install():
    # created instance must contains MATPOWER
    m = matpower.start_instance(engine='octave')
    MATPOWER_IN_PATH = check_path_matpower_in_path(m)
    assert MATPOWER_IN_PATH

    # purge_matpower removes MATPOWER from path
    m = matpower.purge_matpower(session=m)
    MATPOWER_IN_PATH = check_path_matpower_in_path(m)
    assert MATPOWER_IN_PATH is False

    # install matpower adds MATPOWER to path, permanently
    m = matpower.install_matpower(
        path_matpower=matpower.path_matpower,
        session=m,
        verbose=False)
    m.exit()
    m = Oct2Py()
    MATPOWER_IN_PATH = check_path_matpower_in_path(m)
    assert MATPOWER_IN_PATH

    # uninstall matpower removes MATPOWER from path, permanently
    m = matpower.uninstall_matpower(
        path_matpower=matpower.path_matpower,
        session=m,
        verbose=False)
    m.exit()
    m = Oct2Py()
    MATPOWER_IN_PATH = check_path_matpower_in_path(m)
    assert MATPOWER_IN_PATH is False


def test_matpower_as_class_octave():
    m = Matpower(engine='octave')
    run_matpower(m)



def test_context_manager():
    """Make sure matpwoer works within a context manager"""

    case9_gencost_val = np.array(
        [[2.000e+00, 1.500e+03, 0.000e+00, 3.000e+00, 1.100e-01, 5.000e+00, 1.500e+02],
         [2.000e+00, 2.000e+03, 0.000e+00, 3.000e+00, 8.500e-02, 1.200e+00, 6.000e+02],
         [2.000e+00, 3.000e+03, 0.000e+00, 3.000e+00, 1.225e-01, 1.000e+00, 3.350e+02]]
    )

    with Matpower(engine='octave') as m:
        mpc = run_matpower(m)

    # test value outside context
    assert np.allclose(mpc.gencost, case9_gencost_val)
    assert m._engine is None
