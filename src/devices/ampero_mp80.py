from src.components.tap import Tap
from src.controllers.program_change import ProgramChange


def sys_to_bpm(tempo_sysex):
    if tempo_sysex[0] == 0:
        return tempo_sysex[1]
    elif tempo_sysex[0] == 1:
        return tempo_sysex[1] + 128


class AmperoMP80:
    # input_name = "HOTONE MP80 PRODUCT 0"
    # output_name = "HOTONE MP80 PRODUCT 1"

    input_name = "HOTONE MP80 PRODUCT:HOTONE MP80 PRODUCT MIDI 1 20:0"
    output_name = "HOTONE MP80 PRODUCT:HOTONE MP80 PRODUCT MIDI 1 20:0"

    _tap_identifier = [33, 37, 127, 77, 80, 45, 80, 18, 0, 2, 0, 32]
    _preset_change = [33, 37, 127, 77, 80, 45, 80, 18, 0, 2, 6, 4]

    def __init__(self, program_change:ProgramChange, tap:Tap):
        self._program_change = program_change
        self._tap = tap

    def handle_midi(self, data):
        print(data)

        if list(data[:len(self._tap_identifier)]) == self._tap_identifier:
            bpm = sys_to_bpm([data[-2], data[-1]])

            print("Tap detected", data, bpm)

            self._tap.set_tap(bpm)

        elif list(data[:len(self._preset_change)]) == self._preset_change:
            preset = data[-1] - 1
            print("Preset detected", data, preset)

            self._program_change.set_preset(preset)



