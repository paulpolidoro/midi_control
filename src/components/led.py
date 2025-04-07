import RPi.GPIO as GPIO
import time
import threading

from src.components.pin import Pin


class Led(Pin):
    """
    Classe para controle os LEDs.

    """
    LED_ON = True
    LED_OFF = False

    def __init__(self, pin: int):
        """
        Constructor.
        :param pin
        """
        super().__init__(pin)

        self.blink_thread = None
        self._state = False
        self._blinking = False
        self._on = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.OUT)

    def on(self):
        """
        Acende o LED
        """
        GPIO.output(self._pin, GPIO.HIGH)
        self._on = True

    def off(self):
        """
        Apaga o LED
        """
        GPIO.output(self._pin, GPIO.LOW)
        self._on = False

    def toggle(self):
        """
        Liga ou desliga o LED de acordo com o estado atual
        """
        if self._state:
            self.off()
        else:
            self.on()

    def is_on(self):
        """
        Retorna se o LED está ligado ou desligado.
        :return: Boolean
        """
        return self._on

    def blink(self, on_time_ms: int, off_time_ms: int):
        """
        Faz o LED piscar no tempo definido.
        :param on_time_ms: Tempo em milissegundos que o LED ficará aceso
        :param off_time_ms: Tempo em milissegundos que o LED ficará desligado
        """
        self._blinking = True

        def _blink():
            while self._blinking:
                self.on()
                time.sleep(on_time_ms / 1000.0)
                self.off()
                time.sleep(off_time_ms / 1000.0)

        self.blink_thread = threading.Thread(target=_blink)
        self.blink_thread.start()

    def stop_blinking(self):
        """
        Faz o LED parar de piscar
        """
        self._blinking = False
        self.blink_thread.join()
