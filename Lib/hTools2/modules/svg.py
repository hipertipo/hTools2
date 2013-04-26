# [h] hTools.modules.svg

class svgImporter:

    svgSyntax = {
        'M' : 'moveTo',
        'm' : 'moveTo',
        'L' : 'lineTo',
        'l' : 'lineTo',
        'C' : 'curveTo',
        'c' : 'curveTo',
        'Q' : 'qCurveTo',
        'q' : 'qCurveTo',
        'Z' : 'closePath',
        'z' : 'closePath',
    }

    def __init__ (self, svgSource):
        self.svgCommands = []
        self.parse(svgSource)

    def parse(self, svgSource):
        # first pass: separate commands from coordenates
        _counter = 0
        _commandName = ""
        _commandNumbers = []
        for x in svgSource.split():
            if x in self.svgSyntax.keys():
                if _counter == 0:
                    _commandName = str(x)
                else:
                    self.svgCommands.append((_commandName, _commandNumbers ))
                    _commandName = str(x)
                    _commandNumbers = []
            else:
                _commandNumbers.append(float(x))
            _counter = _counter + 1
        # second pass: make point tuples
        self._svg = []
        for command in self.svgCommands:
            commandName = command[0]
            points = []
            point = []
            counter = 0
            for nmbr in command[1]:
                point.append(nmbr)
                counter = counter + 1
                if counter == 2:
                    points.append( ( point[0], -point[1] ) )
                    counter = 0
                    point = [ ]
            self._svg.append(( commandName, points ))

