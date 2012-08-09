# [h] hSpace

# reload when debugging

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hproject
    reload(hproject)

    import hfont
    reload(hfont)

    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

# imports

import os

try:
    from mojo.roboFont import RFont
except:
    from robofab.world import RFont

from hproject import hProject
from hfont import hFont
from hTools2.modules.fontutils import parse_glyphs_groups, get_full_name

# object

class hSpace:

    '''An object to represent a parametric variation space inside `hWorld`.'''

    #------------
    # attributes
    #------------

    # a dictionary containing parameter names and related value ranges
    parameters = {}

    # a list with the order in which the parameters appear
    parameters_order = []

    # a dictionary of parametric font names in the current `hSpace`
    fonts = {}

    #---------
    # methods
    #---------

    def __init__(self, project_name):
        self.project = hProject(project_name)
        self.import_project_parameters()
        self.build()

    def import_project_parameters(self):
        '''Import project parameters from lib.'''
        try:
            self.parameters = self.project.libs['project']['parameters']
            self.parameters_order = self.project.libs['project']['parameters_order']
            self.parameters_separator = self.project.libs['project']['parameters_separator']
        except:
            print 'project %s has no parameters lib' % self.project.name

    def build(self):
        '''Build the defined variation space, using the parameters order, and create individual font names.'''
        parts = len(self.parameters_order)
        font_names = []
        if parts == 0:
            print 'parameters order is empty, please set some values first.\n'
        elif parts == 1:
            param_name = self.parameters_order[0]
            for a in self.parameters[param_name]:
                style_name = '%s' % a
                font_names.append(style_name)
        elif parts == 2:
            param_name_1 = self.parameters_order[0]
            param_name_2 = self.parameters_order[1]
            for a in self.parameters[param_name_1]:
                for b in self.parameters[param_name_2]:
                    if self.parameters_separator:
                        style_name = '%s-%s' % (a, b)
                    else:
                        style_name = '%s%s' % (a, b)
                    font_names.append(style_name)
        elif parts == 3:
            param_name_1 = self.parameters_order[0]
            param_name_2 = self.parameters_order[1]
            param_name_3 = self.parameters_order[2]
            for a in self.parameters[param_name_1]:
                for b in self.parameters[param_name_2]:
                    for c in self.parameters[param_name_3]:
                        if self.parameters_separator:
                            style_name = '%s-%s-%s' % (a, b, c)
                        else:
                            style_name = '%s%s%s' % (a, b, c)
                        font_names.append(style_name)
        elif parts == 4:
            param_name_1 = self.parameters_order[0]
            param_name_2 = self.parameters_order[1]
            param_name_3 = self.parameters_order[2]
            param_name_4 = self.parameters_order[3]
            for a in self.parameters[param_name_1]:
                for b in self.parameters[param_name_2]:
                    for c in self.parameters[param_name_3]:
                        for d in self.parameters[param_name_4]:
                            if self.parameters_separator:
                                style_name = '%s-%s-%s-%s' % (a, b, c, d)
                            else:
                                style_name = '%s%s%s%s' % (a, b, c, d)
                            font_names.append(style_name)
        elif parts == 5:
            param_name_1 = self.parameters_order[0]
            param_name_2 = self.parameters_order[1]
            param_name_3 = self.parameters_order[2]
            param_name_4 = self.parameters_order[3]
            param_name_5 = self.parameters_order[4]
            for a in self.parameters[param_name_1]:
                for b in self.parameters[param_name_2]:
                    for c in self.parameters[param_name_3]:
                        for d in self.parameters[param_name_4]:
                            for e in self.parameters[param_name_5]:
                                if self.parameters_separator:
                                    style_name = '%s-%s-%s-%s-%s' % (a, b, c, d, e)
                                else:
                                    style_name = '%s%s%s%s%s' % (a, b, c, d, e)
                                font_names.append(style_name)
        elif parts == 6:
            param_name_1 = self.parameters_order[0]
            param_name_2 = self.parameters_order[1]
            param_name_3 = self.parameters_order[2]
            param_name_4 = self.parameters_order[3]
            param_name_5 = self.parameters_order[4]
            param_name_6 = self.parameters_order[5]
            for a in self.parameters[param_name_1]:
                for b in self.parameters[param_name_2]:
                    for c in self.parameters[param_name_3]:
                        for d in self.parameters[param_name_4]:
                            for e in self.parameters[param_name_5]:
                                for f in self.parameters[param_name_6]:
                                    if self.parameters_separator:
                                        style_name = '%s-%s-%s-%s-%s-%s' % (a, b, c, d, e, f)
                                    else:
                                        style_name = '%s%s%s%s%s%s' % (a, b, c, d, e, f)
                                    font_names.append(style_name)
        else:
            print 'too many parts, current hSpace implementation only supports 6 parameters.\n'
        # save font list
        self.fonts = font_names

    def ufos(self):
        '''Return a list containing the `.ufo` paths of the existing fonts in the current `hSpace`.'''
        font_paths = []
        masters = self.project.masters()
        instances = self.project.instances()
        for style_name in self.fonts:
            font_name = '%s_%s.ufo' % (self.project.name, style_name)
            master_path = os.path.join(self.project.paths['ufos'], font_name)
            instance_path = os.path.join(self.project.paths['instances'], font_name)
            if os.path.exists(master_path):
                font_paths.append(master_path)
            elif os.path.exists(master_path):
                font_paths.append(instance_path)
            else:
                continue
        return font_paths

    # functions

    def transfer_glyphs(self, gstring, var, ranges):
        axis, src, dest = var
        # define source space
        for param in self.parameters.keys():
            if param == axis:
                self.parameters[param] = [ src ]
            else:
                if param in ranges.keys():
                    self.parameters[param] = ranges[param]
        self.build()
        # get glyphs
        names = gstring.split(' ')
        groups = self.project.libs['groups']['glyphs']
        glyph_names = parse_glyphs_groups(names, groups)
        # batch copy
        print "batch transferring glyphs in %s..." % self.project.name
        for src_path in self.ufos():
            font = hFont(RFont(src_path, showUI=False))
            dest_parameters = font.parameters
            dest_parameters[axis] = dest
            dest_file = '%s_%s.ufo' % (font.project.name, font.name_from_parameters(separator='-'))
            dest_path = os.path.join(font.project.paths['ufos'], dest_file)
            if os.path.exists(dest_path):
                dest_font = RFont(dest_path, showUI=False)
                print
                print "\tcopying glyphs from %s to %s..." % (get_full_name(font.ufo), get_full_name(dest_font))
                print '\t\t',
                for glyph_name in glyph_names:
                    if font.ufo.has_key(glyph_name):
                        if dest_font.has_key(glyph_name) is False:
                            dest_font.newGlyph(glyph_name)
                        # decompose first
                        if len(font.ufo[glyph_name].components) > 0:
                            font.ufo[glyph_name].decompose()
                        print glyph_name,
                        # insert glyph
                        dest_font.insertGlyph(font.ufo[glyph_name])
                        dest_font.save()
                print
        print '\n...done.\n'

    def copy_glyphs(self, src_glyphs, dst_glyphs, parameters=None):
        # build space
        if parameters is not None:
            self.parameters = parameters
        self.build()
        # get glyphs
        groups = self.project.libs['groups']['glyphs']
        src_glyph_names = parse_glyphs_groups(src_glyphs.split(' '), groups)
        dst_glyph_names = parse_glyphs_groups(dst_glyphs.split(' '), groups)
        # batch copy glyphs
        print "batch copying glyphs in %s...\n" % self.project.name
        for font_path in self.ufos():
            font = hFont(RFont(font_path, showUI=False))
            print '\tcopying glyphs in font %s' % font.full_name()
            for i in range(len(src_glyph_names)):
                _src_glyph_name = src_glyph_names[i]
                _dst_glyph_name = dst_glyph_names[i]
                # copy glyph
                if font.ufo.has_key(_src_glyph_name):
                    print '\t\tcopying %s to %s...' % (_src_glyph_name, _dst_glyph_name)
                    if not font.ufo.has_key(_dst_glyph_name):
                        font.ufo.newGlyph(_dst_glyph_name)
                    font.ufo.insertGlyph(font.ufo[_src_glyph_name], name=_dst_glyph_name)
                    font.ufo.save()
            # print '\t...done.'
            print
        # done
        print '...done.\n'
