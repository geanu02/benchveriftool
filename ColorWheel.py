import math


def color_wheel(pour_cent):
    r_float = ((100 - pour_cent) * 1.4259259) + 16
    reds = math.floor(r_float)
    g_float = ((100 - pour_cent) * 1.189873418) + 42
    greens = math.floor(g_float)
    blues = 180 - pour_cent
    return [reds, greens, blues]
