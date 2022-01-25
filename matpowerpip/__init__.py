import os
import re

def start_instance(path_matpower=None, engine='octave'):
    """Start octave or matlab instance

    Args:
        path_matpower (str, optional): path to matpower. Defaults to None.
        engine (str, optional): Name of engine to run `.m` file, either 'octave' or 'matlab'. Defaults to 'octave'.

    Returns:
        Oct2Py() or matlab.engine.start_matlab(): engine to run `.m` file
    """
    if path_matpower is None:
        path_matpower = os.path.dirname(os.path.abspath(__file__))
    
    if engine == 'octave':
        from oct2py import Oct2Py
        m = Oct2Py()
    elif engine == 'matlab':
        import matlab.engine
        m = matlab.engine.start_matlab()
    else:
        msg = f"Unknown engine with name {engine}. Please choose between 'octave' or 'matlab'."
        raise ValueError(msg)

    m.addpath(m.genpath(path_matpower))

    return m

_suffix = "a3"
try:
    # matpower.__version__
    current_path = os.path.abspath(os.path.dirname(__file__))
    version_line = open(os.path.join(current_path, 'CHANGES.md'), "rt").read()
    m = re.search(r"^Version [.a-zA-Z0-9]*", version_line, re.M)

    __version__ = m.group(0).split(" ")[1] + _suffix
except: # TODO: proper except: can't find 'CHANGES.md'
    # matpowerpip.__version__
    __version__ = "0.0.2" + _suffix

path_matpower = os.path.dirname(os.path.abspath(__file__))