"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""


def mbool(thing):  # stand for my bool
    if (thing == "True") or (thing == 1) or (thing == "1"):
        return True
    elif (thing == "False") or (thing == 0) or (thing == "0"):
        return False
    else:
        raise ValueError("Need a 'like bool' not anything else")
