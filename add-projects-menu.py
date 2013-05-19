# [h] build a custom menu with scripts from different folders

## thanks Frederik!

from AppKit import *
import os

menuTitle = "Projects"

items = [
    ("path/to/pyFile", "name", "k"),
    ("path/to/pyFile", "othername", "m"),
]

## see https://developer.apple.com/library/mac/#documentation/cocoa/reference/applicationkit/classes/nsmenu_class/reference/reference.html
## and https://developer.apple.com/library/mac/#documentation/cocoa/reference/applicationkit/classes/NSMenuItem_Class/Reference/Reference.html#//apple_ref/doc/c_ref/NSMenuItem

menu = NSMenu.alloc().initWithTitle_(menuTitle)

for (path, title, shortcut) in items:
    menuItem = menu.addItemWithTitle_action_keyEquivalent_(title, "executeScript:", shortcut)    
    script = dict(fileName=os.path.basename(path), path=path)
    menuItem.setRepresentedObject_(script)
    menuItem.setKeyEquivalentModifierMask_(NSCommandKeyMask | NSControlKeyMask)

##menu2 = NSMenu.alloc().initWithTitle_('hello') 
menu.setSubmenu_('hello')

mainMenu = NSApp().mainMenu()
## check if the mainMenu has already this item with mainMenu.itemWithTitle_ (it will return None if the item doesnt exist)
newItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(menuTitle, "", "")

newItem.setSubmenu_(menu)
mainMenu.addItem_(newItem) ## or use insertItem_atIndex_(item, index)
