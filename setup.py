#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from setuptools import find_packages
from setuptools import setup

from pyamber import __version__ as version

# read the contents of your README file
with open("README.md") as f:
    long_description = f.read()

setup(
    name="pyamber",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version,
    packages=find_packages(include=["pyamber*"]),
    author="Thomas Schmelzer",
    author_email="thomas.schmelzer@gmail.com",
    url="https://github.com/tschm/amberdata",
    description="Utility code for interacting with amberdata",
    install_requires=["requests>=2.23.0", "pandas>=1.0.5"],
    license="MIT",
)
