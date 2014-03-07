# [h] clean all pyc files from source

# imports

import os
import sys

from hTools2.modules.sysutils import clean_pyc

# get hTools2 path

for path in sys.path:
    if 'hTools2' in path:
        if path.endswith('hTools2/Lib'):
            _path = path

# delete all .pyc files

_dir = os.listdir(_path)
clean_pyc(_dir, _path)
