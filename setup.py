import os
import re
import setuptools

current_path = os.path.abspath(os.path.dirname(__file__))
version_line = open(os.path.join(current_path, 'matpowerpip/matpower/CHANGES.md'), "rt").read()
m = re.search(r"^Version [.a-zA-Z0-9]*", version_line, re.M)

suffix = "a0"
__version__ = m.group(0).split(" ")[1] + suffix

def package_files(directory_list):
    paths = []
    for directory in directory_list:
        for (path, _, filenames) in os.walk(directory):
            for filename in filenames:
                paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files([
    'matpowerpip/matpower/data',
    'matpowerpip/matpower/docker',
    'matpowerpip/matpower/docs',
    'matpowerpip/matpower/lib',
    'matpowerpip/matpower/mips',
    'matpowerpip/matpower/most',
    'matpowerpip/matpower/mp-opt-model',
    'matpowerpip/matpower/mptest'
    ])

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name = "matpower",
    version = __version__, # versions '0.0.x' are unstable and subject to refactor
    author = "Muhammad Yasirroni",
    author_email = "muhammadyasirroni@gmail.com",
    description = "Make MATPOWER installable from `pypi`.",
    long_description = long_description,
    url = "https://gitlab.com/yasirroni/matpower-pip",
    long_description_content_type = "text/markdown",
    packages = "matpowerpip/matpower",
    package_data = {
        '': extra_files,
        'matpowerpip/matpower':[
            'AUTHORS',
            'CHANGES.md',
            'CITATION',
            'CONTRIBUTING.md',
            'install_matpower.m',
            'LICENSE',
            'README.md'
            ]
    },
    classifiers = [
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering"
    ],
)
