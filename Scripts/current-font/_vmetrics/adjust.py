# [h] adjust vertical metrics

'''Adjust vertical metrics interactvely with sliders.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# import

from hTools2.dialogs import adjustVerticalMetrics

# run

adjustVerticalMetrics()
