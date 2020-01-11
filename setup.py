#!/usr/bin/env python


import pathlib
import sys

from setuptools import find_packages, setup

from timeflake import __version__

assert sys.version >= "3.6", "Requires Python v3.6 or above."

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


setup(
    name="timeflake",
    version=__version__,
    author="Anthony Najjar Simon",
    url="https://github.com/anthonynsimon/timeflake",
    description="Timeflakes are 64-bit (unsigned), roughly-ordered, globally-unique, URL-safe IDs.",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["timeflake=timeflake.__main__:main",]},
    tests_require=[],
)
