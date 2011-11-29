# [h] mark group

f = CurrentFont()

group_name = 'lowercase_basic'

color = (1.0, 0.0, 0.0, 1.0)

if f.groups.has_key(group_name):
    # mark group
    for gname in f.groups[group_name]:
        f[gname].mark = color
        f[gname].update()
    f.update()
