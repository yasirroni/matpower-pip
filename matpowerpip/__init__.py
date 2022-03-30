import os
import re

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
            path_matpower = os.path.dirname(os.path.abspath(__file__))
            
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
    m = _meta_install_matpower(path_matpower=path_matpower, session=session, engine=engine, verbose=verbose, process='install')
    return m

def uninstall_matpower(path_matpower=None, session=None, engine='octave', verbose=True):
    m = _meta_install_matpower(path_matpower=path_matpower, session=session, engine=engine, verbose=verbose, process='uninstall')

    # remove matpower-pip path
    m.rmpath(path_matpower)
    m.savepath()

    return m

def _meta_install_matpower(path_matpower=None, session=None, engine='octave', verbose=True, process='install'):
    if session is None:
        m = start_session(engine=engine)
    else:
        m = session
    
    if path_matpower is None:
        path_matpower = os.path.dirname(os.path.abspath(__file__))

    if verbose:
        verbose = 1
    else:
        verbose = 0
    
    if process == 'install':
        process = 1
    else:
        process = 0

    m.addpath(path_matpower)
    m.install_matpower(1, 1, verbose, process)

    return m

_suffix = "2.post1"
try:
    # matpower.__version__
    current_path = os.path.abspath(os.path.dirname(__file__))
    version_line = open(os.path.join(current_path, 'CHANGES.md'), "rt").read()
    m = re.search(r"^Version [.a-zA-Z0-9]*", version_line, re.M)

    __version__ = m.group(0).split(" ")[1] + _suffix
except: # TODO: proper except: can't find 'CHANGES.md'
    # matpowerpip.__version__
    __version__ = "0.0.2." + _suffix

path_matpower = os.path.dirname(os.path.abspath(__file__))

# TODO:
# 1. Delete MATPOWER
# 2. Download and unzip MATPOWER