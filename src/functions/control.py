from src.components.display import Display
from src.components.led import Led
from src.controllers.midi_controller import MidiController


class Control:
    def __init__(self, display: Display, led:Led=None):
        self._midi_controller = None
        self._led = led
        self._display = display
        self._is_enabled = False

    def enable(self):
        self._is_enabled = True

        if self._led is not None:
            self._led.on()

        self._display.alert("CTRL ON", text_size=24)


    def disable(self):
        self._is_enabled = False

        if self._led is not None:
            self._led.off()

        self._display.alert("CTRL OFF", text_size=24)


    def toggle(self):
        self._is_enabled = not self._is_enabled

        if self._led is not None:
            self._led.toggle()

        self._midi_controller.send_cc(0, 72, 127)
        self._display.alert("CTRL ON" if self._is_enabled else "CTRL OFF", text_size=24)

    def set_midi_controller(self, midi_controller: MidiController):
        self._midi_controller = midi_controller