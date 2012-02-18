colors = ximport('colors')

clr = colors.hsb(0, 1, 1)

size(400, 300)
background(0)

steps = 9

x = 27
y = 18

for i in range(steps):
    clrAngle = (360 / steps) * i
    c = clr.rotate(angle= clrAngle)
    fill(c)    
    print '%s: %s (R) %s (G) %s (B)' % (i, c.r * 255, c.g * 255, c.b * 255)
    rect(x, y, 176, 137)
    x += 21
    y += 16
