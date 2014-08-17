# [h] add hTools2 menu to RoboFont

"""Add hTools2 as a menu item in RoboFont's application menu."""

### thanks Frederik ###

import os
import sys

from AppKit import *

from lib.UI.fileBrowser import PathItem

def add_menu(name, path):
    # create a new menu
    menu = NSMenu.alloc().initWithTitle_(name)
    # create a path item that will build the menu and connect all the callbacks
    pathItem = PathItem(path, [".py"], isRoot=True)
    pathItem.getMenu(title=name, parentMenu=menu)
    # get the main menu
    menubar = NSApp().mainMenu()
    # search if the menu item already exists
    newItem = menubar.itemWithTitle_(name)
    if not newItem:
        # if not, create one and append it before `Help`
        newItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(name, "", "")
        menubar.insertItem_atIndex_(newItem, menubar.numberOfItems()-1)
    # set the menu as submenu
    newItem.setSubmenu_(menu)

menu_name = "hTools2"
scripts_path = os.path.join(os.getcwd(), 'Scripts')
add_menu(menu_name, scripts_path)
