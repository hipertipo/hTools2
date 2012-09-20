# [h] clean all pyc files from source

import os
import sys

from hTools2.modules.sysutils import clean_pyc

# get hTools2 path

for path in sys.path:
    if 'hTools2' in path:
        _path = path

_directory = os.listdir(_path)

clean_pyc(_directory, _path)
