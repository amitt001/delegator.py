#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import codecs

from setuptools import setup

try:
    # Python 3
    from os import dirname
except ImportError:
    # Python 2
    from os.path import dirname

here = os.path.abspath(dirname(__file__))

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()

required = [
    'pexpect>=4.1.0'
]

setup(
    name='delegator.py',
    version='0.0.14',
    description='Subprocesses for Humans 2.0.',
    long_description=long_description,
    author='Kenneth Reitz',
    author_email='me@kennethreitz.com',
    url='https://github.com/kennethreitz/delegator',
    py_modules=['delegator'],
    install_requires=required,
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
])
