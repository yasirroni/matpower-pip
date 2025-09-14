import os
import re


class Matpower:
    # !WARNING: not tested under MATLAB
    def __new__(cls, path_matpower=None, engine="octave", save_path=False):
        return start_instance(
            path_matpower=path_matpower, engine=engine, save_path=save_path
        )

    # TODO: support install, uninstall, etc


def start_instance(
    path_matpower=None,
    engine="octave",
    save_path=False,
    suppress_warning=True,
):
    """
    Start octave or matlab instance by temporarily installing MATPOWER

    Parameters
    ----------
    path_matpower : str, optional
        String of path to matpower, by default None
    engine : str, optional
        Name of engine to run `.m` file, either 'octave' or 'matlab', by default
        'octave'
    save_path : bool, optional
        Save the new path as default function path, by default False
    suppress_warning : bool, optional
        Suppress warning in octave due to oct2py conversion, by default True

    Raises
    -------
    ImportError:
    ValueError: unknown engine name.

    Returns
    -------
    Oct2Py() | matlab.engine.start_matlab()
        Engine to run `.m` file
    """

    m = start_session(engine=engine)

    if engine == "octave" and suppress_warning:
        # NOTE: to suppress all warnings,
        #   `m.eval("warning('off', 'all')")`
        m.eval("warning('off', 'Octave:classdef-to-struct');")
        m.eval("warning('off', 'oct2py:pyeval:save_safe_struct:UnacceptableType');")

    if path_matpower is None:
        path_matpower = PATH_MATPOWER

    m.addpath(path_matpower)

    # modify my path, not save path, silently, remove existing path first
    m.install_matpower(1, 0, 0, 1)  # NOTE: this might cause warning rmpath()
    m.rmpath(path_matpower)

    if save_path:
        m.savepath()

    return m


def start_session(engine="octave"):
    if engine == "octave":
        # TODO:
        # Tell user to use `pip install matpower[octave]` or `pip install oct2py`
        try:
            from oct2py import Oct2Py

            m = Oct2Py()
        except ImportError:
            msg = (
                "No package named Oct2Py. Please install using `pip install"
                " matpower[octave]` or `pip install oct2py`."
            )
            raise ImportError(msg)
    elif engine == "matlab":
        try:
            import matlab.engine

            m = matlab.engine.start_matlab()
        except ImportError:
            msg = (
                "No package named matlab. You can install Oct2Py as free alternative"
                " of matlab using `pip install matpower[octave]` or `pip install"
                " oct2py`."
            )
            raise ImportError(msg)
    else:
        msg = (
            f"Unknown engine with name {engine}. Please choose between 'octave' or"
            f"'matlab'."
        )
        raise ValueError(msg)

    return m


def install_matpower(path_matpower=None, session=None, engine="octave", verbose=True):
    m = _install_matpower(
        path_matpower=path_matpower,
        session=session,
        engine=engine,
        verbose=verbose,
        process="install",
    )
    return m


def uninstall_matpower(path_matpower=None, session=None, engine="octave", verbose=True):
    m = _install_matpower(
        path_matpower=path_matpower,
        session=session,
        engine=engine,
        verbose=verbose,
        process="uninstall",
    )
    return m


def _install_matpower(
    path_matpower=None, session=None, engine="octave", verbose=True, process="install"
):
    """
    Install MATPOWER using install_matpower.m

    The API of install_matpower.m might change.
    This version is based on MATPOWER 8.1 install_matpower.m

    Parameters
    ----------
    path_matpower : str, optional
        String of path to matpower, by default None
    session : oct2py.Oct2Py | matlab.engine, optional
        oct2py.Oct2Py or matlab.engine object, by default None
    engine : str, optional
        Name of engine to run `.m` file, either 'octave' or 'matlab', by default
        'octave'
    verbose : bool, optional
        Verbosity of install_matpower, by default True
    process : str, optional
        'install' or 'uninstall', by default 'install'

    Returns
    -------
    oct2py.Oct2Py | matlab.engine
        oct2py.Oct2Py or matlab.engine session object.
    """
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
    # NOTE:
    #   install_matpower arguments:
    #       modify, save_it, verbose, rm_oldpaths
    if process == "install":
        # modify my path, save, remove existing path if exist
        m.install_matpower(1, 1, verbose, 1)
    else:
        # uninstall MATPOWER from path, must call savepath() to make permanent
        m.install_matpower(0, 0, verbose, 1)

        # bug on MATPOWER 8.1, examples is not deleted
        m.rmpath(os.path.join(path_matpower, "examples"))

    m.rmpath(path_matpower)
    m.savepath()

    return m


__MATPOWERPIP_VERSION__ = "2.2.3"

try:
    current_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(current_path, "CHANGES.md"), "rt", encoding="utf-8") as file:
        version_line = file.read()
    m = re.search(r"^Version [.a-zA-Z0-9]*", version_line, re.M)
    __MATPOWER_VERSION__ = m.group(0).split(" ")[1]

    version_info = __MATPOWER_VERSION__.split(".")
    if len(version_info) == 2:
        version_info.append("0")
    version_info.append(__MATPOWERPIP_VERSION__)

    __version__ = ".".join(version_info)

    PATH_MATPOWER = os.path.dirname(os.path.abspath(__file__))
    path_matpower = PATH_MATPOWER  # used for alias
    path_matpower_cases = os.path.join(path_matpower, "data")
    cases = os.listdir(path_matpower_cases)

except FileNotFoundError:
    print(
        "Can't find matpower package. This package will work as pure matpowerpip"
        " package."
    )
    __version__ = __MATPOWERPIP_VERSION__
    PATH_MATPOWER = None
    path_matpower = PATH_MATPOWER  # used for alias
    path_matpower_cases = None
    cases = []


# TODO:
# 1. Delete MATPOWER
# 2. Download and unzip MATPOWER
