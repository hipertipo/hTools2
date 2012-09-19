## All fonts

#### actions.py

Applies the selected actions to all open fonts. The available actions are:

- round points to integers
- decompose
- auto set contour order
- auto set contour direction
- remove overlaps
- add extreme points
- save .ufo
- close font

#### close.py

*Note: This script has no dialog.*

Closes all open font windows.

#### generate.py

A dialog to generate .otf fonts for all open fonts.

Use the `test install` button to temporarily install all open fonts for testing, using RoboFont’s ‘Test Install’ function. The fonts are removed from the system as soon as the fonts are closed.

Use the button `otfs folder` to select the destination folder for the .otfs, and the checkboxes to selected the desired actions (decompose, remove overlaps, PS autohint and release mode).

Finally, use the `generate` button to initiate the generation process.
