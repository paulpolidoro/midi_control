import time

from src.components.display import Display
from src.components.led import Led
from src.controllers.midi_controller import MidiController

def bpm_to_cc(bpm):
    data1 = 0

    if bpm > 127:
        data1 = 1

        data2 =  bpm - 128
    else:
        data2 = bpm

    return [data1, min(data2, 127)]

def bpm_to_ms(bpm):
    return 60000 / bpm

class Tap:
    MIN_BPM = 40
    MAX_BPM = 250

    def __init__(self, led: Led, display: Display, initial_bpm: int = 60):
        self._led = led
        self._midi_controller = None
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
        self._update_led(bpm)
        self._bpm = bpm

    def _update_led(self, bpm):
        if self._midi_controller:
            cc =  bpm_to_cc(bpm)
            self._midi_controller.send_cc(0, 73, cc[0])
            self._midi_controller.send_cc(0, 74, cc[1])
        if bpm != self._bpm:
            self._led.blink(bpm_to_ms(bpm)/2, bpm_to_ms(bpm)/2)

    def set_midi_controller(self, midi_controller:MidiController):
        self._midi_controller = midi_controller
