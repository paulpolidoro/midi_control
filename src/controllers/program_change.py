from src.components.foot import Foot
from src.components.led import Led
from src.hardware import pins
from typing import List


class ProgramChange:
    def __init__(self, presets: int = 3, banks: int = 2, max_presets: int = 99, current_preset: int = 0):
        self._presets = presets
        self._banks = banks
        self._max_presets = max_presets

        self._current_preset = current_preset
        self._current_bank = self._current_preset // self._presets

        self._foots: List[Foot] = []
        self._leds: List[Led] = []

        self._init_config()

    def bank_up(self):
        if self._current_bank < self._banks:
            self._current_bank += 1

    def bank_down(self):
        if self._current_bank > 1:
            self._current_bank -= 1

    def preset_up(self):
        if self._current_preset < self._max_presets:
            self.set_preset(self._current_preset + 1)

    def preset_down(self):
        if self._current_preset > 0:
            self.set_preset(self._current_preset - 1)

    def set_preset(self, preset: int):
        self._current_preset = preset
        self._current_bank = self._current_preset // self._presets

        self._turn_off_all_leds()
        self._leds[self._current_preset % self._presets].on()

    def _set_preset_by_foot(self, name):
        for i in range(1, self._presets):
            if name == f"ps{i}":
                self.set_preset((self._current_bank * i) - 1)

    def _init_config(self):
        for i in range(1, self._presets):
            self._foots.append(Foot(getattr(pins, f"FOOT_{i}"), name=f"ps{i}", on_press=self._set_preset_by_foot))
            self._leds.append(Led(getattr(pins, f"LED_{i}")))

        self.set_preset(self._current_preset)

    def _turn_off_all_leds(self):
        for led in self._leds:
            led.off()
