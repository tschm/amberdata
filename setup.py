#!/usr/bin/env python

from setuptools import setup, find_packages
from pyamber import __version__ as version

setup(
    name='pyamber',
    version=version,
    packages=find_packages(include=["pyamber*"]),
    author='Thomas Schmelzer',
    author_email='thomas.schmelzer@gmail.com',
    url = 'https://github.com/tschm/amberdata',
    description='', install_requires=['requests>=2.22.0', 'pandas>=0.25.0'],
    license='LICENSE.txt'
)
