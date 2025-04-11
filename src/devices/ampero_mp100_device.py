from abc import ABC
from typing import Optional, Callable, List

from src.devices.device import Device


class AmperoMP100Device(Device, ABC):
    # Definições do dispositivo
    brand    = "hotone"
    name     = "Ampero MP100"
    model    = "MP100"
    device_name  = "HOTONE MP100 PRODUCT:HOTONE MP100 PRODUCT MIDI 1 20:0"
    max_presets = 99
    presets_per_bank = 3

    """Comandos MIDI"""
    # MIDI de presset
    CC_VOLUME = (7, 0)
    CC_EXP1_LEVEL = (11, 0)
    CC_EXP1_ON = (13, 127)
    CC_EXP1_OFF = (13, 0)
    CC_KNOB1_MSB = (16, 0)
    CC_KNOB1_LSB = (17, 0)
    CC_KNOB2_MSB = (18, 0)
    CC_KNOB2_LSB = (19, 0)
    CC_KNOB3_MSB = (20, 0)
    CC_KNOB3_LSB = (21, 0)
    CC_BANK_BACK = (22, 127)
    CC_BANK_FORWARD = (23, 127)
    CC_PATCH_BACK = (24, 127)
    CC_PATCH_FORWARD = (25, 127)
    CC_BANK_BACK_WAIT_MODE = (26, 127)
    CC_BANK_FORWARD_WAIT_MODE = (27, 127)

    # MIDI efeitos
    CC_FX1_ON = (48,127)
    CC_FX1_OFF = (48,0)
    CC_FX2_ON = (49,127)
    CC_FX2_OFF = (49,0)
    CC_AMP_ON = (50,127)
    CC_AMP_OFF = (50,0)
    CC_NR_ON = (51,127)
    CC_NR_OFF = (51,0)
    CC_CAB_ON = (52,127)
    CC_CAB_OFF = (52,0)
    CC_EQ_ON = (53,127)
    CC_EQ_OFF = (53,0)
    CC_FX3_ON = (54,127)
    CC_FX3_OFF = (54,0)
    CC_DLY_ON = (55,127)
    CC_DLY_OFF = (55,0)
    CC_RVB_ON = (56,127)
    CC_RVB_OFF = (56,0)
    CC_TUNNER_ON = (57,127)
    CC_TUNNER_OFF = (57,0)

    # MIDI bateria
    CC_DRUM_ON = (58,127)
    CC_DRUM_OFF = (58,0)
    CC_DRUM_PLAY = (59,127)
    CC_DRUM_STOP = (59,0)
    CC_DRUM_RTM = (60,99)
    CC_DRUM_VOLUME = (61,100)

    # MIDI looper
    CC_LOOPER_ON = (62,127)
    CC_LOOPER_OFF = (62,0)
    CC_LOOPER_REC = (63,127)
    CC_LOOPER_PLAY = (64,127)
    CC_LOOPER_STOP = (64,0)
    CC_LOOPER_TEMPO_NORMAL = (65,127)
    CC_LOOPER_TEMPO_HALF = (65,0)
    CC_LOPPER_REVERSE = (66,0)
    CC_LOOPER_NORMAL = (66,127)
    CC_DELETE_LOOP = (68,127)
    CC_LOOPER_REC_VOLUME=(69,99)
    CC_LOOPER_PLAY_VOLUME=(70,99)
    CC_LOOPER_PLACEMENT_REAR =(71,0)
    CC_LOOPER_PLACEMENT_FROM =(71,127)

    # MIDI outros
    CC_CTRL_TOGGLE = (72,127)
    CC_TAP_TEMPO = (75, 127)
    CC_DEVICE_LOCK = (76,0)
    CC_DEVICE_UNLOCK = (76,127)


    """Identificadores de comandos MIDI recebidos"""
    _identifier_tap    = [33, 37, 127, 77, 80, 45, 80, 18, 0, 2, 0, 32]
    _identifies_preset = [33, 37, 127, 77, 80, 45, 80, 18, 0, 2, 6, 4]

    @staticmethod
    def sysex_to_bpm(bits:List[int]):
        return bits[1] if bits[0] == 0 else bits[1] + 128

    @staticmethod
    def bpm_to_cc(bpm:int):
        data1 = 0

        if bpm > 127:
            data1 = 1

            data2 = bpm - 128
        else:
            data2 = bpm

        return [[73, min(data1, 1)], [74, min(data2, 127)]]

    def __init__(self, on_get_tap: Optional[Callable[[int], None]] = None, on_get_preset_change: Optional[Callable[[int], None]] = None):
        self._on_get_tap: Optional[Callable[[int], None]] = on_get_tap
        self._on_get_preset_change: Optional[Callable[[int], None]] = on_get_preset_change
        self._log_handle_detected = False

    def handle_midi(self, midi_type: str, data: tuple):
        if list(data[:len(self._identifier_tap)]) == self._identifier_tap:
            bpm = self.sysex_to_bpm([data[-2], data[-1]])

            if self._log_handle_detected:
                print(f"Tap detected: {bpm}")

            self._on_get_tap(bpm)

        elif list(data[:len(self._identifies_preset)]) == self._identifies_preset:
            preset = data[-1] - 1

            if self._log_handle_detected:
                print(f"Preset change detected: {preset}")

            self._on_get_preset_change(preset)

    def set_on_get_tap(self, callback:Callable[[int], None]):
        self._on_get_tap = callback

    def set_on_get_preset_change(self, callback:Callable[[int], None]):
        self._on_get_preset_change = callback

    def log_handle_detected(self, log:bool=True):
        self._log_handle_detected = log
