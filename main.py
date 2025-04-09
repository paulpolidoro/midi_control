import time
from typing import List

import RPi.GPIO as GPIO

from src.components.display import Display
from src.components.multi_foot import MultiFoot
from src.components.tap import Tap
from src.controllers.midi_controller import MidiController
from src.controllers.program_change import ProgramChange
from src.devices.ampero_mp80 import AmperoMP80
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
    tap.set_tap(70)

    program_change = ProgramChange(display, 99, 3)
    program_change.set_preset(0)

    foots[0].set_on_press(lambda: program_change.set_preset_by_index(0))
    foots[1].set_on_press(lambda: program_change.set_preset_by_index(1))
    foots[2].set_on_press(lambda: program_change.set_preset_by_index(2))
    foots[3].set_on_press(lambda: tap.tap())
    foots[3].set_on_long_press(control.toggle)

    multi_foot.set_on_short_press_ab(program_change.bank_down)
    multi_foot.set_on_short_press_bc(program_change.bank_up)

    ampero_mp80: AmperoMP80 = AmperoMP80(program_change, tap)
    midi_controller: MidiController = MidiController(ampero_mp80.input_name, ampero_mp80.output_name,
                                                     ampero_mp80.handle_midi)

    program_change.set_midi_controller(midi_controller)
    tap.set_midi_controller(midi_controller)
    control.set_midi_controller(midi_controller)

    try:
        midi_controller.connect_ports()
        midi_controller.start_receiving()
        midi_controller.start_monitoring()
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
        midi_controller.close()

if __name__ =="__main__":
    start_components()
    main()