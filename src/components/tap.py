import time

from src.components.display import Display
from src.components.led import Led

def bpm_to_ms(bpm):
    return 60000 / bpm

class Tap:
    MIN_BPM = 40
    MAX_BPM = 250

    def __init__(self, led: Led, display: Display, initial_bpm: int = 70):
        self._led = led
        self._display = display
        self._bpm = initial_bpm
        self._last_tap_time = None
        self._tap_count = 0

    def tap(self, name:str=None):
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
                self._update_led(bpm)
                self._bpm = bpm
                self._display.show_tap(self._bpm)
            else:
                self._tap_count = 1

    def get_bpm(self):
        return self._bpm

    def reset(self):
        self._last_tap_time = None
        self._tap_count = 0

    def stop(self):
        self._led.stop_blinking()

    def _update_led(self, bpm):
        if bpm != self._bpm:
            self._led.blink(bpm_to_ms(bpm)/2, bpm_to_ms(bpm))