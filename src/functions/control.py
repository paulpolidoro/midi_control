from typing import Optional, Callable

from src.components.display import Display
from src.components.led import Led
from src.controllers.midi_controller import MidiController


class Control:
    def __init__(self, display: Display, led:Led=None):
        self._led:Led = led
        self._display:Display = display
        self._is_enabled:bool = False

        self._on_enable:Optional[Callable[[], None]]=None
        self._on_disable:Optional[Callable[[],None]]=None
        self._on_toggle:Optional[Callable[[],None]]=None

    def enable(self):
        if not self._is_enabled:
            self._is_enabled = True

            if self._led is not None:
                self._led.on()

            self._display.alert("CTRL ON", text_size=24, duration=2)

            if self._on_enable:
                self._on_enable()

    def disable(self):
        if self._is_enabled:
            self._is_enabled = False

            if self._led is not None:
                self._led.off()

            self._display.alert("CTRL OFF", text_size=24, duration=2)

            if self._on_disable:
                self._on_disable()

    def toggle(self):
        self._is_enabled = not self._is_enabled

        if self._led is not None:
            self._led.toggle()

        self._display.toast("CTRL ON" if self._is_enabled else "CTRL OFF", size=24, duration=2)

        if self._on_toggle:
            self._on_toggle()

    def set_on_enable(self, on_enable:Callable[[],None]):
        self._on_enable = on_enable

    def set_on_disable(self, on_disable:Callable[[],None]):
        self._on_disable = on_disable

    def set_on_toggle(self, on_toggle:Callable[[],None]):
        self._on_toggle = on_toggle
