## Selected glyphs


### actions

#### actions.py

![glyph actions](../_imgs/dialogs_glyphs_actions.png "glyph actions")

Displays a list of actions commonly applied to glyphs, such as remove overlaps, decompose, reverse contours, insert points at extremes etc. The user selects the options he needs, and uses the `apply` button to apply the actions to the selected glyphs.

#### delete.py

Deletes the selected glyphs from the font.

#### copy-paste.py

![copy paste](../_imgs/dialogs_glyphs_copy_paste.png "copy paste")

Copy and paste different kinds of data from one glyph to another.


### anchors

#### clear.py

Clears all anchors in the selected glyphs.

#### rename.py

Renames the anchors with `old name` in the selected glyphs to `new name`.

#### transfer.py

![transfer anchors](../_imgs/dialogs_glyphs_transfer_anchors.png "transfer anchors")

Transfers all anchors in the selected glyphs of one font to the same glyphs in a second font.


### color

#### paint-select.py

Gives access to the native color dialog, so the user can choose a custom color. The `paint` button applies the chosen color to the selected glyphs, while the `select` button selects all glyphs in the font with the same color.


### interpolate

#### interpolate.py

Interpolates `(A)` the selected glyphs in the current font with `(B)` the same glyphs in a second font into `(C)` an existing third font, with the specified `(x,y)` factors.


### layers

#### copy-to-layer.py

Copies the selected glyphs to a (new) layer with the specified name.

#### copy-to-mask.py

Copies the `foreground` layer of the selected glyphs in one font to the `mask` layer of the same glyphs in another font.

#### mask.py

Use the `copy` button to copy the contents of the `foreground` layer in the selected glyphs to the `mask` layer, and the `flip` button to switch their contents. The `clear` button deletes the contents of the `mask` layer.


### metrics

#### copy-margins.py

Copies the margins of the selected glyphs in the current font to the same glyphs in another font.

#### copy-width.py

Copies the width of the selected glyphs in the current font to the same glyphs in another font.

#### set-margins.py

Sets the values for the left/right margins of the selected glyphs. The options in the drop-down menu allow the user to chose between setting an exact value for the margins, or adding/subtracting it from the current values. It is also possible to set only the right or only the left margins.

#### set-width.py

Sets the width of the selected glyphs to the given value.


### name

#### change-suffix.py

Changes the suffix of the selected glyphs, from the value in `old suffix` to the value in `new suffix`.

#### print.py

Prints the names of the selected glyphs in the output window, as Python strings. Example:

    'a', 'b', 'c', 'e',


### transform

#### gridfit.py

![gridfit](../_imgs/dialogs_glyphs_gridfit.png "gridfit")

Fits one or more features of the selected glyphs to the given grid size. Options currently include `points`, `bPoints`, `margins`, `character width` and `anchors`.

#### move.py

![move glyphs](../_imgs/dialogs_glyphs_move.png "move glyphs")

Moves the selected glyphs by the given amount of units in the desired direction.

#### scale.py

![scale glyphs](../_imgs/dialogs_glyphs_scale.png "scale glyphs")

Scales the selected glyphs up or down by the given percentage. Users can choose if metrics should also be scaled: margins for scaling in the `x` dimension, and vertical metrics for scaling in the `y` dimension.

#### skew.py

![skew glyphs](../_imgs/dialogs_glyphs_skew.png "skew glyphs")

Skews the selected glyphs forward or backward by the specified angle. The user can choose if the axis of the skew transformation is the baseline (default), or the middle-point between baseline and x-height (useful when working on italics).

#### slide.py

Moves the selected glyphs interactively with the help of sliders. This has the same effect as using the `move` dialog, with less precision but instant feedback.


### unicode

#### auto.py

Automatically sets the unicode value for the selected glyphs, using the `auto_unicode(glyph)` function from `hTools.modules.encoding`.

#### clear.py

Clears the unicode(s) value(s) of the selected glyphs.


