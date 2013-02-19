'''objects'''

import hTools2
reload(hTools2)

# debug

if hTools2.DEBUG:

    import hsettings
    reload(hsettings)

    import hworld
    reload(hworld)

    import hproject
    reload(hproject)

    import hspace
    reload(hspace)

    import hfont
    reload(hfont)

    import hglyph
    reload(hglyph)

    import hdocs
    reload(hdocs)

# import objects

from hsettings import hSettings
from hworld import hWorld
from hproject import hProject
from hspace import hSpace
from hfont import hFont
from hglyph import hGlyph
from hdocs import hDocs

# export object names

__all__ = [
    'hSettings',
    'hWorld',
    'hProject',
    'hSpace',
    'hFont',
    'hGlyph',
    'hDocs',
]
