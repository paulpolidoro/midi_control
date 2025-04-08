import time
from typing import List

import RPi.GPIO as GPIO

from src.components.tap import Tap
from src.controllers.foot_controller import FootController
from src.controllers.program_change import ProgramChange
from src.hardware import pins
from src.components.foot import Foot
from src.components.led import Led

controller: FootController = FootController([])
foots: List[Foot] = []
tap: Tap = Tap(pins.LED_TAP)

def start_components():
    for i in range(4):
        foots.append(Foot(getattr(pins, f"FOOT_{i}"), controller, f"ft{i}"))

    controller.foots.extend(foots)
    controller.start_monitoring()

def main():
    led_power = Led(pins.LED_POWER)
    led_power.on()

    program_change = ProgramChange(banks=10)

    foots[0].on_press = program_change.set_preset_by_foot(foots[0].get_name())
    foots[2].on_press = program_change.set_preset_by_foot(foots[1].get_name())
    foots[2].on_press = program_change.set_preset_by_foot(foots[2].get_name())
    foots[4].on_press = tap.tap()

    try:
        while True:
            time.sleep(0.1)
            continue
    except KeyboardInterrupt:
        print("Programa finalizado com sucesso!")
    finally:
        GPIO.cleanup()

if __name__ =="__main__":
    start_components()
    main()
    
