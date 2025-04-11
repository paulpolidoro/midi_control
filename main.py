import time
from typing import List

import RPi.GPIO as GPIO

from src.components.display import Display
from src.components.multi_foot import MultiFoot
from src.components.pin import Pin
from src.functions.tap import Tap
from src.controllers.midi_controller import MidiController
from src.devices.ampero_mp80_device import AmperoMP80Device
from src.functions.control import Control
from src.components.foot import Foot
from src.components.led import Led
from src.modes.program_change_mode import ProgramChangeMode

TOTAL_FOOTS = 4

led_power = Led(Pin.LED_POWER)
display: Display = Display()
foots: List[Foot] = []
tap: Tap = Tap(Led(Pin.LED_TAP), display)
control = Control(led=Led(Pin.LED_3), display=display)
multi_foot = MultiFoot()


def main():
    led_power.on()
    tap.set_tap(70)

    program_change = ProgramChangeMode(display, foots, multi_foot)
    program_change.start()

    ampero_mp80 = AmperoMP80Device(on_get_tap=tap.set_tap, on_get_preset_change=program_change.set_preset)

    foots[3].set_on_short_press(tap.tap)
    foots[3].set_on_long_press(control.toggle)

    midi_controller: MidiController = MidiController(ampero_mp80.device_name)
    midi_controller.set_on_receive(ampero_mp80.handle_midi)

    program_change.set_on_preset_change(lambda pc: midi_controller.send_pc(0, pc))
    tap.set_on_tap(lambda bpm: midi_controller.send_cc(0, ampero_mp80.bpm_to_cc(bpm)))

    midi_controller.connect()

    try:
        while True:
            time.sleep(0.1)
            continue
    except KeyboardInterrupt:
        print("Programa finalizado com sucesso!")
    finally:
        led_power.blink(500, 500)
        tap.stop()
        midi_controller.disconnect()
        multi_foot.stop()
        display.clear()

        display.show('BYE', 30, 'Shutting down...')

        time.sleep(2)
        led_power.off()
        GPIO.cleanup()

if __name__ =="__main__":
    for i in range(TOTAL_FOOTS):
        foots.append(Foot(getattr(Pin, f"FOOT_{i}"), f"ft{i}"))

    main()