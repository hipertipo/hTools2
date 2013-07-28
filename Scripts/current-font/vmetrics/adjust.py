# [h] adjust vertical metrics

'''Adjust vertical metrics interactvely with sliders.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.font
    reload(hTools2.dialogs.font)

# import

from hTools2.dialogs.font import adjustVerticalMetrics

# run

adjustVerticalMetrics()
