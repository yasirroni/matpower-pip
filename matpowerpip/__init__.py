import os
import re

PATH_MATPOWER = os.path.dirname(os.path.abspath(__file__))

# to support `from matpower import path_matpower`
path_matpower = PATH_MATPOWER

def start_instance(path_matpower=None, engine='octave', add_path=True, save_path=False):
    """Start octave or matlab instance

    Args:
        path_matpower (str, optional): path to matpower. Defaults to None.
        engine (str, optional): name of engine to run `.m` file, either 'octave' or 'matlab'. Defaults to 'octave'.
        add_path (bool, optional): add matpower to function path after start engine. Defaults to True.
        save_path (bool, optional): save the new path as default function path. Defaults to False.

    Raises:
        ValueError: unknown engine name.

    Returns:
        Oct2Py() or matlab.engine.start_matlab(): engine to run `.m` file
    """

    m = start_session(engine=engine)

    if add_path:
        if path_matpower is None:
            path_matpower = PATH_MATPOWER
            
        if save_path:
            m.eval(f"addpath(genpath('{path_matpower}')); savepath;")
        else:
            m.eval(f"addpath(genpath('{path_matpower}'))")

    return m

def start_session(engine='octave'):
    if engine == 'octave':
        # TODO:
        # Tell user to use `pip install matpower[octave]` or `pip install oct2py`
        try:
            from oct2py import Oct2Py
            m = Oct2Py()
        except ImportError:
            msg = f"No package named Oct2Py. Please install using `pip install matpower[octave]` or `pip install oct2py`."
            raise ImportError(msg)
    elif engine == 'matlab':
        import matlab.engine
        m = matlab.engine.start_matlab()
    else:
        msg = f"Unknown engine with name {engine}. Please choose between 'octave' or 'matlab'."
        raise ValueError(msg)

    return m

def install_matpower(path_matpower=None, session=None, engine='octave', verbose=True):
    m = _install_matpower(path_matpower=path_matpower, session=session, engine=engine, verbose=verbose, process='install')
    return m

def uninstall_matpower(path_matpower=None, session=None, engine='octave', verbose=True):
    m = _install_matpower(path_matpower=path_matpower, session=session, engine=engine, verbose=verbose, process='uninstall')
    return m

def _install_matpower(path_matpower=None, session=None, engine='octave', verbose=True, process='install'):
    if path_matpower is None:
        path_matpower = PATH_MATPOWER

    if session is None:
        m = start_session(engine=engine)
    else:
        m = session

    if verbose:
        verbose = 1
    else:
        verbose = 0

    m.addpath(path_matpower)
    if process == 'install':
        m.install_matpower(1, 1, verbose, 0)
    else:
        m.install_matpower(0, 0, verbose, 1)

    m.rmpath(path_matpower)
    m.savepath()

_suffix = "2.1.0"
try:
    # matpower.__version__
    current_path = os.path.abspath(os.path.dirname(__file__))
    version_line = open(os.path.join(current_path, 'CHANGES.md'), "rt").read()
    m = re.search(r"^Version [.a-zA-Z0-9]*", version_line, re.M)

    __version__ = m.group(0).split(" ")[1] + _suffix
except: # TODO: proper except: can't find 'CHANGES.md'
    # matpowerpip.__version__
    __version__ = _suffix

# TODO:
# 1. Delete MATPOWER
# 2. Download and unzip MATPOWER