import time
from yeelight import Bulb
from yeelight import Flow
from yeelight.transitions import *


def sunrise():
    # dim red, to warm yellow, to bright light
    transitions = [
            RGBTransition(red=0xFF, green=0x4D, blue=0x00, duration=50, brightness=1),
            TemperatureTransition(degrees=1700, duration=3600, brightness=10),
            TemperatureTransition(degrees=2700, duration=5400, brightness=100),
        ]

    # this is our bulb
    bulb = Bulb("10.25.8.47")
    flow = Flow(
        count = 1,
        transitions=transitions,
    )

    # make sure it's initially on before starting flow
    bulb.turn_on(brightness=1)
    bulb.start_flow(flow)

    # wait before turning off
    time.sleep(15)
    bulb.turn_off()
