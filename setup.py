#!/usr/bin/env python

from distutils.core import setup

# check for robofab / vanilla / mojo

setup(name="hTools2",
    version="1.5",
    description="A font-production toolkit for RoboFont.",
    author="Gustavo Ferreira",
    author_email="gustavo@hipertipo.com",
    url="http://hipertipo.com/",
    license="MIT",
    packages=["hTools2"],
    package_dir={"":"Lib"}
)