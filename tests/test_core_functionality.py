import numpy as np
import pytest
from oct2py import Oct2Py

try:
    import matlab.engine  # noqa: F401

    MATLAB_AVAILABLE = True
except ImportError:
    MATLAB_AVAILABLE = False

import matpower
from matpower import (
    __MATPOWER_VERSION__,
    __MATPOWERPIP_VERSION__,
    __MIPS_VERSION__,
    __MOST_VERSION__,
    __MPOPTMODEL_VERSION__,
    __MPTTEST_VERSION__,
    Matpower,
)

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


def _test_run_matpower(m):
    mpc = m.loadcase("case9")
    case9_gencost_val = np.array(
        [
            [2.000e00, 1.500e03, 0.000e00, 3.000e00, 1.100e-01, 5.000e00, 1.500e02],
            [2.000e00, 2.000e03, 0.000e00, 3.000e00, 8.500e-02, 1.200e00, 6.000e02],
            [2.000e00, 3.000e03, 0.000e00, 3.000e00, 1.225e-01, 1.000e00, 3.350e02],
        ]
    )

    engine_name = matpower._detect_engine(m)
    if engine_name == "octave":
        assert np.allclose(mpc.gencost, case9_gencost_val)
    elif engine_name == "matlab":
        assert np.allclose(mpc["gencost"], case9_gencost_val)
    else:
        raise ValueError(f"Unknown engine: {engine_name}")

    # TODO: test runpf able to change mpc
    mpc = matpower.run_matpower_cmd("runpf(mpc)", m=m, mpc=mpc)

    return mpc


def test_version():
    # test dynamic versioning
    print(f"matpower.__version__: {matpower.__version__}")
    assert len(matpower.__version__.split(".")) == 6
    assert matpower.__version__.startswith(__MATPOWER_VERSION__)
    assert matpower.__version__.endswith(__MATPOWERPIP_VERSION__)

    # test static versioning
    assert __MATPOWER_VERSION__ == "8.1"
    assert __MIPS_VERSION__ == "1.5.2"
    assert __MOST_VERSION__ == "1.3.1"
    assert __MPOPTMODEL_VERSION__ == "5.0"
    assert __MPTTEST_VERSION__ == "8.1"


def test_path():
    assert matpower.__path__[0] == matpower.path_matpower


def test_instance_none():
    m = matpower.start_instance()
    _test_run_matpower(m)
    assert matpower.path_matpower in m.path()
    m.exit()


def test_instance_octave():
    m = matpower.start_instance(engine="octave")
    _test_run_matpower(m)
    assert matpower.path_matpower in m.path()
    m.exit()


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
def test_instance_matlab():
    m = matpower.start_instance(engine="matlab")
    _test_run_matpower(m)
    assert matpower.path_matpower in m.path()
    m.exit()


def test_matpower_start_instance_matpower_already_installed():
    # even when matpower already installed, it must be able to start
    m = Oct2Py()
    m.addpath(matpower.path_matpower)
    m.install_matpower(1, 1, 0, 1)  # mock install matpower outside start_instance()
    m.savepath()
    assert matpower.path_matpower in m.path()
    m.exit()

    m = matpower.start_instance(engine="octave")
    assert matpower.path_matpower in m.path()
    m.exit()


def test_matpower_install():
    # install matpower adds MATPOWER to path, permanently
    m = Oct2Py()
    m = matpower.install_matpower(
        path_matpower=matpower.path_matpower, session=m, verbose=False
    )
    m.exit()
    m = Oct2Py()
    assert matpower.path_matpower in m.path()

    # uninstall matpower removes MATPOWER from path, permanently
    m = matpower.uninstall_matpower(
        path_matpower=matpower.path_matpower, session=m, verbose=False
    )
    m.exit()
    m = Oct2Py()
    assert matpower.path_matpower not in m.path()
    m.exit()


def test_matpower_as_class_octave():
    m = Matpower(engine="octave")
    _test_run_matpower(m)
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
        mpc = _test_run_matpower(m)

    # test value outside context
    assert np.allclose(mpc.gencost, case9_gencost_val)
    assert m._engine is None


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
def test_matpower_matlab_command():
    m = matpower.start_instance(engine="matlab")
    mpc = m.loadcase("case9")
    r1 = matpower.run_matlab_cmd("runopf(mpc)", m=m, mpc=mpc)

    assert r1["gen"].size[1] > mpc["gen"].size[1]  # runopf adds more columns to gen


def test_matpower_octave_command():
    m = matpower.start_instance(engine="octave")
    mpc = m.loadcase("case9")
    r1 = matpower.run_octave_cmd("runopf(mpc)", m=m, mpc=mpc)

    assert r1["gen"].shape[1] > mpc["gen"].shape[1]  # runopf adds more columns to gen


def test_matpower_command():
    r1 = matpower.run_matpower_cmd("runopf()")
    assert r1["gen"].shape[1] > 21
