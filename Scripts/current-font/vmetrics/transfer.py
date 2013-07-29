# [h] transfer vmetrics

'''Transfer vertical metrics from one font to another.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.font
    reload(hTools2.dialogs.font)

# imports

from hTools2.dialogs.font import transferVMetricsDialog

# run

transferVMetricsDialog()
