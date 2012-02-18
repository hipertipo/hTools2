colors = ximport("colors")

# from hTools2.modules.color import solarized

base03 = colors.rgb(0, 43, 54, range=255)
base02 = colors.rgb(7, 54, 66, range=255)

base2 = colors.rgb(238, 232, 213, range=255)
base3 = colors.rgb(253, 246, 227, range=255)

base01 = colors.rgb(88, 110, 117, range=255)
base00 = colors.rgb(101, 123, 131, range=255)
base0 = colors.rgb(131, 148, 150, range=255)
base1 = colors.rgb(147, 161, 161, range=255)

yellow = colors.rgb(181, 137, 0, range=255)
orange = colors.rgb(203, 75, 22, range=255)
red = colors.rgb(220, 50, 47, range=255)
magenta = colors.rgb(211, 54, 130, range=255)
violet = colors.rgb(108, 113, 196, range=255)
blue = colors.rgb(38, 139, 210, range=255)
cyan = colors.rgb(42, 161, 152, range=255)
green = colors.rgb(133, 152, 0, range=255)

#---------------

txt = "At the same time, I feel I'm still very interested in wonder and surprise, but understand that how we get there might not always be the same mechanics. For example, this last year I have been giving talks really, kind of incessantly, because of the success of the EyeWriter project, and I've noticed that I'm able, when doing it well, to really channel TEMPT, his message, energy, will and determination to people via talking. This also, when done right, has the potential to create wonder in audience members."

# background

fill(base03)
rect(-32, -32, 1102, 790, roundness=.1)

fill(base02)
rect(-18, 211, 1119, 327, roundness=.1)

fill(base2)
rect(-9, 285, 1100, 320, roundness=.1)

fill(base3)
rect(-15, 390, 1089, 257, roundness=.1)

# text

fill(base01)
font('EMono', 13)
text(txt, 56, 128, width=200)

fill(base00)
font('EMono', 13)
text(txt, 296, 122, width=200)

fill(base0)
font('EMono', 13)
text(txt, 535, 124, width=200)

fill(base1)
font('EMono', 13)
text(txt, 756, 124, width=200)

# colors

y = 42

fill(yellow)
rect(114, y, 20, 20)

fill(orange)
rect(175, y, 20, 20)

fill(red)
rect(239, y, 20, 20)

fill(magenta)
rect(300, y, 20, 20)

fill(violet)
rect(364, y, 20, 20)

fill(blue)
rect(425, y, 20, 20)

fill(cyan)
rect(483, y, 20, 20)

fill(green)
rect(561, y, 20, 20)
