from oct2py import Oct2Py
import os
import inspect

def make_octave_matpower(path_matpower=None, oc=None):
    if path_matpower is None:
        path_matpower = os.path.dirname(os.path.abspath(inspect.getfile(make_octave_matpower)))

    if oc is None:
        oc = Oct2Py()

    oc.addpath(oc.genpath(path_matpower)) # add path to matpower
    return oc

matpower = make_octave_matpower()