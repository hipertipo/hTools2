# [h] select projects

import hTools2.modules.fileutils
reload(hTools2.modules.fileutils)

from hTools2.objects import hWorld, hProject
from hTools2.modules.fileutils import get_names_from_path

import vanilla

class hWorld_Dialog(object):

    def __init__(self, world):

        self.world = world
        self.projects = world.projects()
        self.w = vanilla.Window((660, 400), "hProjects browser")

        self.w.projects_list = vanilla.List((15, 15, 200, -60), world.projects(), selectionCallback=self.projects_selection, allowsMultipleSelection=False)
        self.w.masters_list = vanilla.List((230, 15, 400, -60), [], selectionCallback=self.masters_selection)

        self.w.button_apply = vanilla.Button((130, -45, 100, 30), "apply", callback=None)
        self.w.button_close = vanilla.Button((-130, -45, 100, 30), "close", callback=self.closeCallblack)

        self.w.open()

    def projects_selection(self, sender):
        _selected_projects = self.w.projects_list.getSelection()
        self.masters_clear()
        for _selected_project in _selected_projects:
            pName = self.projects[_selected_project]
            p = hProject(pName)
            masters = p.masters()
            if len(masters) > 0:
                #self.w.masters_list.extend(masters)
                for master in masters:
                    font_name = get_names_from_path(master)
                    self.w.masters_list.extend([font_name])
            else:
                self.w.masters_list.extend(['no ufo masters'])


    def masters_selection(self, sender):
        #self.w.masters_list.getSelection()
        pass

    def masters_clear(self):
        while len(self.w.masters_list.get()) > 0:
            del self.w.masters_list[0]

    def closeCallblack(self, sender):
        self.w.close()

w = hWorld()
p = hWorld_Dialog(w)

