# [h] init hTools2 extension

import os
import sys

from AppKit import *

from lib.UI.fileBrowser import PathItem

# add hTools2 to RoboFont main menu

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
scripts_folder = os.path.join(os.getcwd(), 'Scripts')
add_menu(menu_name, scripts_folder)

# add hTools2 modules to sys.path

sys.path.append(os.path.dirname(__file__))
