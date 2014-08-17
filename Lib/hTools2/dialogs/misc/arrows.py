# [h] arrows ui

# imports

from vanilla import *

# objects

class Arrows(Group):

    """An object to add directional arrow buttons to vanilla dialogs."""

    # attributes

    all_arrows = [
        'top', 'down', 'left', 'right',
        'leftUp', 'leftDown', 'rightUp', 'rightDown',
    ]

    # methods

    def __init__(self, (l, t), s=35, p=10, callbacks=dict(), arrows=None):

        w = (s * 3) - 2
        h = w

        super(Arrows, self).__init__((0, 0, w+(p*2), h+(p*2)))

        small = s - 9

        # draw UI

        x0 = p
        x1 = x0 + s - 1
        x2 = x1 + s - 1

        y0 = p
        y1 = y0 + s - 1
        y2 = y1 + s - 1

        if arrows is None:
            arrows = self.all_arrows

        for arrow in arrows:

            if arrow == 'left':
                self.left = SquareButton(
                    (x0, y1, s, s),
                    unichr(8672),
                    callback=callbacks["left"])
                self.left.bind("left", [])

            if arrow == 'down':
                self.down = SquareButton(
                    (x1, y2, s, s),
                    unichr(8675),
                    callback=callbacks["down"])
                self.down.bind("down", [])

            if arrow == 'right':
                self.right = SquareButton(
                    (x2, y1, s, s),
                    unichr(8674),
                    callback=callbacks["right"])
                self.right.bind("right", [])

            if arrow == 'up':
                self.up = SquareButton(
                    (x1, y0, s, s),
                    unichr(8673),
                    callback=callbacks["up"])
                self.up.bind("up", [])

            if arrow == 'leftUp':
                self.left_up = SquareButton(
                    (x0, y0, small, small),
                    unichr(8598),
                    sizeStyle='small',
                    callback=callbacks["leftUp"])
                self.left_up.bind("leftUp", [])

            if arrow == 'leftDown':
                self.left_down = SquareButton(
                    (x0, y2 + (s - small),
                    small, small),
                    unichr(8601),
                    sizeStyle='small',
                    callback=callbacks["leftDown"])
                self.left_down.bind("leftDown", [])

            if arrow == 'rightDown':
                self.right_up = SquareButton(
                    (x2 + (s - small),
                    y2 + (s - small),
                    small, small),
                    unichr(8600),
                    sizeStyle='small',
                    callback=callbacks["rightDown"])
                self.right_up.bind("rightDown", [])

            if arrow == 'rightUp':
                self.right_down = SquareButton(
                    (x2 + (s - small), y0,
                    small, small),
                    unichr(8599),
                    sizeStyle='small',
                    callback=callbacks["rightUp"])
                self.right_down.bind("rightUp", [])
