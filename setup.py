# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from backup import tools

readme_file = open("README.md", "rt").read()

setup(
    name="pyfanfou",
    version=tools.__version__,
    author="Xiaoke Zhang",
    author_email="mail@mcxiaoke.com",
    packages=find_packages(),
    scripts=["fanfoubackup.py"],
    url="https://github.com/mcxiaoke/pyfanfou",
    license="Apache License 2.0",
    keywords="exif image metadata photo",
    description=" ".join(tools.__doc__.splitlines()).strip(),
    long_description=readme_file,
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        #"Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        #"Programming Language :: Python :: 3.2",
        #"Programming Language :: Python :: 3.3",
        #"Programming Language :: Python :: 3.4",
        "Topic :: Utilities",
    ),
)
