# [h] batch hProject

import hTools2.modules.fileutils
reload(hTools2.modules.fileutils)

from hTools2.objects import hWorld, hProject
from hTools2.modules.fileutils import get_names_from_path

from vanilla import *

class batchProjectDialog(object):

    _col1 = 160
    _col2 = 180
    _col3 = 100
    _col4 = 200
    _padding = 15
    _footer = 60
    _height = 400
    _checkbox_space = 20

    _masters = []
    _instances = []
    _selected_projects = []

    _open = True

    def __init__(self, world):
        self.world = world
        self.projects = world.projects()
        self._width = self._col1 + self._col2 + self._col3 + self._col4 + (self._padding * 5)
        self.w = FloatingWindow(
            #(800,
            (self._width,
            self._height),
            "batch hProject")
        # projects list
        self.w.projects_list = List(
            (self._padding,
            self._padding, self._col1, -self._footer),
            world.projects(),
            selectionCallback = self.projects_selection,
            allowsMultipleSelection=False)
        # masters list
        self.w.masters_list = List(
            (self._col1 + (self._padding * 2),
            self._padding,
            self._col2,
            -self._footer),
            self._masters,
            allowsMultipleSelection=True,
            selectionCallback = self.masters_selection )
        # instances list
        self.w.instances_list = List(
            (self._col1 + self._col2 + (self._padding * 3),
            self._padding,
            self._col3,
            -self._footer),
            self._instances,
            selectionCallback = self.instances_selection)
        # options
        self.w.open_checkBox = CheckBox(
            (self._col1 + self._col2 + self._col3 + (self._padding * 4),
            self._padding,
            -15,
            20),
            "open font window",
            value=self._open)
        # apply button
        self.w.button_apply = Button(
            (self._padding,
            -self._footer + self._padding,
            self._width/2 - (self._padding/2),
            30),
            "apply",
            callback=self.apply_callback)
        # close button
        self.w.button_close = Button(
            (self._padding + self._width/2 + (self._padding/2),
            -self._footer + self._padding,
            -self._padding,
            30),
            "close",
            callback=self.close_callback)
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
                    font_name = '%s' % get_names_from_path(master)[1]
                    self._masters.append(master)
                    self.w.masters_list.extend([font_name])
            else:
                self.w.masters_list.extend(['none'])
            # get instances
            instances = p.instances()
            if len(instances) > 0:
                for instance in instances:
                    font_name = '%s' % get_names_from_path(instance)[1]
                    self._instances.append(instance)
                    self.w.instances_list.extend([font_name])
            else:
                self.w.instances_list.extend(['none'])

    def masters_selection(self, sender):
        #self.w.masters_list.getSelection()
        pass

    def instances_selection(self, sender):
        #self.w.masters_list.getSelection()
        pass

    def masters_clear(self):
        self._masters = []
        self.w.masters_list.set([])

    def instances_clear(self):
        self._instances = []
        self.w.instances_list.set([])

    def apply_callback(self, sender):
        print 'batch hProject...\n'
        # masters
        _masters_selection = self.w.masters_list.getSelection()
        if len(_masters_selection) > 0:
            print '\tmasters:'
            for m in _masters_selection:
                _font_name = self.w.masters_list[m]
                print '\t\topening %s...' % _font_name
                _ufo = RFont(self._masters[m], showUI=True)
            print
        # instances
        _instances_selection = self.w.instances_list.getSelection()
        if len(_instances_selection) > 0:
            print '\tinstances:'
            for n in _instances_selection:
                _font_name = self.w.instances_list[n]
                print '\t\topening %s...' % _font_name
                _ufo = RFont(self._instances[n], showUI=True)
            print
        # done
        print "...done.\n"
            
    def close_callback(self, sender):
        self.w.close()


#------------------------------
# run

w = hWorld()
batchProjectDialog(w)

