import numpy as np
import pytest

import matpower
from matpower import __MATPOWER_VERSION__, __MATPOWERPIP_VERSION__


"""Test using pytest

    pytest -rA -c pyproject.toml --cov-report term --cov=matpowerpip tests/
"""

class TestCoreFunctionality:
    @classmethod
    def setup_method(cls):
        pass

    def test_version(self):
        print(f"matpower.__version__: {matpower.__version__}")
        assert len(matpower.__version__.split(".")) == 6
        assert matpower.__version__.startswith(__MATPOWER_VERSION__) == True
        assert matpower.__version__.endswith(__MATPOWERPIP_VERSION__) == True

    def test_path(self):
        assert matpower.__path__[0] == matpower.path_matpower

    def test_instance_octave(self):
        m = matpower.start_instance(engine='octave')
        mpc = m.loadcase('case9')
        case9_gencost_val = np.array(
            [[2.000e+00, 1.500e+03, 0.000e+00, 3.000e+00, 1.100e-01, 5.000e+00, 1.500e+02],
             [2.000e+00, 2.000e+03, 0.000e+00, 3.000e+00, 8.500e-02, 1.200e+00, 6.000e+02],
             [2.000e+00, 3.000e+03, 0.000e+00, 3.000e+00, 1.225e-01, 1.000e+00, 3.350e+02]]
        )
        assert np.allclose(mpc.gencost, case9_gencost_val) == True

        # NOTE: install_matpowerwill fail if matpower already installed
        # TODO: Check path is in engine path or not
        # matpower.install_matpower(path_matpower=matpower.path_matpower, session=m, verbose=False)
        # matpower.uninstall_matpower(path_matpower=matpower.path_matpower, session=m, verbose=False)
