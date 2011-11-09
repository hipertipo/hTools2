# [h] select projects

from hTools2.objects import hWorld, hProject
from hTools2.modules.fileutils import get_names_from_path

import vanilla

class hWorld_Dialog(object):

    _col1 = 180
    _col2 = 240
    _col3 = 240
    _margin = 15
    _footer = 100
    _height = 300

    def __init__(self, world):
        self.world = world
        self.projects = world.projects()
        self.w = vanilla.Window((self._col1 + self._col2 + self._col3 + (self._margin * 4), self._height), "batch project")
        # projects list
        #self.w.popUpButton = PopUpButton((10, 320, -10, 20), ["A", "B", "C"], callback=self.popUpButtonCallback)
        self.w.projects_list = vanilla.List(
            (self._margin, self._margin, self._col1, -self._footer),
            world.projects(),
            selectionCallback = self.projects_selection,
            allowsMultipleSelection=False)
        # masters list
        self.w.masters_list = vanilla.List(
            (self._col1 + (self._margin * 2), self._margin, self._col2, -self._footer),
            [],
            selectionCallback = self.masters_selection )
        # instances list
        self.w.instances_list = vanilla.List(
            (self._col1 + self._col2 + (self._margin * 3), self._margin, self._col3, -self._footer),
            [],
            selectionCallback = self.instances_selection)
        # apply button
        self.w.button_apply = vanilla.Button(
            (130, -45, 100, 30),
            "apply",
            callback=None)
        # close button
        self.w.button_close = vanilla.Button(
            (-130, -45, 100, 30),
            "close",
            callback=self.closeCallblack)
        # open
        self.w.open()

    def projects_selection(self, sender):
        _selected_projects = self.w.projects_list.getSelection()
        self.masters_clear()
        self.instances_clear()
        for _selected_project in _selected_projects:
            pName = self.projects[_selected_project]
            p = hProject(pName)
            # get masters
            masters = p.masters()
            if len(masters) > 0:
                for master in masters:
                    font_name = get_names_from_path(master)
                    self.w.masters_list.extend([font_name])
            else:
                self.w.masters_list.extend(['no ufo masters'])
            # get instances
            instances = p.instances()
            if len(instances) > 0:
                for instance in instances:
                    font_name = get_names_from_path(instance)
                    self.w.instances_list.extend([font_name])
            else:
                self.w.instances_list.extend(['no ufo instances'])

    def masters_selection(self, sender):
        #self.w.masters_list.getSelection()
        pass

    def instances_selection(self, sender):
        #self.w.masters_list.getSelection()
        pass

    def masters_clear(self):
        while len(self.w.masters_list.get()) > 0:
            del self.w.masters_list[0]

    def instances_clear(self):
        while len(self.w.instances_list.get()) > 0:
            del self.w.instances_list[0]

    def closeCallblack(self, sender):
        self.w.close()


w = hWorld()
p = hWorld_Dialog(w)

