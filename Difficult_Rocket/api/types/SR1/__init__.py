#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from typing import Dict, Union
from dataclasses import dataclass

# pyglet
# import pyglet
from pyglet.image import load, AbstractImage

# Difficult Rocket
from Difficult_Rocket.utils.typings import Options


@dataclass
class SR1PartData:
    x: float
    y: float
    id: int
    type: str
    angle: float
    angle_v: float
    editor_angle: int
    flip_x: bool
    flip_y: bool
    explode: bool
    textures: str


class SR1Textures(Options):
    """ 存储 sr1 的材质 img """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flush_option()
        for image_name in self.cached_options:
            setattr(self, image_name, load(f'textures/parts/{image_name}.png'))
        self.flush_option()

    def get_texture(self, name: str):
        assert name in self.cached_options
        return self.cached_options.get(name)

    Battery:               AbstractImage = None
    Beam:                  AbstractImage = None
    CoverBottom:           AbstractImage = None
    CoverStretch:          AbstractImage = None
    CoverTop:              AbstractImage = None
    DetacherRadial:        AbstractImage = None
    DetacherVertical:      AbstractImage = None
    DockingConnector:      AbstractImage = None
    DockingPort:           AbstractImage = None
    EngineIon:             AbstractImage = None
    EngineLarge:           AbstractImage = None
    EngineMedium:          AbstractImage = None
    EngineSmall:           AbstractImage = None
    EngineTiny:            AbstractImage = None
    Fuselage:              AbstractImage = None
    LanderLegJoint:        AbstractImage = None
    LanderLegLower:        AbstractImage = None
    LanderLegPreview:      AbstractImage = None
    LanderLegUpper:        AbstractImage = None
    NoseCone:              AbstractImage = None
    Parachute:             AbstractImage = None
    ParachuteCanister:     AbstractImage = None
    ParachuteCanisterSide: AbstractImage = None
    Pod:                   AbstractImage = None
    Puffy750:              AbstractImage = None
    RcsBlock:              AbstractImage = None
    SideTank:              AbstractImage = None
    SolarPanel:            AbstractImage = None
    SolarPanelBase:        AbstractImage = None
    SolidRocketBooster:    AbstractImage = None
    TankLarge:             AbstractImage = None
    TankMedium:            AbstractImage = None
    TankSmall:             AbstractImage = None
    TankTiny:              AbstractImage = None
    Wheel:                 AbstractImage = None
    Wing:                  AbstractImage = None


class SR1PartTexture:
    part_type_sprite: Dict[str, str] = {'pod-1': 'Pod',
                                        'detacher-1': 'DetacherVertical',
                                        'detacher-2': 'DetacherRadial',
                                        'wheel-1': 'Wheel',
                                        'wheel-2': 'Wheel',
                                        'fuselage-1': 'Fuselage',
                                        'strut-1': 'Beam',
                                        'fueltank-0': 'TankTiny',
                                        'fueltank-1': 'TankSmall',
                                        'fueltank-2': 'TankMedium',
                                        'fueltank-3': 'TankLarge',
                                        'fueltank-4': 'Puffy750',
                                        'fueltank-5': 'SideTank',
                                        'engine-0': 'EngineTiny',
                                        'engine-1': 'EngineSmall',
                                        'engine-2': 'EngineMedium',
                                        'engine-3': 'EngineLarge',
                                        'engine-4': 'SolidRocketBooster',
                                        'ion-0': 'EngineIon',
                                        'parachute-1': 'ParachuteCanister',
                                        'nosecone-1': 'NoseCone',
                                        'rcs-1': 'RcsBlock',
                                        'solar-1': 'SolarPanelBase',
                                        'battery-0': 'Battery',
                                        'dock-1': 'DockingConnector',
                                        'port-1': 'DockingPort',
                                        'lander-1': 'LanderLegPreview'}

    @classmethod
    def get_sprite_from_type(cls, name: str) -> Union[None, str]:
        if name not in cls.part_type_sprite:
            return None
        return cls.part_type_sprite[name]

#
#
# from xml.etree.ElementTree import Element, ElementTree
# from defusedxml.ElementTree import parse
#
# part_list = parse("../../../../textures/PartList.xml")
# part_list_root: Element = part_list.getroot()
# print(part_list_root.tag, part_list_root.attrib)
#
# part_types = part_list_root.find('PartTypes')
#
# for x in list(part_list_root):
#     print(f'tag: {x.tag} attr: {x.attrib}')
#
# for part_type in list(part_list_root):
#     part_type: Element
#     print(f'\'{part_type.attrib.get("id")}\': \'{part_type.attrib.get("sprite")}\'')
#
#
