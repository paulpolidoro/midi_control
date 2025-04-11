import time
from typing import Callable, Optional
from src.components.display import Display
from src.components.led import Led

class Tap:
    MIN_BPM = 40
    MAX_BPM = 250

    def __init__(self, led: Led, display: Display, initial_bpm: int = 60):
        self._led:Led = led
        self._display = display
        self._bpm = initial_bpm
        self._last_tap_time = None
        self._tap_count = 0

        self._on_tap:Optional[Callable[[int],None]]=None
        self._on_set_tap:Optional[Callable[[int],None]]=None

    def tap(self):
        current_time = time.time()

        if self._last_tap_time is None:
            self._last_tap_time = current_time
            self._tap_count = 1
        else:
            interval = current_time - self._last_tap_time
            self._last_tap_time = current_time
            bpm = round(60 / interval)

            if bpm > 20:
                self._tap_count += 1
                bpm = max(self.MIN_BPM, min(self.MAX_BPM, round(60 / interval)))

                if self._on_tap:
                    self._on_tap(bpm)

                self._update_led(bpm)
                self._bpm = bpm
                self._display.alert(str(self._bpm), "TAP TEMPO")
            else:
                self._tap_count = 1

    def get_bpm(self):
        return self._bpm

    def reset(self):
        self._last_tap_time = None
        self._tap_count = 0

    def stop(self):
        self._led.stop_blinking()

    def set_tap(self, bpm):
        if self._on_set_tap:
            self._on_set_tap(bpm)

        self._update_led(bpm)
        self._bpm = bpm

    def _update_led(self, bpm:int):
        if bpm != self._bpm:
            ms = (60000/bpm)
            self._led.blink(ms, ms)

    def set_on_tap(self, on_tap:Callable[[int],None]):
       self._on_tap = on_tap

    def set_on_set_tap(self, on_set_tap:Callable[[int],None]):
        self._on_set_tap = on_set_tap
