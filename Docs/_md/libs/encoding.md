## encoding

Encoding files are simple text files with an `.enc` extension. They are the default way of specifying character sets in each project, and are used to order glyphs and paint groups in the fonts.

Below is small sample encoding file. The first line is the title, usually the name of the project (this line is skipped when parsing). Lines starting with `% ` followed by a series of hyphens indicate group names, and the following lines correspond to the glyphs contained in this group.

    %% [h] Publica
    % --------------- group_name
    glyph_name
    % --------------- latin_lc_basic
    a
    b
    c
    d
    …
    %
