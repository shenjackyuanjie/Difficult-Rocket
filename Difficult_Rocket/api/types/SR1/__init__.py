#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

# pyglet
import pyglet
from pyglet.image import load, AbstractImage

# Difficult Rocket
from Difficult_Rocket.utils.typings import Options


class SR1Textures(Options):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flush_option()
        for image_name in self.cached_options:
            setattr(self, image_name, load(f'textures/parts/{image_name}.png'))
        self.flush_option()
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




