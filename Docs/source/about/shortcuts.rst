==================
Keyboard shortcuts
==================

It is possible to configure keyboard shortcuts for ``hTools2`` scripts in RoboFont's ``Preferences/Extensions`` Window. In the section ``start-up scripts``, add the file ``add-RF-shortcuts.py``.

Here is an overview of all current keyboard schortcuts:

======= =================== ========================================
key     dialog              script
======= =================== ========================================
a       actions             selected-glyphs/actions/actions.py
c       paint select        selected-glyphs/color/paint-select.py
f       gridfit             selected-glyphs/transform/gridfit.py
h       set width           selected-glyphs/metrics/set-width.py
i       interpolate         selected-glyphs/interpol/interpolate.py
k       mask                selected-glyphs/layers/mask.py
l       copy to layer       selected-glyphs/layers/copy-to-layer.py
m       move                selected-glyphs/transform/move.py
o       copy to mask        selected-glyphs/layers/copy-to-mask.py
p       copy paste          selected-glyphs/actions/copy-paste.py
r       mirror              selected-glyphs/transform/mirror.py
s       scale               selected-glyphs/transform/scale.py
t       shift               selected-glyphs/transform/shift.py
v       adjust              current-font/vmetrics/adjust.py
w       skew                selected-glyphs/transform/skew.py
======= =================== ========================================

.. warning:: These shortcuts might clash with existing ones defined by other extensions or by the user.

.. note:: To customize the shortcuts used by ``hTools2``, simply edit the contents of the file ``add-RF-shortcuts.py``. It is recommended to save your custom shortcuts under a different file name, to avoid them from being overwritten in future ``hTools2`` code updates. Also, in the ``Preferences/Extensions`` Window, make sure that the correct (customized) script is set as a start-up script.
