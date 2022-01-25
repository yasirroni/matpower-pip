import os
import re
import setuptools

current_path = os.path.abspath(os.path.dirname(__file__))

version_line = open(os.path.join(current_path, 'matpower/__init__.py'), "rt").read()
m = re.search(r"^_suffix = ['\"]([^'\"]*)['\"]", version_line, re.M)
_suffix = m.group(1)

version_line = open(os.path.join(current_path, 'matpower/CHANGES.md'), "rt").read()
m = re.search(r"^Version [.a-zA-Z0-9]*", version_line, re.M)
MATPOWER_VERSION = m.group(0).split(" ")[1]

version_info = MATPOWER_VERSION.split(".")
if len(version_info) == 2:
    version_info.append('0')
version_info.append(_suffix)

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
    packages = ["matpower"],
    package_data = {
        '': extra_files,
        'matpower':[
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
    python_requires = '>3.6',
    extras_require={
        "octave": [
            "oct2py>=5.2.0",
        ],
    }
)
