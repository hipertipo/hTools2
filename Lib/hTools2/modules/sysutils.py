# [h] hTools2.modules.sysutils

def get_context():
    # test for FontLab
    try:
        import FL
        _FL = True
    except:
        _FL = False
    # test for RoboFont
    try:
        import mojo
        _RF = True
    except:
        _RF = False
    # if none is True, return `NoneLab`
    if _FL:
        context = 'FontLab'
    elif _RF:
        context = 'RoboFont'
    else:
        context = 'NoneLab'
    # done
    return context

_ctx = get_context()
