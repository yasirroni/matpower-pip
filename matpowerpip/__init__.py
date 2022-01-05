import os
import re

def start_instance(path_matpower=None):
    from oct2py import Oct2Py

    if path_matpower is None:
        path_matpower = os.path.dirname(os.path.abspath(__file__))
            
    m = Oct2Py()
    m.addpath(m.genpath(path_matpower))

    return m

_suffix = "a2"
try:
    # matpower.__version__
    current_path = os.path.abspath(os.path.dirname(__file__))
    version_line = open(os.path.join(current_path, 'CHANGES.md'), "rt").read()
    m = re.search(r"^Version [.a-zA-Z0-9]*", version_line, re.M)

    __version__ = m.group(0).split(" ")[1] + _suffix
except:
    # matpowerpip.__version__
    __version__ = "0.0.1" + _suffix

path_matpower = os.path.dirname(os.path.abspath(__file__))