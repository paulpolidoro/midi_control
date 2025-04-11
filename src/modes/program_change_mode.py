from threading import Thread
import time
from abc import ABC

from src.components.display import Display
from src.components.foot import Foot
from src.components.led import Led
from typing import List, Callable, Optional

from src.components.multi_foot import MultiFoot
from src.components.pin import Pin
from src.modes.mode import Mode

class ProgramChangeMode(Mode, ABC):
    TIME_WAIT_PRESET = 4
    UP = 1
    DOWN = -1

    def __init__(self, display: Display, foots:List[Foot], multi_foot:MultiFoot, max_presets: int=99, presets_per_bank: int = 3):
        super().__init__(display, foots, multi_foot)

        self._leds: List[Led] = []

        self._presets_per_bank = presets_per_bank
        self._max_presets = max_presets
        self._max_banks = max_presets // self._presets_per_bank

        self._current_preset = 0
        self._current_bank = 1

        self._is_change_bank:bool = False
        self._change_bank_start:Optional[float]=None
        self._thread_change_bank:Optional[Thread]=None

        self._next_bank = self._current_bank

        self._on_preset_change:Optional[Callable[[int], None]] = None

    def start(self):
        self._setup()
        self._default_view()
        self.set_preset(0)

    def stop(self):
        self._stop_change_bank()

        for i in range(self._presets_per_bank):
            self._leds[i].close()
            self._foots[i].callback_release('on_press')

        self._multi_foots.set_on_short_press_ab('on_short_press_ab')

        if self._presets_per_bank == 4:
            self._multi_foots.callback_release('on_short_press_cd')
        else:
            self._multi_foots.callback_release('on_short_press_bc')

        self._display.clear()

    def _setup(self):
        for i in range(self._presets_per_bank):
            self._leds.append(Led(getattr(Pin, f"LED_{i}")))
            self._foots[i].set_on_press(lambda i=i: self.set_preset_by_index(i))

        self._multi_foots.set_on_short_press_ab(lambda: self.bank_up_down(self.DOWN))

        if self._presets_per_bank == 4:
            self._multi_foots.set_on_short_press_cd(lambda: self.bank_up_down(self.UP))
        else:
            self._multi_foots.set_on_short_press_bc(lambda: self.bank_up_down(self.UP))

    def bank_up_down(self, next_bank:int, direct:bool=False):
        if (next_bank < 0 and self._next_bank > 1) or (next_bank > 0 and self._next_bank < self._max_banks):
            if not direct:
                self._next_bank += next_bank

                print(self._next_bank)

                self._change_bank_start = time.time()

                if not self._is_change_bank:
                    self._thread_change_bank = Thread(target=self._change_bank)
                    self._thread_change_bank.start()

                self._display.alert(f"{self._next_bank:02d}--", "CHANGE BANK", True, self.TIME_WAIT_PRESET)
            else:
                self._current_bank += next_bank
                self.set_preset(self._current_bank * self._presets_per_bank - self._presets_per_bank)

    def preset_up_down(self, next_preset:int):
        if (next_preset < 0 < self._current_preset) or (next_preset > 0 and self._current_preset < self._max_presets):
            self.set_preset(self._current_preset + next_preset)

    def set_preset(self, preset: int):
        self._current_preset = preset
        self._current_bank = (self._current_preset // self._presets_per_bank) + 1
        self._next_bank = self._current_bank
        self._is_change_bank = False

        if self._on_preset_change:
            self._on_preset_change(self._current_preset)

        self._turn_off_all_leds()
        self._leds[self._current_preset % self._presets_per_bank].on()

        self._default_view()

    def bank_change_by_foot(self, foots):
        if len(foots) >= 2 and foots[0] == 'ft0' and foots[1] == 'ft1':
            self.bank_up_down(self.DOWN)
        elif len(foots) >= 2 and foots[0] == 'ft1' and foots[1] == 'ft2':
            self.bank_up_down(self.UP)

    def set_preset_by_index(self, foot_index: int)->None:
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

    def _stop_change_bank(self):
        if self._is_change_bank:
            self._is_change_bank = False
            self._thread_change_bank.join()

    def _default_view(self):
        self._display.hide_alert()
        presset_letter = ["A", "B", "C", "D", "E", "F"]

        text = f"{self._current_bank:02d}-{presset_letter[self._current_preset % self._presets_per_bank].upper()}"

        self._display.show(text, title='PRESET MODE', text_size=54)

    def set_on_preset_change(self, callback: Callable[[int], None]):
        self._on_preset_change = callback
