# [h] hFont

# import

import os

from hTools2.objects.hproject import hProject

from hTools2.modules.anchors import clear_anchors, get_anchors_dict
from hTools2.modules.color import clear_colors, hls_to_rgb, x11_colors, convert_to_1, random_color
from hTools2.modules.encoding import paint_groups, auto_unicodes, crop_glyphset
from hTools2.modules.fontinfo import set_names_from_path, set_vmetrics, get_stems, set_stems
from hTools2.modules.fontutils import *
from hTools2.modules.ftp import *
from hTools2.modules.languages import diacritics_glyphnames
from hTools2.modules.opentype import import_features, export_features, clear_features, import_kern_feature
from hTools2.modules.messages import no_glyph_selected
from hTools2.modules.ttx import *

# objects

class hFont:

    '''An object to represent a ``.ufo`` font source, wrapped in a few useful functions.'''

    # attributes

    #: The parent ``hProject`` object to which the font belongs.
    project = None

    #: The ``.ufo`` file containing the actual font.
    ufo = None

    #: The name of the ``.ufo`` file, without the extension.
    file_name = None

    #: The ``styleName`` of the font, parsed from the name of the ``.ufo`` file on initialization. See ``init_from_filename()``.
    style_name = None

    #: A dictionary with the parameters which identify this particular font in the family's variation space.
    parameters = {}

    #: A dictionary to contain this font's guidelines, once the basic vertical metrics have been defined and set.
    guides_dict = {}

    # methods

    def __init__(self, ufo):
        '''Initiate the ``hFont`` object from a ``.ufo`` file.'''
        self.ufo = ufo
        self.init_from_filename()

    def __repr__(self):
        '''Return textual representation of ``hFont``.'''
        return '<hFont %s>' % self.full_name()

    def init_from_filename(self, set_names=True, verbose=False):
        '''Initiate ``hFont`` object from ``RFont``, get parent project, parse name parts.'''
        ufo_file = os.path.basename(self.ufo.path)
        self.file_name = os.path.splitext(ufo_file)[0]
        try:
            # break file name into family- and style name
            family_name, self.style_name = self.file_name.split('_')
            # get parent project
            self.project = hProject(family_name)
            # set font names
            if set_names:
                set_font_names(self.ufo, family_name, self.style_name)
            # get parameters from name and store them into a dict
            try:
                name_parameters = self.style_name.split('-')
                parameters_order = self.project.libs['project']['parameters_order']
                self.parameters = dict(zip(parameters_order, name_parameters))
            # keep parameters dict empty
            except:
                if verbose:
                    print 'Error: no parameters lib for this font.\n'
        except:
            print 'Error: font name is not in the format family_style'

    # groups and glyphs

    def create_glyphs(self):
        '''Create all glyphs from the project's encoding file.'''
        glyph_set = self.glyphset()
        for glyph_name in glyph_set:
            if self.ufo.has_key(glyph_name) is not True:
                self.ufo.newGlyph(glyph_name)
        self.ufo.save()

    def get_glyph_names(self, gstring):
        if gstring is not None:
            glyph_names = self.project.parse_gstring(gstring)
        else:
            glyph_names = self.project.all_glyphs()
        return glyph_names

    def glyphset(self):
        '''Return a list with all glyph names in the font's glyphset.'''
        _glyph_order = []
        for group in self.project.libs['groups']['order']:
            for glyph in self.project.libs['groups']['glyphs'][group]:
                _glyph_order.append(glyph)
        return _glyph_order

    def auto_unicodes(self):
        '''Automatically set unicodes for all glyphs in the font.'''
        auto_unicodes(self.ufo)

    def clear_groups(self):
        '''Delete all groups in the font.'''
        delete_groups(self.ufo)

    def order_glyphs(self):
        '''Automatically set the order of the glyphs in the font based on the project's ``groups`` lib.'''
        glyph_order = self.glyphset()
        self.ufo.glyphOrder = glyph_order
        self.ufo.update()

    def paint_groups(self, crop=False):
        '''Paints and orders the glyphs in the font based on the project's ``groups`` lib.

        :param bool crop: If ``True``, remove from the font all glyphs which don't belong to any group.

        '''
        paint_groups(self.ufo, crop)

    def import_spacing_groups(self, mode=0):
        '''Import left/right spacing classes from lib into groups.'''
        _spacing_dict = self.project.libs['spacing']
        for side in _spacing_dict.keys():
            for group in _spacing_dict[side].keys():
                self.ufo.groups[group] = _spacing_dict[side][group]
        self.ufo.update()

    def paint_spacing_groups(self, side, verbose=False):
        '''Paint left or right spacing groups.'''
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
                            print '\t\t%s not in font' % glyph_name
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

    def crop_glyphset(self):
        '''Delete all glyphs which are not in the font's glyphset.'''
        glyph_set = self.glyphset()
        crop_glyphset(self.ufo, glyph_set)

    def get_glyphs(self):
        return get_glyphs(self.ufo)

    # actions

    def apply_actions(self, actions_dict):
        # if actions_dict['remove overlap']:
        #     self.remove_overlap()
        # if actions_dict['decompose']:
        #     self.decompose()
        # if actions_dict['auto contour order']:
        #     self.auto_contour_order()
        # if actions_dict['auto contour direction']:
        #     self.auto_contour_direction()
        # if actions_dict['add extremes']:
        #     self.add_extremes()
        # if actions_dict['remove overlaps']:
        #     self.remove_overlap()
        pass

    def remove_overlap(self):
        '''Remove overlaps for all glyphs in font.'''
        remove_overlap(self.ufo)

    def decompose(self):
        '''Decompose all glyphs in font.'''
        decompose(self.ufo)

    def auto_contour_order(self):
        '''Auto set contour order in all glyphs in font.'''
        auto_contour_order(self.ufo)

    def auto_contour_direction(self):
        '''Auto set contour direction in all glyphs in font.'''
        auto_contour_direction(self.ufo)

    def auto_order_direction(self):
        '''Auto set contour order and direction in all glyphs in font.'''
        auto_order_direction(self.ufo)

    def add_extremes(self):
        '''Auto add extreme points to all glyphs in font.'''
        add_extremes(self.ufo)

    def align_to_grid(self, (sizeX, sizeY)):
        '''Align points in all glyphs in font to the given ``(x,y)`` grid.'''
        align_to_grid(self.ufo, (sizeX, sizeY))

    def scale_glyphs(self, (factor_x, factor_y)):
        '''Scale all glyphs in font by the given factor ``(x,y)``.'''
        scale_glyphs(self.ufo, (factor_x, factor_y))

    def move_glyphs(self, (delta_x, delta_y)):
        '''Move all glyphs in font by the given distance ``(x,y)``.'''
        move_glyphs(self.ufo, (delta_x, delta_y))

    def round_to_grid(self, gridsize, gstring=None):
        '''Round points in all given glyphs in the font to the given ``gridsize``.'''
        glyph_names = self.get_glyph_names(gstring)
        round_to_grid(self.ufo, gridsize, glyph_names)

    def delete_layers(self):
        '''Delete all layers in the font.'''
        while len(self.ufo.layerOrder) > 0:
            self.ufo.removeLayer(self.ufo.layerOrder[0])
            self.ufo.update()

    # building glyphs

    def clear_anchors(self, gstring=None):
        '''Delete all anchors in the font.'''
        glyph_names = self.get_glyph_names(gstring)
        clear_anchors(self.ufo, glyph_names=glyph_names)

    def build_glyph(self, glyph_name, composed=False, verbose=True):
        '''Build glyph with the given ``glyph_name`` from components based on the project's ``accents`` or ``composed`` libs.'''
        # accents
        if self.project.libs['accents'].has_key(glyph_name):
            base_glyph, accents = self.project.libs['accents'][glyph_name]
            self.ufo.removeGlyph(glyph_name)
            self.ufo.compileGlyph(glyph_name, base_glyph, accents)
            self.ufo[glyph_name].update()
            return True
        # composed
        elif self.project.libs['composed'].has_key(glyph_name):
            self.ufo.newGlyph(glyph_name, clear=True)
            components = self.project.libs['composed'][glyph_name]
            offset_x, offset_y = 0, 0
            scale_x, scale_y = 1, 1
            for component in components:
                self.ufo[glyph_name].appendComponent(component, (offset_x, offset_y), (scale_x, scale_y))
                offset_x += self.ufo[component].width
            self.ufo[glyph_name].update()
            return True
        # not composed
        else:
            if verbose: print '%s is not composed.' % glyph_name
            return False

    # def build_accents_old(self, gstring=None, ignore=[]):
    #     '''Build all accented glyphs in the font based on the project's ``accents`` libs.'''
    #     glyph_names = self.get_glyph_names(gstring)
    #     # build glyphs
    #     for glyph_name in glyph_names:
    #         if self.ufo.has_key(glyph_name):
    #             # skip glyphs in ignore list
    #             if glyph_name not in ignore:
    #                 self.build_glyph(glyph_name, composed=False, verbose=False)

    def build_accents(self):
        '''Build accented glyphs for all supported languages.'''
        lang_file = self.project.paths['languages']
        languages = [ lang.strip() for lang in open(lang_file).readlines() ]
        for lang in languages:
            if diacritics_glyphnames.has_key(lang):
                lc, uc = diacritics_glyphnames[lang]
                lang_glyphs = lc + uc
                for glyph_name in sorted(lang_glyphs):
                    if self.project.libs['accents'].has_key(glyph_name):
                        base_glyph, accents = self.project.libs['accents'][glyph_name]
                        # self.ufo.removeGlyph(glyph_name)
                        self.ufo.compileGlyph(glyph_name, base_glyph, accents)
                        self.ufo[glyph_name].update()

    # def build_composed(self):
    #     '''Build all composed glyphs in the font based on the project's ``composed`` libs.'''
    #     for glyph_name in self.project.libs['composed'].keys():
    #         if self.ufo.has_key(glyph_name):
    #             self.build_glyph(glyph_name)

    def build_anchors(self, clear=True):
        # get anchors
        anchors_lib = get_anchors_dict(self.project.libs['accents'])
        vmetrics_lib = self.get_vmetrics()
        groups_lib = self.project.libs['groups']['glyphs']
        # clear anchors
        if clear:
            self.clear_anchors()
        # create base anchors
        for glyph_name in anchors_lib.keys():
            if self.ufo.has_key(glyph_name):
                glyph = self.ufo[glyph_name]
                # get horizontal center
                try:
                    l, b, r, t = glyph.box
                    x_center = l + ((r - l) * 0.5)
                except TypeError:
                    x_center = glyph.width * 0.5
                # lc top base
                if 'top' in anchors_lib[glyph_name]:
                    y = vmetrics_lib['xheight'] + vmetrics_lib['xheight_anchors']
                    glyph.appendAnchor('top', (x_center, y))
                # lc bottom base
                if 'bottom' in anchors_lib[glyph_name]:
                    y = vmetrics_lib['baseline_lc_anchors']
                    glyph.appendAnchor('bottom', (x_center, y))
                # done glyph
                glyph.update()
        # create accents anchors
        for glyph_name in groups_lib['accents_lc']:
            if self.ufo.has_key(glyph_name):
                glyph = self.ufo[glyph_name]
                # get horizontal center
                try:
                    l, b, r, t = glyph.box
                    x_center = l + ((r - l) * 0.5)
                except TypeError:
                    x_center = glyph.width * 0.5
                y = vmetrics_lib['xheight'] + vmetrics_lib['xheight_anchors']
                glyph.appendAnchor('_top', (x_center, y))
        # done font
        self.ufo.update()

    def build_selected_glyphs(self):
        # get glyphs
        glyph_names = get_glyphs(self.ufo)
        # get color
        mark_color = random_color(alpha=.5)
        # build glyphs
        if len(glyph_names) > 0:
            for glyph_name in glyph_names:
                composed = self.build_glyph(glyph_name)
                # paint glyph
                if composed:
                    self.ufo[glyph_name].mark = mark_color
            self.ufo.update()
        else:
            print no_glyph_selected

    # OT features

    def clear_features(self):
        '''Delete all OpenType features and classes in font.'''
        clear_features(self.ufo)

    def import_features(self):
        '''Import features from features file into font.'''
        import_features(self.ufo, self.project.paths['features'])

    def import_kern_feature(self):
        '''Import `kern` feature from features file into font.'''
        # extend: make switch to get style-specific kerning
        kern_path = os.path.join(self.project.paths['libs'], 'kern.fea')
        import_kern_feature(self.ufo, kern_path)

    def export_features(self):
        '''Export features from font to features file.'''
        export_features(self.ufo, self.project.paths['features'])

    # font names

    def full_name(self):
        '''Return the full name of the font, made of the `hProject.name` and `font.style_name`.'''
        return '%s %s' % (self.project.name, self.style_name)

    def set_names(self):
        '''Set font names from the font's ``.ufo`` file name.'''
        set_names_from_path(self.ufo, prefix='HPTP')

    def name_from_parameters(self, separator=''):
        '''Set font names from the font's parameters lib.'''
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
        '''Set font names from the ``.ufo``'s path name.'''
        set_names_from_path(self.ufo)

    def set_foundry_info(self):
        '''Set foundry info from the project's ``info`` lib.'''
        fontinfo_lib = self.project.libs['info']
        # set info fields
        for k in fontinfo_lib.keys():
            v = fontinfo_lib[k]
            if k == 'copyright':
                self.ufo.info.copyright = v
            if k == 'trademark':
                self.ufo.info.trademark = v
            if k == 'note':
                self.ufo.info.note = v
            if k == 'licence':
                self.ufo.info.openTypeNameLicense = v
            if k == 'sample':
                self.ufo.info.openTypeNameSampleText = v
            if k == 'description':
                self.ufo.info.openTypeNameDescription = v
            if k == 'year':
                self.ufo.info.year = int(v)
            if k == 'designer':
                self.ufo.info.openTypeNameDesigner = v
            if k == 'designer_url':
                self.ufo.info.openTypeNameDesignerURL = v
            if k == 'manufacturer':
                self.ufo.info.openTypeNameManufacturer = v
            if k == 'manufacturer_url':
                self.ufo.info.openTypeNameManufacturerURL = v
        # done
        self.ufo.update()

    def print_info(self):
        '''Print different kinds of font information.'''
        pass

    def clear_info(self):
        '''Print different kinds of font information.'''
        clear_font_info(self.ufo)

    # vertical metrics

    def get_vmetrics(self):
        '''Build a ``vmetrics`` dict using data from the ``vmetrics`` lib.'''
        # build up vmetrics dict
        vmetrics_lib = self.project.libs['project']['vmetrics']
        vmetrics = {}
        # get default values
        if vmetrics_lib.has_key('default'):
            vmetrics = vmetrics_lib['default']
        # get style-specific values
        if vmetrics_lib.has_key(self.style_name):
            for k in vmetrics_lib[self.style_name].keys():
                vmetrics[k] = vmetrics_lib[self.style_name][k]
        # condensed: get values from normal
        else:
            for style in vmetrics_lib.keys():
                if style[0] == self.style_name[0]:
                    for k in vmetrics_lib[style].keys():
                        vmetrics[k] = vmetrics_lib[style][k]
        return vmetrics

    # def get_stems(self):
    #     # build up vmetrics dict
    #     stems_lib = self.project.libs['project']['stems']
    #     stems = []
    #     # get default values
    #     if stems_lib.has_key('default'):
    #         stems = stems_lib['default']
    #     # get style-specific values
    #     if stems_lib.has_key(self.style_name):
    #         stems = stems_lib[self.style_name]
    #     # condensed: get values from normal
    #     else:
    #         for style in stems_lib.keys():
    #             if style[0] == self.style_name[0]:
    #                 stems = stems_lib[style]
    #     return stems

    def set_stems(self, verbose=True):
        '''Set PS stems by measuring glyph data in the font.'''
        if verbose:
            print 'setting stems in %s...' % self.full_name(),
        stems = get_stems(self.ufo)
        set_stems(self.ufo, stems)
        # done
        if verbose:
            print 'done.'

    def set_vmetrics(self, verbose=True):
        '''Set the font's vertical metrics from the a ``vmetrics`` dict.'''
        if verbose:
            print 'setting vertical metrics in %s...' % self.full_name(),
        # set vmetrics
        vmetrics = self.get_vmetrics()
        set_vmetrics(self.ufo, vmetrics['xheight'], vmetrics['capheight'], vmetrics['ascender'], vmetrics['descender'], vmetrics['emsquare'])
        # done
        if verbose:
            print 'done.'

    def make_guides(self):
        '''Build a guides dictionary from the project's ``vmetrics`` lib.'''
        vmetrics = self.get_vmetrics()
        guides = vmetrics.keys()
        # separate guides into groups
        guides_names = {
            'anchors' : [ g for g in guides if 'anchors' in g.split('_') ],
            'overshoots' : [ g for g in guides if 'overshoot' in g.split('_') ],
            'lowercase' : [ g for g in guides if 'lc' in g.split('_') ],
            'numbers' : [ g for g in guides if g[:6] == 'number' ],
            'uppercase' : [ g for g in guides if 'uc' in g.split('_') ] + [ g for g in guides if 'capheight' in g.split('_') ],
        }
        # compile guides dict from offsets
        guides_dict = {}
        for k in guides_names.keys():
            guides_dict[k] = {}
            for guides_name in guides_names[k]:
                if k in [ 'anchors', 'overshoots'] :
                    pos = vmetrics[guides_name]
                    pos_ref = guides_name.split('_')[0]
                    pos += vmetrics[pos_ref]
                    guides_dict[k][guides_name] = pos
                else:
                    guides_dict[k][guides_name] = vmetrics[guides_name]
        self.guides_dict = guides_dict

    def draw_guides(self, case='lowercase', guides_group='overshoots', verbose=True):
        '''Create guidelines using data from the project's ``vmetrics`` lib.'''
        if verbose:
            print 'creating guidelines...',
        # clear current guides
        self.make_guides()
        clear_guides(self.ufo)
        # create the guides
        for guide_name, guide_pos in self.guides_dict[guides_group].items():
            if case == 'lowercase':
                if guide_name not in self.guides_dict['uppercase'].keys() and guide_name not in self.guides_dict['numbers'].keys():
                    self.ufo.addGuide((0, guide_pos), 0, name=guide_name)
            elif case == 'numbers':
                if guide_name in self.guides_dict['numbers'].keys():
                    self.ufo.addGuide((0, guide_pos), 0, name=guide_name)
            else:
                if guide_name in self.guides_dict['uppercase'].keys():
                    self.ufo.addGuide((0, guide_pos), 0, name=guide_name)
        # special guides
        if case == 'numbers':
            self.ufo.addGuide((0, self.guides_dict['numbers']['numberdesc']), 0, name='numbers_descenders')
            self.ufo.addGuide((0, self.guides_dict['overshoots']['xheight_overshoot']), 0, name='xheight_overshoot')
            self.ufo.addGuide((0, self.guides_dict['overshoots']['baseline_lc_overshoot']), 0, name='baseline_overshoot')
        # done
        self.ufo.update()
        if verbose:
            print 'done.\n'

    def clear_guides(self):
        '''Delete all global guides in the font.'''
        clear_guides(self.ufo)

    def set_bluezones(self):
        '''Set the PostScript blue zones from the font's vertical metrics and guidelines dict.'''
        self.make_guides()
        bluezones = []
        bluezones.append(self.guides_dict['overshoots']['descender_overshoot'])
        bluezones.append(self.ufo.info.descender)
        bluezones.append(self.guides_dict['overshoots']['baseline_lc_overshoot'])
        bluezones.append(0)
        bluezones.append(self.guides_dict['overshoots']['xheight_overshoot'])
        bluezones.append(self.ufo.info.xHeight)
        bluezones.append(self.guides_dict['overshoots']['capheight_overshoot'])
        bluezones.append(self.ufo.info.capHeight)
        bluezones.append(self.guides_dict['overshoots']['ascender_overshoot'])
        bluezones.append(self.ufo.info.ascender)
        bluezones.sort()
        self.ufo.info.postscriptBlueValues = bluezones
        self.ufo.update()

    def clear_bluezones(self):
        self.ufo.info.postscriptBlueValues =[]

    # font paths

    def otf_path(self, test=False, folder=None):
        '''Return the default path for ``.otf`` font generation, in the project's ``_otfs/`` folder.'''
        otf_file = self.file_name + '.otf'
        if test is True:
            otf_path = os.path.join(self.project.paths['otfs_test'], otf_file)
        else:
            if not folder:
                otf_path = os.path.join(self.project.paths['otfs'], otf_file)
            else:
                otf_path = os.path.join(folder, otf_file)
        return otf_path

    def woff_path(self):
        '''Return the default path for ``.woff`` font generation, in the project's ``_woffs/`` folder.'''
        woff_file = self.file_name + '.woff'
        woff_path = os.path.join(self.project.paths['woffs'], woff_file)
        return woff_path

    def ttx_path(self):
        '''Return the default path for ``.ttx`` generation, in the project's ``_ttx/`` folder.'''
        ttx_file = self.file_name + '.ttx'
        ttx_path = os.path.join(self.project.paths['ttx'], ttx_file)
        return ttx_path

    # font generation

    def generate_otf(self, options=None, verbose=False, folder=None):
        '''Generate an ``.otf`` for the font using the given ``options``.'''
        # get options
        if options is None:
            try:
                options = self.project.libs['project']['generation']
            except KeyError:
                if verbose: print 'project %s has no generation lib.' % self.project.name
                options = {
                    'decompose' : True,
                    'autohint' : False,
                    'remove overlap' : True,
                    'release mode' : False,
                    'test folder' : False,
                }
        # get otf path
        if folder is None:
            _test = options['test folder']
            _otf_path = self.otf_path(test=_test)
        else:
            _otf_path = self.otf_path(folder=folder)
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
        self.ufo.generate(
                    _otf_path, 'otf',
                    decompose=options['decompose'],
                    autohint=options['autohint'],
                    checkOutlines=options['remove overlap'],
                    releaseMode=options['release mode'])
        # check if sucessfull
        if verbose:
            print '\tgeneration succesfull? %s' % ['No', 'Yes'][os.path.exists(_otf_path)]
            print
            print '...done.\n'

    def generate_woff(self, strip=False):
        '''Generate a ``.woff`` font file from the available ``.otf`` font.'''
        try:
            from hTools2_plus.extras.KLTF_WOFF import compressFont
            if strip:
                # save to ttx
                self.generate_ttx()    
                # strip names from ttx
                ttx_path = self.ttx_path()
                strip_names(ttx_path)
                # generate otf
                otf_path = os.path.join(self.project.paths['woffs'], os.path.split(ttx_path)[1]+'.otf')
                ttx2otf(ttx_path, otf_path)
                # generate woff
                compressFont(otf_path, self.woff_path())
                os.remove(otf_path)
            else:
                compressFont(self.otf_path(), self.woff_path())
        except:
            print 'KLTF WOFF module could not be imported.\n '

    def generate_ttx(self):
        '''Generate a ``.ttx`` file from the available ``.otf`` font.'''
        otf_path = self.otf_path()
        ttx_path = self.ttx_path()
        if not os.path.exists(otf_path):
            self.generate_otf()
        tt = TTFont(otf_path)
        tt.saveXML(ttx_path)

    def upload_woff(self):
        '''Upload the font's ``.woff`` file to the project's folder in the FTP server.'''
        woff_path = self.woff_path()
        if os.path.exists(woff_path):
            url = self.project.world.settings.hDict['ftp']['url']
            login = self.project.world.settings.hDict['ftp']['login']
            password = self.project.world.settings.hDict['ftp']['password']
            folder = self.project.ftp_path()
            F = connect_to_server(url, login, password, folder, verbose=False)
            upload_file(woff_path, F)
            F.quit()
        else:
            print 'woff %s does not exist.' % woff_path

