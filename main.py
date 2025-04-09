import time
from typing import List

import RPi.GPIO as GPIO

from src.components.display import Display
from src.components.multi_foot import MultiFoot
from src.components.tap import Tap
from src.controllers.program_change import ProgramChange
from src.functions.control import Control
from src.hardware import pins
from src.components.foot import Foot, button_states
from src.components.led import Led

display: Display = Display()
foots: List[Foot] = []
tap: Tap = Tap(Led(pins.LED_TAP), display)
control = Control(led=Led(pins.LED_3), display=display)

def start_components():
    for i in range(4):
        foots.append(Foot(getattr(pins, f"FOOT_{i}"), f"ft{i}"))

def main():
    multi_foot = MultiFoot()
    led_power = Led(pins.LED_POWER)
    led_power.on()

    program_change = ProgramChange(display, 99, 3)
    program_change.set_preset(14)

    foots[0].set_on_press(lambda: program_change.set_preset_by_index(0))
    foots[1].set_on_press(lambda: program_change.set_preset_by_index(1))
    foots[2].set_on_press(lambda: program_change.set_preset_by_index(2))
    foots[3].set_on_press(lambda: tap.tap())
    foots[3].set_on_long_press(control.toggle)

    multi_foot.set_on_short_press_ab(program_change.bank_down)
    multi_foot.set_on_short_press_bc(program_change.bank_up)

    try:
        while True:

            time.sleep(0.1)
            continue
    except KeyboardInterrupt:
        print("Programa finalizado com sucesso!")
    finally:
        multi_foot.stop()
        tap.stop()
        GPIO.cleanup()
        display.clear()

if __name__ =="__main__":
    start_components()
    main()