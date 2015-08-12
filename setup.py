# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from lib import const
from lib import backup

readme_file = open("README.md", "rt").read()

setup(
    name="pyfanfou",
    version=const.APP_VERSION,
    author="Xiaoke Zhang",
    author_email="mail@mcxiaoke.com",
    packages=find_packages(),
    scripts=["fanfoubackup.py"],
    url="https://github.com/mcxiaoke/pyfanfou",
    license="Apache License 2.0",
    keywords="fanfou.com, fanfou, backup, Tkinter",
    description=const.APP_NAME,
    long_description=readme_file,
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        #"Programming Language :: Python :: 3.2",
        #"Programming Language :: Python :: 3.3",
        #"Programming Language :: Python :: 3.4",
        "Topic :: Utilities",
    ),
)
