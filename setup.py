#!/usr/bin/env python

from setuptools import setup
import os

with open(os.path.join(os.path.dirname(__file__), 'p1203Pv_extended', '__init__.py')) as version_file:
    version = eval(version_file.read().split("\n")[0].split("=")[1].strip())

setup(
    name='p1203Pv_extended',
    version=version,
    description='P.1203 Codec Extension',
    packages=['p1203Pv_extended'],
    author='Steve Goering',
    author_email='stg7@gmx.de',
    url='',
    py_modules=['p1203Pv_extended'],
    install_requires=[
      'scipy',
      'pandas'
    ]
)
