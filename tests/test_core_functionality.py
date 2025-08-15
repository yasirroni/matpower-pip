import matpower
import numpy as np
from matpower import __MATPOWER_VERSION__, __MATPOWERPIP_VERSION__, Matpower
from oct2py import Oct2Py

"""Test using pytest
    # Windows
    # normal test
    copy matpowerpip\\__init__.py matpower\\__init__.py
    pytest -n auto -rA -c pyproject.toml --cov-report term-missing --cov=matpower

    # complete test, including example notebooks
    copy matpowerpip\\__init__.py matpower\\__init__.py
    pytest -rA -c pyproject.toml --cov-report term-missing --cov=matpower --nbmake

    # only run last failed test
    copy matpowerpip\\__init__.py matpower\\__init__.py
    pytest --lf -rA -c pyproject.toml --cov-report term-missing --cov=matpower --nbmake

    # Unix
    # normal test
    cp matpowerpip/__init__.py matpower/__init__.py
    pytest -n auto -rA -c pyproject.toml --cov-report term-missing --cov=matpower

    # complete test, including example notebooks
    cp matpowerpip/__init__.py matpower/__init__.py
    pytest -rA -c pyproject.toml --cov-report term-missing --cov=matpower --nbmake

    # only run last failed test
    cp matpowerpip/__init__.py matpower/__init__.py
    pytest --lf -rA -c pyproject.toml --cov-report term-missing --cov=matpower --nbmake

    # for specific test
    pytest -rA -c pyproject.toml --cov-report term-missing --cov=matpower tests/test_core_functionality.py::test_matpower_install
"""


def check_path_matpower_in_path(m):
    MATPOWER_IN_PATH = False
    for i in m.path().split(";"):
        if matpower.path_matpower in i:
            MATPOWER_IN_PATH = True
            break
    return MATPOWER_IN_PATH


def run_matpower(m):
    mpc = m.loadcase("case9")
    case9_gencost_val = np.array(
        [
            [2.000e00, 1.500e03, 0.000e00, 3.000e00, 1.100e-01, 5.000e00, 1.500e02],
            [2.000e00, 2.000e03, 0.000e00, 3.000e00, 8.500e-02, 1.200e00, 6.000e02],
            [2.000e00, 3.000e03, 0.000e00, 3.000e00, 1.225e-01, 1.000e00, 3.350e02],
        ]
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
    m = matpower.start_instance(engine="octave")
    run_matpower(m)
    MATPOWER_IN_PATH = check_path_matpower_in_path(m)
    assert MATPOWER_IN_PATH
    m.exit()


def test_matpower_start_instance_matpower_already_installed():
    # even when matpower already installed, it must be able to start
    m = Oct2Py()
    m.addpath(matpower.path_matpower)
    m.install_matpower(1, 1, 0, 1)  # mock install matpower outside start_instance()
    m.savepath()
    MATPOWER_IN_PATH = check_path_matpower_in_path(m)
    m.exit()
    assert MATPOWER_IN_PATH
    m = matpower.start_instance(engine="octave")
    MATPOWER_IN_PATH = check_path_matpower_in_path(m)
    m.exit()
    assert MATPOWER_IN_PATH


def test_matpower_install():
    # install matpower adds MATPOWER to path, permanently
    m = Oct2Py()
    m = matpower.install_matpower(
        path_matpower=matpower.path_matpower, session=m, verbose=False
    )
    m.exit()
    m = Oct2Py()
    MATPOWER_IN_PATH = check_path_matpower_in_path(m)
    assert MATPOWER_IN_PATH

    # uninstall matpower removes MATPOWER from path, permanently
    m = matpower.uninstall_matpower(
        path_matpower=matpower.path_matpower, session=m, verbose=False
    )
    m.exit()
    m = Oct2Py()
    MATPOWER_IN_PATH = check_path_matpower_in_path(m)
    assert MATPOWER_IN_PATH is False
    m.exit()


def test_matpower_as_class_octave():
    m = Matpower(engine="octave")
    run_matpower(m)
    m.exit()


def test_context_manager():
    """Make sure matpwoer works within a context manager"""

    case9_gencost_val = np.array(
        [
            [2.000e00, 1.500e03, 0.000e00, 3.000e00, 1.100e-01, 5.000e00, 1.500e02],
            [2.000e00, 2.000e03, 0.000e00, 3.000e00, 8.500e-02, 1.200e00, 6.000e02],
            [2.000e00, 3.000e03, 0.000e00, 3.000e00, 1.225e-01, 1.000e00, 3.350e02],
        ]
    )

    with Matpower(engine="octave") as m:
        mpc = run_matpower(m)

    # test value outside context
    assert np.allclose(mpc.gencost, case9_gencost_val)
    assert m._engine is None
