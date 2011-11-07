# [h] select projects

from hTools2.objects import hWorld

import vanilla

class projects(object):

    def __init__(self, world):
        self.world = world
        self.w = vanilla.Window((300, 400), "hProjects")
        self.w.list = vanilla.List((15, 15, -15, -60), self.world.projects(), selectionCallback=self.selection)
        self.w.myButton = vanilla.Button((15, -45, -30, 30), "close", callback=self.okCallback)
        self.w.open()

    def okCallback(self, sender):
        print self.world.selected = self.w.list.getSelection()
        self.w.close()

w = hWorld()
p = projects(w)
