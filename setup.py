#!/usr/bin/env python
#coding=utf-8

import os
from setuptools import find_packages, setup


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="privu",
    version="0.0.1",
    description="A simple file upload/download web service.",
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'ReadMe.md'
        )
    ).read(),
    author="charles pan",
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    entry_points={
        "console_scripts": [
            "privu = privu.run:main",
        ]},
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.7.1'
    ]
)
