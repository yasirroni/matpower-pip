import os
import re

import setuptools

current_path = os.path.abspath(os.path.dirname(__file__))

version_line = open(os.path.join(current_path, 'matpower/__init__.py'), "rt").read()
m = re.search(r"^__MATPOWERPIP_VERSION__ = ['\"]([^'\"]*)['\"]", version_line, re.M)
__MATPOWERPIP_VERSION__ = m.group(1)

version_line = open(os.path.join(current_path, 'matpower/CHANGES.md'), "rt").read()
m = re.search(r"^Version [.a-zA-Z0-9]*", version_line, re.M)
__MATPOWER_VERSION__ = m.group(0).split(" ")[1]

version_info = __MATPOWER_VERSION__.split(".")
if len(version_info) == 2:
    version_info.append('0')
version_info.append(__MATPOWERPIP_VERSION__)

__version__ = '.'.join(version_info)


def package_files(directory_list):
    paths = []
    for directory in directory_list:
        for (path, _, filenames) in os.walk(directory):
            for filename in filenames:
                paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files([
    'matpower/data',
    'matpower/docker',
    'matpower/docs',
    'matpower/lib',
    'matpower/mips',
    'matpower/most',
    'matpower/mp-opt-model',
    'matpower/mptest'
])

setuptools.setup(
    version=__version__,  # versions '0.0.x' are unstable and subject to refactor
    package_data={
        '': extra_files,
        'matpower': [
            'AUTHORS',
            'CHANGES.md',
            'CITATION',
            'CONTRIBUTING.md',
            'install_matpower.m',
            'LICENSE',
            'README.md'
        ]
    },
)
