# Workflow in RoboFlight

The RoboFlight class is the framework that binds all FontBureau conversion, QA and production functions into one overall application class and interface.

## Schedule and status of fonts and families

- graphs showing percentage of each task completed
- [Gantt chart](https://en.wikipedia.org/wiki/Gantt_chart) – start and end of each task, dependencies, milestones

## Importing from existing FontLab, UFO, TTF

- Combining distributed data (version, TTF tables)
- Saving as UFO
- Creating missing info/tables that can be automated
- Vertical metrics

### ttf2ufo

### otf2ufo

### vfb2ufo

- FL TTF instructions
- FL spacing classes (key glyphs marked with ')
- FL guidelines
- FL OpenType features
- FL multiple masters

## Versioning through SVN

- Show overview on SVN version and status of fonts and glyphs

## GlyphAnalyser

- automatic generation of statistics on measurement, meta information, font info

- apply to all glyphs, or only to a few key glyphs?
- use measurements for PANOSE data

## FontAnalyser

- Statistics on measurements
- Statistic on spacing and kerning
- Kerning fingerprint image (as Erik had in the old days)

## Spacing and Kerning

- Interfacing to FontMetrics and RoboFont

## Create Remove-overlap layer

...

## Maintenance of layers with custom versions of glyphs

## OpenType features

- building (semi-)automatic alternates and ligatures
- build simple substitutions

## Accent building, build anchors

- build from accents lib

## Interpolation

- Prepolation

- Interfacing to Superpolator and RoboFont

Standard folder and naming for Superpolator files ('instances' folder), process with other fonts.

## Hinting TT/PS

- automatic generation of CVT table
- (Partial) autohinting
- using RoboHint to write hint code optimized for various output devices

## QA

### Generating specimens/proof pages

- character set / glyph groups
- OpenType features
- spacing and kerning
- variations: series, superposition
- languages
- tabular data, currency symbols
- different kinds of text
- numbers within text blocks
- small caps with numbers, punctuation

- which tools/libraries to use? NodeBox / DrawBot / CoreGraphics / InDesign?

### checking various output devices

- auto-generate specimen page (html/js/css)
- upload webfonts to FTP server

### status of versions, todo, authorization

- data entries in `project lib`
- README file
- TODO file
- VERSION + RELEASE_NOTES file

## Generating WOFF/OTF/Type1

- how to generate woffs? (I have been using a custom library by KL)

- Subsetting fonts (how to deal with the features)

- Obfuscating fonts for Webtype

- Automatic custom width/weight adjustment

- Generating DSIG table?

- - -

## Documentation about this application

## Documentation about the workflow
