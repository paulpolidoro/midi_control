from src.components.display import Display
from src.components.led import Led


class Control:
    def __init__(self, display: Display, led:Led=None):
        self._led = led
        self._display = display
        self._is_enabled = False

    def enable(self):
        self._is_enabled = True

        if self._led is not None:
            self._led.on()

        self._display.show_ctrl_status(self._is_enabled)


    def disable(self):
        self._is_enabled = False

        if self._led is not None:
            self._led.off()

        self._display.show_ctrl_status(self._is_enabled)


    def toggle(self):
        self._is_enabled = not self._is_enabled

        if self._led is not None:
            self._led.toggle()

        self._display.show_ctrl_status(self._is_enabled)

