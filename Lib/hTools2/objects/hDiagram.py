# [h] hDiagram

class hDiagram:

    scale = 0.1
    gridsize = 125
    x = 40
    y = 180
    alpha = .5

    hmetrics = True
    grid = False

    flip_x = False
    flip_y = False
    flip_z = False

    shift_x = 0
    shift_y = 0
    shift_z = (0, 0)

    columns = True
    rows = True
    gridfit = True

    def __init__(self, space, context):
        self.space = space
        self.ctx = context
        self.ctx.colors = context.ximport('colors')
        self.axes = space.parameters_order

    def draw(self, text, text_mode):
        _fonts = self.space.ufos()
        if self.grid:
            draw_grid(self.ctx, size_=self.gridsize)
        if len(_fonts) > 0:
            # make color factors
            x_factor = 1.00 / len(self.space.parameters[self.axes[0]])
            y_factor = 1.00 / len(self.space.parameters[self.axes[1]])
            z_factor = 1.00 / len(self.space.parameters[self.axes[2]])
            # reverse
            if self.flip_x:
                self.space.parameters[self.axes[0]].reverse()
            if self.flip_y:
                self.space.parameters[self.axes[1]].reverse()
            if self.flip_z:
                self.space.parameters[self.axes[2]].reverse()
            # iterate
            _x = self.x
            for param_x in self.space.parameters[self.axes[0]]:
                _y = self.y
                for param_y in self.space.parameters[self.axes[1]]:
                    for param_z in self.space.parameters[self.axes[2]]:
                        font_params = {
                            self.axes[0] : param_x,
                            self.axes[1] : param_y,
                            self.axes[2] : param_z,
                        }
                        param_1 = self.space.parameters_order[0]
                        param_2 = self.space.parameters_order[1]
                        param_3 = self.space.parameters_order[2]
                        font_name = '%s_%s-%s-%s.ufo' % (self.space.project.name,
                                    font_params[param_1],
                                    font_params[param_2],
                                    font_params[param_3])
                        ufo_path = os.path.join(self.space.project.paths['ufos'], font_name)
                        if ufo_path in _fonts:
                            # print ufo_path
                            _color = self.ctx.fill(.3)
                            _color.a = self.alpha
                            L = hLine(RFont(ufo_path), self.ctx)
                            L.txt(text, mode=text_mode)
                            if self.gridfit:
                                pos = gridfit((_x, _y), self.gridsize)
                            else:
                                pos = (_x, _y)
                            L.draw(pos, color_=_color, scale_=self.scale)
                            line_width = L.width(scale_=self.scale)
                            line_height = L.height(scale_=self.scale)
                    if self.rows:
                        _y += line_height
                    _y += self.shift_y
                if self.columns:
                    _x += line_width
                _x += self.shift_x
