# [h] hFont

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hproject
    reload(hproject)

    import hTools2.modules.encoding
    reload(hTools2.modules.encoding)

    import hTools2.modules.fontinfo
    reload(hTools2.modules.fontinfo)

    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

    import hTools2.modules.ftp
    reload(hTools2.modules.ftp)

# imports

import os

from hproject import hProject
from hTools2.modules.encoding import paint_groups, auto_unicodes
from hTools2.modules.fontutils import set_font_names
from hTools2.modules.fontinfo import set_names_from_path
from hTools2.modules.ftp import *

# objects

class hFont:

    '''An object to represent a .ufo font source, wrapped in a few useful functions.'''

    # attributes

    project = None
    ufo = None
    file_name = None
    style_name = None

    # methods

    def __init__(self, ufo):
        self.ufo = ufo
        self.init_from_filename()

    def init_from_filename(self):
        '''Initiate `hFont` object from ufo, get parent project, parse name parts.'''
        ufo_file = os.path.basename(self.ufo.path)
        self.file_name = os.path.splitext(ufo_file)[0]
        try:
            family_name, style_name = self.file_name.split('_')
        except ValueError:
            family_name, style_name = self.file_name.split('-')
        self.project = hProject(family_name)
        self.style_name = style_name
        # set font names
        set_font_names(self.ufo, family_name, style_name)
        # import parameters
        try:
            name_parameters = self.style_name.split('-')
            parameters_order = self.project.libs['project']['parameters_order']
            self.parameters = dict(zip(parameters_order, name_parameters))
        except:
            self.parameters = {}
            # print 'there is no parameters lib for this font.\n'

    def auto_unicodes(self):
        '''Automatically set unicodes for all glyphs in the font.'''
        auto_unicodes(self.ufo)

    # groups and glyphs

    def order_glyphs(self):
        '''Automatically set the order of the glyphs in the font.'''
        _glyph_order = []
        for group in self.project.libs['groups']['order']:
            for glyph in self.project.libs['groups']['glyphs'][group]:
                _glyph_order.append(glyph)
        # update font
        self.ufo.glyphOrder = _glyph_order
        self.ufo.update()

    def paint_groups(self, crop=False):
        '''Paint and order the glyphs in the font according to their group.'''
        paint_groups(self.ufo, crop)

    def import_spacing_groups(self, mode=0):
        _spacing_dict = self.project.libs['spacing']
        # old hTools1 format
        if mode == 1:
            for side in _spacing_dict.keys():
                for group in _spacing_dict[side].keys():
                    _class_name = '_%s_%s' % (side, group)
                    _glyphs = [ group ] + _spacing_dict[side][group]
                    self.ufo.groups[_class_name] = _glyphs
        # new hTools2 format
        else:
            for side in _spacing_dict.keys():
                for group in _spacing_dict[side].keys():
                    self.ufo.groups[group] = _spacing_dict[side][group]
        # update font
        self.ufo.update()

    def paint_spacing_groups(self, side, verbose=False):
        # collect groups & glyphs to paint
        _groups_dict = get_spacing_groups(self.ufo)
        if side == 'left':
            _groups = _groups_dict['left']
        else:
            _groups = _groups_dict['right']
        # paint
        if len(_groups) > 0:
            if verbose:
                print 'painting spacing groups...'
            print
            _group_names = _groups.keys()
            clear_colors(self.ufo)
            color_step = 1.0 / len(_group_names)
            count = 0
            for group in _group_names:
                if verbose:
                    print '\tpainting group %s...' % group
                color = color_step * count
                R, G, B = hls_to_rgb(color, 0.5, 1.0)
                for glyph_name in _groups[group]:
                    if self.ufo.has_key(glyph_name):
                        self.ufo[glyph_name].mark = (R, G, B, .5)
                        self.ufo[glyph_name].update()
                    else:
                        if verbose:
                            print '%s not in font' % glyph_name
                count += 1
            self.ufo.update()
            if verbose:
                print
                print '...done.\n'
        else:
            if verbose:
                print 'there are no spacing groups to paint.\n'

    def import_groups_from_encoding(self):
        '''Import glyph names and order from encoding file, and stores them in a lib.'''
        self.project.import_encoding()
        self.ufo.groups.clear()
        for group in self.project.libs['groups']['glyphs'].keys():
            self.ufo.groups[group] = self.project.libs['groups']['glyphs'][group]
        self.ufo.lib['groups_order'] = self.project.libs['groups']['order']

    def build_accents(self):
        # if self.project.libs['accents'].has_key(glyph_name):
        #     base_glyph, accents = self.project.libs['accents'][glyph_name]
        #     font.ufo.removeGlyph(glyph_name)
        #     font.ufo.compileGlyph(glyph_name, base_glyph, accents)
        #     font.ufo[glyph_name].update()
        # else:
        #     print 'project has not accents lib.\n'
        pass

    # OpenType features

    def import_features(self):
        '''Import features from features file into font.'''
        import_features(self.ufo, self.project.paths['features'])

    def export_features(self):
        '''Export features from font to features file.'''
        export_features(self.ufo, self.project.paths['features'])

    # font names

    def full_name(self):
        '''Return the full name of the font, made of the `hProject.name` and `font.style_name`.'''
        return '%s %s' % (self.project.name, self.style_name)

    def set_names(self):
        '''Set font names from the ufo file name.'''
        set_names_from_path(self.ufo)

    def name_from_parameters(self, separator=''):
        '''Set font names from parameters lib.'''
        name = ''
        parameters = self.project.libs['project']['parameters_order']
        count = 0
        for parameter in parameters:
            name += str(self.parameters[parameter])
            if count < (len(parameters) - 1):
                name += separator
            count += 1
        return name

    # font info

    def set_info(self):
        '''Set different kinds of font info.'''
        set_names_from_path(self.ufo)
        # foundry info
        # version info

    def print_info(self):
        '''Print different kinds of font information.'''
        pass

    def set_vmetrics(self, verbose=True):
        if verbose: print 'setting vertical metrics...'
        # set_vmetrics(font, xheight, capheight, ascender, descender, emsquare, gridsize=1)

    def clear_info(self):
        '''Print different kinds of font information.'''
        clear_font_info(self.ufo)

    # font paths

    def otf_path(self, test=False):
        '''Return the default path for .otf fonts, in the project's `_otfs/` folder.'''
        otf_file = self.file_name + '.otf'
        if test is True:
            otf_path = os.path.join(self.project.paths['otfs_test'], otf_file)
        else:
            otf_path = os.path.join(self.project.paths['otfs'], otf_file)
        return otf_path

    def woff_path(self):
        '''Return the default path for .woff fonts, in the project's `_woffs/` folder.'''
        woff_file = self.file_name + '.woff'
        woff_path = os.path.join(self.project.paths['woffs'], woff_file)
        return woff_path

    # font generation

    def generate_otf(self, options=None, verbose=False):
        '''Generate an otf font file using the default settings.'''
        # get options
        if options is None:
            options = {
                'decompose' : True,
                'remove overlap' : True,
                'autohint' : False,
                'release mode' : False,
                'test folder' : False
            }
        # get otf path
        if options['test folder'] == True:
            _otf_path = self.otf_path(test=True)
        else:
            _otf_path = self.otf_path()
        # print info
        if verbose:
            print 'generating .otf for %s...\n' % self.full_name()
            print '\tdecompose: %s' % options['decompose']
            print '\tremove overlap: %s' % options['remove overlap']
            print '\tautohint: %s' % options['autohint']
            print '\trelease mode: %s' % options['release mode']
            print '\tfont path: %s' % _otf_path
            print
        # generate
        self.ufo.generate(_otf_path, 'otf',
                    decompose=options['decompose'],
                    autohint=options['autohint'],
                    checkOutlines=options['remove overlap'],
                    releaseMode=options['release mode'])
        # check if sucessfull
        if verbose:
            print '\tgeneration succesfull? %s' % ['No', 'Yes'][os.path.exists(_otf_path)]
            print
            print '...done.\n'

    def generate_woff(self):
        '''Generate a woff font file from the available otf font'''
        # this function currently relies on the `KLTF_WOFF.py` extra module
        try:
            from hTools2.extras.KLTF_WOFF import compressFont
            compressFont(self.otf_path(), self.woff_path())
        except:
            print 'KLTF WOFF generation plugin not available.\n '

    def upload_woff(self):
        '''Upload the font's woff file to the project's folder in the FTP server.'''
        _url = self.project.world.settings.hDict['ftp']['url']
        _login = self.project.world.settings.hDict['ftp']['login']
        _password = self.project.world.settings.hDict['ftp']['password']
        _folder = self.project.ftp_path()
        F = connect_to_server(_url, _login, _password, _folder, verbose=False)
        upload_file(self.woff_path(), F)
        F.quit()

