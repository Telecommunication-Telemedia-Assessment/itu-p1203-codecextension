#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='p1203Pv_extended',
    version='0.1',
    description='p1203Pv_extended',
    author='Steve Goering',
    author_email='stg7@gmx.de',
    url='',
    packages=find_packages(),
    install_requires=[
      'scipy',
      'pandas'
    ],
    package_dir={'p1203Pv_extended': 'p1203Pv_extended'},
)
