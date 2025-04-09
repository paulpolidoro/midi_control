from gpiozero import LED
from time import sleep
from threading import Thread

class Led:
    def __init__(self, pin: int):
        self.pin = pin
        self.led = LED(pin)

        self.blink_thread = None
        self._blinking = False
        self._blink_time_on = 1000
        self._blink_time_off = 1000
        self._on = False

    def on(self):
        """Liga o LED."""
        self.led.on()
        self._on = True

    def off(self):
        """Desliga o LED."""
        self.led.off()
        self._on = False

    def toggle(self):
        """Altera o estado do LED (liga/desliga)."""
        if self._on:
            self.off()
        else:
            self.on()

    def is_on(self):
        """Verifica se o LED está ligado."""
        return self._on

    def blink(self, on_time_ms: int, off_time_ms: int):
        """Pisca o LED com os tempos definidos."""
        self._blink_time_on = on_time_ms
        self._blink_time_off = off_time_ms

        if not self._blinking:
            self._blinking = True

            def _blink():
                while self._blinking:
                    self.on()
                    sleep(self._blink_time_on / 1000.0)
                    self.off()
                    sleep(self._blink_time_off / 1000.0)

            self.blink_thread = Thread(target=_blink)
            self.blink_thread.start()

    def stop_blinking(self):
        if self._blinking:
            self._blinking = False
            if self.blink_thread:
                self.blink_thread.join()