# [h] create custom menu item

from AppKit import *

from lib.UI.fileBrowser import PathItem

#-----------------------------
# script by Frederik Berlaen
# http://typemytype.com/
# http://robofont.com/
#-----------------------------

## make this a start up script and you will always have your own menu items around and can order as you like :)

path = u"/_code/hTools2/Scripts/RoboFont/_projects"
menuName = "hFonts"

## create a new menu
menu = NSMenu.alloc().initWithTitle_(menuName)

## create a path item that will build the menu and connect all the callbacks
pathItem = PathItem(path, [".py"], isRoot=True)
pathItem.getMenu(title=menuName, parentMenu=menu)

## get the main menu
menubar = NSApp().mainMenu()

## search if the menu item already exists
newItem = menubar.itemWithTitle_(menuName)

if not newItem:
   ## if not create one and append it before the 'help'
   newItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(menuName, "", "")
   menubar.insertItem_atIndex_(newItem, menubar.numberOfItems()-1)

## set the menu as submenu
newItem.setSubmenu_(menu)
