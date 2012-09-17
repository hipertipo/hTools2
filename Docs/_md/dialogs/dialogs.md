hTools2 currently contains two main groups of dialogs: generic dialogs and hDialogs. Each of these dialog groups is further sub-divided based on the context in which the dialogs operate.

These categories are used to organize the available scripts and dialogs in the ‘Extensions’ section of the RoboFont application menu.

## Generic dialogs

This group contains a broad set of dialogs to perform tasks to fonts with RoboFont.

These tools are general enough to work with all kinds of fonts, and do not require any special setup, naming of files etc. Some scripts might ask for the font to be saved to disk first.

### all fonts
 
scripts that perform actions to all open fonts in the RoboFont UI

### current font

scripts that deal only with the selected font in the RoboFont UI

### selected glyphs

scripts that perform actions to the selected glyphs in the current font

### current glyph

scripts that perform actions to the currently open glyph window

## hDialogs

The additional hDialogs are special dialogs which use hTools2 core objects, such as hWorld, hProject, hFont and hGlyph. These objects only work if a certain set of conventions are followed.

### hWorld

scripts that control global settings in hTools, for example ftp access data.

### hProject

scripts that use hProject objects to access data in libs, batch actions etc.

### hFont

scripts that wrap a hFont object around the current font in the RoboFont UI

### hGlyph

scripts that use the hGlyph objects to manipulate single glyphs
