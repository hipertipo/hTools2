#!/usr/bin/env python

from distutils.core import setup

# install

setup(name='hTools2',
    version='1.5',
    description='A font-production toolkit.',
    author='Gustavo Ferreira',
    author_email='gustavo@hipertipo.com',
    url='http://hipertipo.com/',
    license='BSD3',
    packages=[
        'hTools2',
        'hTools2.objects',
        'hTools2.modules',
        'hTools2.dialogs',
        'hTools2.extras',
    ],
    package_dir={'hTools2': 'Lib/hTools2'}
)
