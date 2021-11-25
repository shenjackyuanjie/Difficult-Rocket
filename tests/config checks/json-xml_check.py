"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import json
import pprint
from xmltodict import xmltodict

json_ = {
    'a': {
        '-abc': '123',
        'bbb':  [
            'a',
            'b',
            'c'
        ]
    }
}

unparse = xmltodict.unparse(json_)
print(unparse)

paste = xmltodict.parse("""<?xml version="1.0" encoding="utf-8" ?>
<PartTypes xmlns="http://jundroo.com/simplerockets/partlist.xsd">
	<PartType id="pod-1" name="Command Pod Mk1" description="This is your ship's brain. Be careful with it." sprite="Pod.png" type="pod" mass="1.0" width="4" height="3" hidden="true">
		<Damage disconnect="1500" explode="1500" explosionPower="5" explosionSize="10" />
		<Shape>
			<Vertex x="-2.0" y="-1.5" />
			<Vertex x="2.0" y="-1.5" />
			<Vertex x="1.3" y="1.5" />
			<Vertex x="-1.3" y="1.5" />
		</Shape>
		<AttachPoints>
			<AttachPoint location="TopCenter" />
			<AttachPoint location="BottomCenter" />
		</AttachPoints>
	</PartType>
	<PartType id="detacher-1" name="Detacher" description="Use this to split your ship into stages." sprite="DetacherVertical.png" type="detacher" mass="0.25" width="4" height="1">
		<AttachPoints>
			<AttachPoint location="TopCenter" />
			<AttachPoint location="BottomCenter" />
		</AttachPoints>
	</PartType>
	<PartType id="detacher-2" name="Side Detacher" description="Same as the detacher above, but this works on the sides." sprite="DetacherRadial.png" type="detacher" mass="0.25" width="1" height="4">
		<AttachPoints>
			<AttachPoint location="LeftCenter" />
			<AttachPoint location="RightCenter" />
		</AttachPoints>
	</PartType>
	<PartType id="wheel-1" name="Old Wheel" description="Your turn buttons can control these wheels." sprite="Wheel.png" type="wheel" mass="0.25" width="4" height="4" ignoreEditorIntersections="true" hidden="true" disableEditorRotation="true">
		<AttachPoints>
			<AttachPoint x="0" y="0" breakAngle="180" />
		</AttachPoints>
	</PartType>
	<PartType id="wheel-2" name="Wheel" description="Your turn buttons can control these wheels." sprite="Wheel.png" type="wheel" mass="0.25" width="4" height="4" ignoreEditorIntersections="true" disableEditorRotation="true" buoyancy="1.0">
		<AttachPoints>
			<AttachPoint x="0" y="0" breakAngle="180" />
		</AttachPoints>
	</PartType>
	<PartType id="fuselage-1" name="Fuselage" description="Just empty, light weight fuselage. Good for spacing things out." sprite="Fuselage.png" type="fuselage" mass="1.25" width="4" height="4" buoyancy="1.0">
		<AttachPoints>
			<AttachPoint location="TopCenter" fuelLine="true" />
			<AttachPoint location="BottomCenter" fuelLine="true" />
			<AttachPoint location="LeftSide" />
			<AttachPoint location="RightSide" />
		</AttachPoints>
	</PartType>
	<PartType id="strut-1" name="Strut" description="Light weight and strong." sprite="Beam.png" type="strut" mass="2.0" width="16" height="2" canExplode="false" buoyancy="0.5">
		<AttachPoints>
			<AttachPoint location="Top" breakAngle="20" breakForce="150.0" />
			<AttachPoint location="Bottom" breakAngle="20" breakForce="150.0" />
			<AttachPoint location="LeftSide" breakAngle="20" breakForce="150.0" />
			<AttachPoint location="RightSide" breakAngle="20" breakForce="150.0" />
		</AttachPoints>
	</PartType>
	<PartType id="fueltank-0" name="Sloshy T750" description="The smallest tank on the market." sprite="TankTiny.png" type="tank" mass="1.85" width="4" height="2">
		<Tank fuel="750.0" dryMass="0.35" fuelType="0" />
		<Damage disconnect="2500" explode="2500" explosionPower="5" explosionSize="10" />
		<AttachPoints>
			<AttachPoint location="TopCenter" fuelLine="true" />
			<AttachPoint location="BottomCenter" fuelLine="true" />
			<AttachPoint location="LeftSide" fuelLine="true" />
			<AttachPoint location="RightSide" fuelLine="true" />
		</AttachPoints>
	</PartType>
	<PartType id="fueltank-1" name="Sloshy T1500" description="Just a small fuel tank. Nothing special." sprite="TankSmall.png" type="tank" mass="3.5" width="4" height="4">
		<Tank fuel="1500.0" dryMass="0.5" />
		<Damage disconnect="2500" explode="2500" explosionPower="5" explosionSize="10" />
		<AttachPoints>
			<AttachPoint location="TopCenter" fuelLine="true" />
			<AttachPoint location="BottomCenter" fuelLine="true" />
			<AttachPoint location="LeftSide" fuelLine="true" />
			<AttachPoint location="RightSide" fuelLine="true" />
		</AttachPoints>
	</PartType>
	<PartType id="fueltank-2" name="Sloshy T3000" description="Medium tank for medium purposes." sprite="TankMedium.png" type="tank" mass="6.85" width="4" height="8">
		<Tank fuel="3000.0" dryMass="0.85" />
		<Damage disconnect="2500" explode="2500" explosionPower="5" explosionSize="10" />
		<AttachPoints>
			<AttachPoint location="TopCenter" fuelLine="true" />
			<AttachPoint location="BottomCenter" fuelLine="true" />
			<AttachPoint location="LeftSide" fuelLine="true" />
			<AttachPoint location="RightSide" fuelLine="true" />
		</AttachPoints>
	</PartType>
	<PartType id="fueltank-3" name="Sloshy T6000" description="It's big, but it's heavy too." sprite="TankLarge.png" type="tank" mass="13.2" width="4" height="16">
		<Tank fuel="6000.0" dryMass="1.2" />
		<Damage disconnect="2500" explode="2500" explosionPower="5" explosionSize="10" />
		<AttachPoints>
			<AttachPoint location="TopCenter" fuelLine="true" />
			<AttachPoint location="BottomCenter" fuelLine="true" />
			<AttachPoint location="LeftSide" fuelLine="true" />
			<AttachPoint location="RightSide" fuelLine="true" />
		</AttachPoints>
	</PartType>
	<PartType id="fueltank-4" name="Puffy T750" description="Monopropellant for RCS thrusters." sprite="Puffy750.png" type="tank" mass="1.85" width="4" height="2" category="Satellite">
		<Tank fuel="750.0" dryMass="0.35" fuelType="1" />
		<Damage disconnect="2500" explode="2500" explosionPower="5" explosionSize="10" />
		<AttachPoints>
			<AttachPoint location="TopCenter" />
			<AttachPoint location="BottomCenter" />
			<AttachPoint location="LeftSide" />
			<AttachPoint location="RightSide" />
		</AttachPoints>
	</PartType>
	<PartType id="fueltank-5" name="Puffy T275" description="Side attaching monopropellant tank." sprite="SideTank.png" type="tank" mass="0.65" width="1" height="3" category="Satellite">
		<Tank fuel="275.0" dryMass="0.13" fuelType="1" />
		<Damage disconnect="2500" explode="2500" explosionPower="5" explosionSize="10" />
		<AttachPoints>
			<AttachPoint location="RightCenter" flipX="true" group="1" />
			<AttachPoint location="LeftCenter" group="1" />
		</AttachPoints>
	</PartType>
	<PartType id="battery-0" name="Batteries" description="Batteries can be recharged by solar panels." sprite="Battery.png" type="tank" mass="1.25" width="4" height="1" category="Satellite" sandboxOnly="true">
		<Tank fuel="250.0" dryMass="1.24" fuelType="2" />
		<Damage disconnect="2500" explode="2500" explosionPower="5" explosionSize="10" />
		<AttachPoints>
			<AttachPoint location="TopCenter" />
			<AttachPoint location="BottomCenter" />
			<AttachPoint location="LeftSide" />
			<AttachPoint location="RightSide" />
		</AttachPoints>
	</PartType>
	<PartType id="engine-0" name="Tiny 21" description="Really only useful for landing on Smoon." sprite="EngineTiny.png" type="engine" mass="0.5" width="4" height="2" buoyancy="0.5">
		<Engine power="0.25" consumption="4.00" size="0.50" turn="20.0" throttleExponential="true" fuelType="0" />
		<Shape>
			<Vertex x="-0.9" y="-1.0" />
			<Vertex x="0.9" y="-1.0" />
			<Vertex x="2.0" y="1.0" />
			<Vertex x="-2.0" y="1.0" />
		</Shape>
		<AttachPoints>
			<AttachPoint location="TopCenter" fuelLine="true" order="1" />
			<AttachPoint location="BottomCenter" order="2" />
		</AttachPoints>
	</PartType>
	<PartType id="engine-1" name="Tiny 85" description="Not bad for landing and it can do a little orbiting too." sprite="EngineSmall.png" type="engine" mass="0.75" width="4" height="4" buoyancy="0.5">
		<Engine power="1.0" consumption="25" size="0.60" turn="7.0" throttleExponential="true" />
		<Shape>
			<Vertex x="-0.9" y="-2.0" />
			<Vertex x="0.9" y="-2.0" />
			<Vertex x="2.0" y="2.0" />
			<Vertex x="-2.0" y="2.0" />
		</Shape>
		<AttachPoints>
			<AttachPoint location="TopCenter" fuelLine="true" order="1" />
			<AttachPoint location="BottomCenter" order="2" />
		</AttachPoints>
	</PartType>
	<PartType id="engine-2" name="Blasto 170" description="Good for take-offs and orbits. It's a solid engine." sprite="EngineMedium.png" type="engine" mass="1.25" width="4" height="6" buoyancy="0.5">
		<Engine power="2.0" consumption="50" size="0.8" turn="3.0" />
		<Shape>
			<Vertex x="-0.9" y="-3.0" />
			<Vertex x="0.9" y="-3.0" />
			<Vertex x="2.0" y="3.0" />
			<Vertex x="-2.0" y="3.0" />
		</Shape>
		<AttachPoints>
			<AttachPoint location="TopCenter" fuelLine="true" order="1" />
			<AttachPoint location="BottomCenter" order="2" />
		</AttachPoints>
	</PartType>
	<PartType id="engine-3" name="Blasto 425" description="Great for taking off but it guzzles fuel like a monster." sprite="EngineLarge.png" type="engine" mass="2.0" width="4" height="8" buoyancy="0.5">
		<Engine power="5.0" consumption="125" size="1.0" turn="2.5" />
		<Shape>
			<Vertex x="-0.9" y="-4.0" />
			<Vertex x="0.9" y="-4.0" />
			<Vertex x="2.0" y="4.0" />
			<Vertex x="-2.0" y="4.0" />
		</Shape>
		<AttachPoints>
			<AttachPoint location="TopCenter" fuelLine="true" order="1" />
			<AttachPoint location="BottomCenter" order="2" />
		</AttachPoints>
	</PartType>
	<PartType id="engine-4" name="Blasto SRB 500" description="Great for blasting off, but they can't be throttle or turn." sprite="SolidRocketBooster.png" type="engine" mass="22.0" width="4" height="26" buoyancy="0.5" coverHeight="2" sandboxOnly="true">
		<Engine power="6.0" consumption="175" size="1.0" turn="0.0" fuelType="3" />
		<Tank fuel="9000.0" dryMass="3.15" />
		<AttachPoints>
			<AttachPoint location="TopCenter" order="1" />
			<AttachPoint location="BottomCenter" order="2" />
			<AttachPoint location="LeftSide" />
			<AttachPoint location="RightSide" />
		</AttachPoints>
	</PartType>
	<PartType id="ion-0" name="Ion Engine" description="Low power, high efficiency and powered by batteries." sprite="EngineIon.png" type="engine" mass="0.5" width="4" height="2" buoyancy="0.5" sandboxOnly="true">
		<Engine power="0.10" consumption="4.00" size="0.3" turn="10.0" throttleExponential="false" fuelType="2" />
		<Shape>
			<Vertex x="-0.9" y="-1.0" />
			<Vertex x="0.9" y="-1.0" />
			<Vertex x="2.0" y="1.0" />
			<Vertex x="-2.0" y="1.0" />
		</Shape>
		<AttachPoints>
			<AttachPoint location="TopCenter" fuelLine="true" order="1" />
			<AttachPoint location="BottomCenter" order="2" />
		</AttachPoints>
	</PartType>
	<PartType id="parachute-1" name="Parachute" description="Land safely, but only works in an atmosphere." sprite="ParachuteCanister.png" type="parachute" mass="0.25" width="4" height="1" canExplode="false">
		<AttachPoints>
			<AttachPoint location="BottomCenter" breakAngle="90" breakForce="150.0" />
		</AttachPoints>
	</PartType>
	<PartType id="nosecone-1" name="Nose Cone" description="Reduces drag a little for those bulky fuel tanks." sprite="NoseCone.png" type="nosecone" mass="0.05" width="4" height="2" drag="-1.0">
		<Shape>
			<Vertex x="-2.0" y="-1.0" />
			<Vertex x="2.0" y="-1.0" />
			<Vertex x="0.6" y="0.6" />
			<Vertex x="-0.6" y="0.6" />
		</Shape>
		<AttachPoints>
			<AttachPoint location="BottomCenter" />
		</AttachPoints>
	</PartType>
	<PartType id="rcs-1" name="RCS Thrusters" description="Reaction control system for precision maneuvering." sprite="RcsBlock.png" type="rcs" mass="0.25" width="1" height="3" category="Satellite" disableEditorRotation="true" buoyancy="0.5">
		<Rcs power="1.0" consumption="0.1" size="1.00" />
		<AttachPoints>
			<AttachPoint location="RightCenter" flipX="true" group="1" />
			<AttachPoint location="LeftCenter" group="1" />
		</AttachPoints>
	</PartType>
	<PartType id="solar-1" name="Solar Panel" description="Expanding solar panel." sprite="SolarPanelBase.png" type="solar" mass="1.0" width="1" height="4" category="Satellite" sandboxOnly="true">
		<Solar chargeRate="2.0" />
		<Damage disconnect="250" explode="3000" explosionPower="1" explosionSize="5" />
		<AttachPoints>
			<AttachPoint location="RightCenter" flipX="true" group="1" />
			<AttachPoint location="LeftCenter" group="1" />
		</AttachPoints>
	</PartType>
	<PartType id="dock-1" name="Docking Plug" description="One per ship. Connects to a docking port." sprite="DockingConnector.PNG" type="dockconnector" mass="0.25" width="4" height="1" friction="0.1" category="Satellite" maxOccurrences="1" canExplode="false">
		<Shape>
			<Vertex x="-1.0" y="-0.5" />
			<Vertex x="1.0" y="-0.5" />
			<Vertex x="1.0" y="-0.1" />
			<Vertex x="0.4" y="0.5" />
			<Vertex x="-0.4" y="0.5" />
			<Vertex x="-1.0" y="-0.1" />
		</Shape>
		<AttachPoints>
			<AttachPoint location="BottomCenter" breakAngle="90" breakForce="150.0" group="1" />
		</AttachPoints>
	</PartType>
	<PartType id="port-1" name="Docking Port" description="Accepts a docking plug for docking in space." sprite="DockingPort.png" type="dockport" mass="0.75" width="2" height="4" friction="0.1" category="Satellite" buoyancy="0.5">
		<Shape>
			<Vertex x="-0.2" y="-2.0" />
			<Vertex x="1.0" y="-2.0" />
			<Vertex x="1.0" y="2.0" />
			<Vertex x="-0.2" y="2.0" />
		</Shape>
		<Shape>
			<Vertex x="-1.0" y="-2.0" />
			<Vertex x="0.0" y="-2.0" />
			<Vertex x="0.0" y="-0.1" />
			<Vertex x="-1.0" y="-1.10" />
		</Shape>
		<Shape>
			<Vertex x="-1.0" y="1.10" />
			<Vertex x="0.0" y="0.1" />
			<Vertex x="0.0" y="2.0" />
			<Vertex x="-1.0" y="2.0" />
		</Shape>
		<Shape sensor="true">
			<Vertex x="-0.33" y="-1.0" />
			<Vertex x="-0.2" y="-1.0" />
			<Vertex x="-0.2" y="1.0" />
			<Vertex x="-0.33" y="1.0" />
		</Shape>
		<AttachPoints>
			<AttachPoint location="RightCenter" group="1" />
			<AttachPoint location="LeftCenter" flipX="true" group="1" />
		</AttachPoints>
	</PartType>
	<PartType id="lander-1" name="Lander" description="Activate these babies to make landing a little easier." sprite="LanderLegPreview.png" type="lander" mass="0.5" width="1" height="5" ignoreEditorIntersections="true" buoyancy="0.5">
		<Lander maxAngle="140" minLength="2.26" maxLength="4.15" angleSpeed="25" lengthSpeed="0.5" width="0.5" />
		<AttachPoints>
			<AttachPoint location="LeftCenter" group="1" />
			<AttachPoint location="RightCenter" group="1" />
		</AttachPoints>
	</PartType>
</PartTypes>
""")
paste = json.dumps(paste)

pprint.pprint(paste)
print(paste)
print(type(paste))
# 将paste转换成字典格式


abc = {'abc': '1234'}

print(xmltodict.unparse(eval(paste)))

from libs import xmltodict

print(xmltodict.unparse(eval(paste)))
