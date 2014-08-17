# hProject doctests

# import

from hTools2.objects import hProject

# object

class hProject_test(object):

    """An interactive tests session for the :py:class:`hProject` object.

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> print p, p.name
    <hProject Publica> Publica

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> print p.world
    <hWorld>

    >>> print len(p.world.projects())
    16

    >>> print p.world.settings
    <hSettings>

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> print p.libs.keys()
    ['info', 'composed', 'accents', 'spacing', 'project', 'groups', 'interpol', 'vmetrics']

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> print p.paths.keys()
    ['features', 'temp', 'python_robofont', 'python', 'woffs', 'encoding', 'otfs', 'instances', 'otfs_test', 'interpol', 'libs', 'ufos', 'root', 'vfbs', 'python_nodebox']

    >>> print p.paths['ufos']
    /_fonts/_Publica/_ufos

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> print p.lib_paths.keys()
    ['info', 'composed', 'accents', 'spacing', 'project', 'groups', 'interpol', 'vmetrics']

    >>> print p.lib_paths['interpol']
    /_fonts/_Publica/_libs/interpol.plist
    

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> fonts = p.fonts.keys()
    >>> fonts.sort()
    >>> for font in fonts: print font, p.fonts[font]
    11 /_fonts/_Publica/_ufos/Publica_11.ufo
    15 /_fonts/_Publica/_ufos/Publica_15.ufo
    25 /_fonts/_Publica/_ufos/_instances/Publica_25.ufo
    35 /_fonts/_Publica/_ufos/_instances/Publica_35.ufo
    45 /_fonts/_Publica/_ufos/_instances/Publica_45.ufo
    55 /_fonts/_Publica/_ufos/Publica_55.ufo
    65 /_fonts/_Publica/_ufos/_instances/Publica_65.ufo
    75 /_fonts/_Publica/_ufos/_instances/Publica_75.ufo
    85 /_fonts/_Publica/_ufos/_instances/Publica_85.ufo
    91 /_fonts/_Publica/_ufos/Publica_91.ufo
    95 /_fonts/_Publica/_ufos/Publica_95.ufo

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> p.import_encoding()
    >>> print p.libs['groups']['glyphs'].keys()
    ['small_caps_extra', 'punctuation', 'uppercase_greek', 'small_caps_basic', 'smallcaps_accents_greek', 'uppercase_accents_cyrillic', 'symbols', 'quotes', 'mathematical_symbols', 'spaces', 'uppercase_extra', 'lowercase_accents_special', 'lowercase_basic', 'punctuation_caps', 'lowercase_cyrillic', 'uppercase_cyrillic_extra', 'uppercase_accents_greek', 'figures_lnum_pnum', 'accents_greek_lowercase', 'lowercase_greek', 'parenthetical_small_caps', 'accents_small_caps', 'small_caps_cyrillic', 'lowercase_alternates', 'punctuation_small_caps', 'dashes', 'lowercase_alternates_accents', 'slashes', 'accents_lowercase', 'dashes_caps', 'uppercase_cyrillic', 'figures_small_caps', 'lowercase_greek_accents', 'slashes_small_caps', 'small_caps_greek', 'accents_uppercase', 'invisible', 'currency', 'lowercase_accents', 'smallcaps_accents_cyrillic', 'lowercase_cyrillic_accents', 'small_caps_accents', 'parenthetical_caps', 'lowercase_extra', 'quotes_small_caps', 'figures_onum_pnum', 'lowercase_extra_exceptions', 'accents_greek_uppercase', 'uppercase_basic', 'parenthetical', 'figures_lnum_tnum', 'uppercase_accents', 'symbols_small_caps']
    >>> print p.libs['groups']['order']
    ['invisible', 'lowercase_basic', 'lowercase_extra', 'lowercase_extra_exceptions', 'lowercase_alternates', 'lowercase_greek', 'lowercase_cyrillic', 'figures_onum_pnum', 'figures_lnum_pnum', 'figures_lnum_tnum', 'uppercase_basic', 'uppercase_extra', 'uppercase_greek', 'uppercase_cyrillic', 'uppercase_cyrillic_extra', 'parenthetical_caps', 'dashes_caps', 'punctuation_caps', 'small_caps_basic', 'small_caps_extra', 'small_caps_greek', 'small_caps_cyrillic', 'figures_small_caps', 'symbols_small_caps', 'parenthetical_small_caps', 'slashes_small_caps', 'punctuation_small_caps', 'quotes_small_caps', 'spaces', 'punctuation', 'mathematical_symbols', 'quotes', 'dashes', 'slashes', 'parenthetical', 'symbols', 'currency', 'accents_lowercase', 'lowercase_accents', 'lowercase_accents_special', 'lowercase_alternates_accents', 'accents_greek_lowercase', 'lowercase_greek_accents', 'lowercase_cyrillic_accents', 'accents_uppercase', 'uppercase_accents', 'accents_greek_uppercase', 'uppercase_accents_greek', 'uppercase_accents_cyrillic', 'accents_small_caps', 'small_caps_accents', 'smallcaps_accents_greek', 'smallcaps_accents_cyrillic']

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> p.write_lib('interpol')
    saving interpol lib to file /_fonts/_Publica/_libs/interpol.plist... done.

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> p.make_folders()
    creating folders and files in Publica...
        /_fonts/_Publica exists.
        /_fonts/_Publica/_libs exists.
        /_fonts/_Publica/_ufos exists.
        /_fonts/_Publica/_vfbs exists.
        /_fonts/_Publica/_otfs exists.
        /_fonts/_Publica/_woffs exists.
        /_fonts/_Publica/_temp exists.
        /_fonts/_Publica/_ufos/_instances exists.
        /_fonts/_Publica/_ufos/_interpol exists.
        /_fonts/_Publica/_py exists.
        /_fonts/_Publica/_py/RoboFont exists.
        /_fonts/_Publica/_py/NodeBox exists.
        creating folder /Library/Application Support/Adobe/Fonts/_Publica... aborted, no Adobe fonts folder available.
    ...done.

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> for master in p.masters(): print master
    /_fonts/_Publica/_ufos/Publica_11.ufo
    /_fonts/_Publica/_ufos/Publica_15.ufo
    /_fonts/_Publica/_ufos/Publica_55.ufo
    /_fonts/_Publica/_ufos/Publica_91.ufo
    /_fonts/_Publica/_ufos/Publica_95.ufo

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> for master in p.masters_interpol(): print master
    /_fonts/_Publica/_ufos/_interpol/Publica_Black-Compressed.ufo
    /_fonts/_Publica/_ufos/_interpol/Publica_Black.ufo
    /_fonts/_Publica/_ufos/_interpol/Publica_Compressed.ufo
    /_fonts/_Publica/_ufos/_interpol/Publica_Regular.ufo
    /_fonts/_Publica/_ufos/_interpol/Publica_UltraLight-Compressed.ufo
    /_fonts/_Publica/_ufos/_interpol/Publica_UltraLight.ufo

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> for instance in p.instances(): print instance
    /_fonts/_Publica/_ufos/_instances/Publica_25.ufo
    /_fonts/_Publica/_ufos/_instances/Publica_35.ufo
    /_fonts/_Publica/_ufos/_instances/Publica_45.ufo
    /_fonts/_Publica/_ufos/_instances/Publica_65.ufo
    /_fonts/_Publica/_ufos/_instances/Publica_75.ufo
    /_fonts/_Publica/_ufos/_instances/Publica_85.ufo

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> for otf in p.otfs(): print otf
    /fonts/_Publica/_otfs/Publica_15.otf
    /fonts/_Publica/_otfs/Publica_35.otf
    /fonts/_Publica/_otfs/Publica_55.otf
    /fonts/_Publica/_otfs/Publica_75.otf
    /fonts/_Publica/_otfs/Publica_95.otf

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> for woff in p.woffs(): print woff
    /fonts/_Publica/_woffs/Publica_15.woff
    /fonts/_Publica/_woffs/Publica_35.woff
    /fonts/_Publica/_woffs/Publica_55.woff
    /fonts/_Publica/_woffs/Publica_75.woff
    /fonts/_Publica/_woffs/Publica_95.woff

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> for vfb in p.vfbs(): print vfb
    /fonts/_Publica/_vfbs/Publica_15.vfb
    /fonts/_Publica/_vfbs/Publica_55.vfb
    /fonts/_Publica/_vfbs/Publica_95.vfb

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> p.generate_instance('55')

    """

# test

if __name__ == "__main__":
    import doctest
    doctest.testmod()
