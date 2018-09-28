#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Setup Script."""

from setuptools import setup, find_packages


def _requirements():
    with open('requirements.txt') as _file:
        return _file.readlines()


setup(
    name="3scale-cli",
    version='0.1',
    description="Command line tool for Fabric8 3scale connect API",
    author='Ravindra Ratnawat',
    author_email="ravindra@redhat.com",
    license='MIT',
    url='https://github.com/fabric8-analytics/f8a-3scale-connect-api',
    py_modules=['run'],
    python_requires='>=3.4',
    packages=find_packages(),
    install_requires=_requirements(),
    entry_points='''
        [console_scripts]
        3scale=run:cli
    ''',
)
