#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""


import threading


class Orbit_demo(threading.Thread):

    def __init__(self, threadID, delivery_class):
        # father class __init__()
        threading.Thread.__init__(self)
        # dic
        self.ship_info = {'mass': [1, 5, ['kg'], []], 'force': []}
        self.planet_system = {'Solar System': {'planets': {
            'smearth': {'description': '', 'gravity': 9.81, 'radius': 63710000, 'map_color': [103, 157, 255]}
        }
        }
        }
        self.this_planet_info = {}
        self.back_ground_element = {}
        self.back_ground_image = ''

    def main(self):
        print('ha ?')

    def orbit_math(self):
        pass
