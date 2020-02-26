#!/usr/bin/env python
from setuptools import setup, find_packages
from pyamber import __version__ as version

# read the contents of your README file
with open('README.md') as f:
    long_description = f.read()

setup(
    name='pyamber',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=version,
    packages=find_packages(include=["pyamber*"]),
    author='Thomas Schmelzer',
    author_email='thomas.schmelzer@gmail.com',
    url = 'https://github.com/tschm/amberdata',
    description='Utility code for interacting with amberdata', install_requires=['requests>=2.22.0', 'pandas>=0.25.0'],
    license="MIT"
)
