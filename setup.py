#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from os.path import dirname, join

from setuptools import find_packages, setup

setup(
    name='pan-tilt-follow',
    version='0.0.1',
    description='Open house python demo',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='',
    author_email='',
    url='https://github.com/EdmontonPy/pan-tilt-follow',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # See: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords=[
    ],
    scripts=[
        'main.py',
    ],
    install_requires=[
        'opencv-contrib-python>=3.4.3.18',
        'opencv-python>=3.4.3.18',
        'pigpio>=1.44',
        'evdev>=1.2.0',
    ],
)
