import threading
import time

from src.components.display import Display
from src.components.led import Led
from typing import List

from src.hardware import pins


class ProgramChange:
    TIME_WAIT_PRESET = 4
    
    _letter = ["A", "B", "C", "D", "E", "F"]

    def __init__(self, display: Display, max_presets: int, presets_per_bank: int = 3):
        self._presets_per_bank = presets_per_bank
        self._max_presets = max_presets
        self._max_banks = max_presets // self._presets_per_bank
        self._display = display

        self._current_preset = 0
        self._current_bank = 1

        self._is_change_bank = False
        self._change_bank_start = None
        self._next_bank = self._current_bank

        self._leds: List[Led] = []

        for i in range(self._presets_per_bank):
            self._leds.append(Led(getattr(pins, f"LED_{i}")))

    def bank_up(self):
        if self._next_bank < self._max_banks:
            self._next_bank += 1

            self._change_bank_start = time.time()

            if not self._is_change_bank:
                thread = threading.Thread(target=self._change_bank)
                thread.start()

            self._display.bank_change_wait(self._next_bank)

    def bank_down(self):
        if self._next_bank > 1:
            self._next_bank -= 1

            self._change_bank_start = time.time()

            if not self._is_change_bank:
                thread = threading.Thread(target=self._change_bank)
                thread.start()

            self._display.bank_change_wait(self._next_bank)

    def preset_up(self):
        if self._current_preset < self._max_presets:
            self.set_preset(self._current_preset + 1)

    def preset_down(self):
        if self._current_preset > 0:
            self.set_preset(self._current_preset - 1)

    def set_preset(self, preset: int):
        self._current_preset = preset
        self._current_bank = (self._current_preset // self._presets_per_bank) + 1
        self._next_bank = self._current_bank
        self._is_change_bank = False

        self._turn_off_all_leds()
        self._leds[self._current_preset % self._presets_per_bank].on()

        self._display.show_preset(self._current_bank, self._letter[self._current_preset % self._presets_per_bank])

    def bank_change_by_foot(self, foots):
        if len(foots) >= 2 and foots[0] == 'ft0' and foots[1] == 'ft1':
            self.bank_down()
        elif len(foots) >= 2 and foots[0] == 'ft1' and foots[1] == 'ft2':
            self.bank_up()

    def set_preset_by_index(self, foot_index:int):
        self.set_preset((self._next_bank - 1) * self._presets_per_bank - 1 + (foot_index + 1))

    def _turn_off_all_leds(self):
        for led in self._leds:
            led.off()

    def _change_bank(self):
        self._is_change_bank = True

        while (time.time() - self._change_bank_start) < self.TIME_WAIT_PRESET and self._is_change_bank:
            time.sleep(0.1)

        self._next_bank = self._current_bank
        self._is_change_bank = False

