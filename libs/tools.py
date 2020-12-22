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

def D_C(listA, listB): # stand for Duplicate check
    """
    usage:\n
    input two list\n
    the fun will do duplicate check and sort then\n
    the fun won't return any thing just change the list now
    """
    for unit in listB:
        if unit in listA:
            listA.remove(unit)
            listB.remove(unit)
        else:
            continue
    listA.sort()
    listB.sort()
    return

def S_C_float_check(SC): # stand for Scientific notation's float check
    pass