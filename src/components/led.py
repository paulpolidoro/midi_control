from typing import Optional

from gpiozero import LED
from time import sleep
from threading import Thread

from src.components.pin import Pin


class Led(Pin):
    def __init__(self, pin: int):
        super().__init__(pin)
        self._led:LED = LED(pin)

        self.blink_thread:Optional[Thread] = None
        self._blinking:bool = False
        self._blink_time_on:float = 1000
        self._blink_time_off:float = 1000
        self._on:bool = False

    def on(self):
        if not self._on:
            self._led.on()
            self._on = True

    def off(self):
        if self._on or self._blinking:
            self.stop_blinking()
            self._led.off()
            self._on = False

    def toggle(self):
        if self._on:
            self._led.off()
        else:
            self._led.on()

        self._on = not self._on

    def is_on(self):
        return self._on
    
    def close(self):
        self._led.off()
        self._led.close()

    def blink(self, on_time_ms: float, off_time_ms: float):
        self._blink_time_on = on_time_ms
        self._blink_time_off = off_time_ms

        def _blink():
            while self._blinking:
                self.toggle()
                sleep(self._blink_time_on / 1000.0)

        if not self._blinking:
            self._blinking = True
            self.blink_thread = Thread(target=_blink, daemon=True)
            self.blink_thread.start()

    def stop_blinking(self):
        if self._blinking:
            self._blinking = False
            if self.blink_thread:
                self.blink_thread.join()