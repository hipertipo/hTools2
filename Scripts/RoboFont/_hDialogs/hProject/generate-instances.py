# [h] : batch generate instances

import os

from vanilla import *

import hTools2.modules.fileutils
reload(hTools2.modules.fileutils)

import hTools2.objects
reload(hTools2.objects)

from hTools2.objects import hProject, hFont, hWorld
from hTools2.modules.fontinfo import set_names
from hTools2.modules.fileutils import delete_files

class generateInstancesDialog(object):

    _title = "hProject"
    _col1 = 120
    _col3 = 40
    _col_height = 160
    _padding = 10
    _row_height = 18
    _bar_height = 18
    _button_height = 30
    _button_width = 60
    _height = _col_height + (_button_height * 3) + _bar_height + (_padding * 4) + 3
    _width = _col1 + _col3 + (_padding * 2) - 1

    _masters = []
    _masters_i = []
    _instances = []
    _selected_projects = []
    _open = True

    _projects = [ 'Jornalistica', 'Guarana', 'Magnetica', 'Mechanica', 'Publica', 'Quantica', 'Synthetica' ]
    _instances = [ 25, 35, 45, 65, 75, 85 ]

    def __init__(self):
        self.world = hWorld()
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title)
        # projects list
        _checkboxes = 0
        x = self._padding
        y = self._padding
        self.w.projects_list = List(
                    (x, y,
                    self._col1,
                    self._col_height),
                    self._projects,
                    # selectionCallback=self.projects_selection,
                    allowsMultipleSelection=True)
        # masters list
        x += self._col1 - 1
        self.w.instances_list = List(
                    (x, y,
                    self._col3,
                    self._col_height),
                    self._instances,
                    allowsMultipleSelection=True)
        # options
        x = self._padding
        y = self._col_height + (self._padding * 2)
        # generate ufo
        self.w.generate_ufo = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "generate .ufo",
                    value=False,
                    sizeStyle='small')
        y += self._row_height
        # set font data
        self.w.set_info = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "set font data",
                    value=False,
                    sizeStyle='small')
        y += self._row_height
        # generate test otf
        self.w.generate_otf_test = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "generate test .otf",
                    value=False,
                    sizeStyle='small')
        y += self._row_height + self._padding
        # apply button
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "generate instances",
                    callback=self._generate_callback,
                    sizeStyle='small')
        # progress bar
        x = self._padding
        y += self._button_height + self._padding
        self.w.bar = ProgressBar(
                    (x, y,
                    -self._padding,
                    self._bar_height),
                    isIndeterminate=True,
                    sizeStyle='small')
        # open
        self.w.open()

    # callbacks

    def _generate_callback(self, sender):
        # get parameters
        _projects_i = self.w.projects_list.getSelection()
        _instances_i = self.w.instances_list.getSelection()
        _set_info = self.w.set_info.get()
        _ufo = self.w.generate_ufo.get()
        _otf_test = self.w.generate_otf_test.get()
        # generate instances
        if len(_projects_i) > 0 and len(_instances_i) > 0:
            self.w.bar.start()
            print 'generating instances...\n'
            for project_i in _projects_i:
                project_name = self._projects[project_i]
                p = hProject(project_name)
                for instance_i in _instances_i:
                    instance_name = str(self._instances[instance_i])
                    file_name = '%s_%s.ufo' % (project_name, instance_name)
                    file_path = os.path.join(p.paths['instances'], file_name)
                    print '\tgenerating instance for %s %s...' % (project_name, instance_name)
                    # generate ufo
                    if _ufo:
                        print '\t\tgenerating ufo...',
                        p.generate_instance(instance_name, verbose=False)
                        print os.path.exists(file_path)
                    # set font data
                    if _set_info:
                        print '\t\tsetting data...'
                        font = hFont(RFont(file_path, showUI=False))
                        font.set_names()
                        font.import_groups_from_encoding()
                        font.paint_groups()
                        font.auto_unicodes()
                        font.ufo.save()
                    # generate otf test
                    if _otf_test:
                        font = hFont(RFont(file_path, showUI=True))
                        print '\t\tgenerating test otf...'
                        font.generate_otf(test=True)
                        font.ufo.close()
                    # done with instance
                    print
                # done with project
            # done
            self.w.bar.stop()
            print '...done.\n'

# run

generateInstancesDialog()
