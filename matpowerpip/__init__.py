from oct2py import Oct2Py
import os
import inspect


path_matpower = os.path.dirname(os.path.abspath(__file__))

matpower = Oct2Py()
matpower.addpath(matpower.genpath(path_matpower))
