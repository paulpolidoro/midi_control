from src.components.led import Led
from typing import List

from src.hardware import pins


class ProgramChange:
    def __init__(self, presets: int = 3, banks: int = 2, max_presets: int = 99, current_preset: int = 0):
        self._presets = presets
        self._banks = banks
        self._max_presets = max_presets

        self._current_preset = current_preset
        self._current_bank = self._current_preset // self._presets

        self._leds: List[Led] = []

        for i in range(1, self._presets):
            self._leds.append(Led(getattr(pins, f"LED_{i}")))

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

    def set_preset_by_index(self, foot_index:int):
        self.set_preset((self._current_bank * foot_index) - 1)

    def _turn_off_all_leds(self):
        for led in self._leds:
            led.off()
