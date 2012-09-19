## hLine

The `hLine` object makes it easy to typeset simple test strings with ufos in NodeBox.

## Attributes

### hLine.ctx

the NodeBox `context` object in which the glyphs and shapes are drawn

### hLine.font

the parent `hFont` object containing the glyphs to be drawn

### hLine.glyph_names

a list of glyph names to be drawn

### hLine.scale

scaling factor, a floating point number

### hLine.fill

turn fill on/off

### hLine.fill_color

the fill color, a NodeBox `color` object

### hLine.stroke_width

the width of the stroke, in NodeBox units

### hLine.stroke

turn stroke on/off

### hLine.stroke_color

the stroke color, a NodeBox `color` object

### hLine.hmetrics

draw guidelines for horizontal metrics

### hLine.hmetrics_crop

crop height of guides for horizontal metrics yes/no

### hLine.anchors

draw anchors yes/no

### hLine.anchors_size

### hLine.anchors_stroke_width

### hLine.anchors_stroke_color

### hLine.origin

draw an additional mark in origin of each glyph

### hLine.vmetrics

draw vertical metrics (x-height, ascenders, descenders, cap-height)

### hLine.baseline

### hLine.color_guidelines

the color of the guidelines, a NodeBox `color` object

### hLine.cap_style

the style of the line ends

### hLine.join_style

the style of the line joins


## Methods

### hLine.\_text\_to_gnames(text)

Converts a given character stream `text` into a list of glyph names, and returns the list.

### hLine.\_gnames\_to\_gstring(glyph_names)

Joins a given list of `glyph_names` into a `gstring` (a string of glyph names separated by slashes), and returns it.

### hLine.\_gstring\_to\_gnames(gstring)

Converts a given `gstring` into a list of `glyph_names`, and returns it.

### hLine.txt(text, mode='text')

Set the list `hLine.glyph_names` from the given `text` string.

If `text` is a normal stream of characters, use `mode='text'`; if `text` is a `gstring`, use `mode='gstring'`.

### hLine.width()

Return the width of the hLine object with the current settings.

### hLine.height()

Return the height of the hLine object with the current settings.

### hLine.draw(pos)

Draw the glyphs in the NodeBox context.
