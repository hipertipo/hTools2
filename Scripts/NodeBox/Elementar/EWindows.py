# EWindows

def BaselineGrid():
    y = .5
    delta = 6
    stroke(.8)
    strokewidth(1)
    while y < HEIGHT:
        line(0, y, WIDTH, y)
        y += delta

class EWindow:

    _titlebar = 18
    _alpha = .9
    _padding = 12
    
    def __init__(self, (x, y, w, h)):
        # store window position & height
        self.x = x
        self.y = y
        self.w = w
        self.h = h        
        # clear defaults
        stroke(None)
        # draw title bar
        fill(.8, self._alpha)
        rect(x, y, w, self._titlebar)
        # draw window
        fill(.9, self._alpha)
        rect(x, y+self._titlebar, w, h)

    def Button(self, (x, y, w, h), _text=None):        
        # draw button
        fill(.85, self._alpha)
        _x = x + self.x
        _y = y + self.y + self._titlebar
        rect(_x, _y, w, h)
        # draw text
        font('EB13212A')
        fontsize(13)
        fill(.5, self._alpha)
        text(_text, _x+self._padding, _y+(h/2)+4)

    def TextField(self, (x, y, w, h), _text=None):        
        # draw button
        fill(1, self._alpha)
        _x = x + self.x
        _y = y + self.y + self._titlebar
        rect(_x, _y, w, h)
        # draw text
        font('EB13113A')
        fontsize(13)
        fill(.5, self._alpha)
        text(_text, _x+self._padding, _y+(h/2)+4)


BaselineGrid()

w = EWindow((49, 105, 368, 268))
w.Button((w._padding, 9, 121, 24), _text='press me')
w.Button((w._padding, 42, 170, 24), _text='press me too')
w.TextField((w._padding, 120, 242, 24), _text='this is a text field')
