import threading
from typing import Callable

import RPi.GPIO as GPIO
import time

from src.components.pin import Pin


class Foot(Pin):
    """
    Classe para controle dos footswitchs
    """
    LONG_PRESS_THRESHOLD = 2

    def __init__(self, pin, name: str = '',
                 on_press: Callable[[str], None] = None,
                 on_press_2: Callable[[str], None] = None,
                 on_press_3: Callable[[str], None] = None,
                 on_release: Callable[[str, float], None] = None):
        """
        Classe Foot representa um footswitch com várias ações de pressão.

        :param pin: O número do pino GPIO ao qual o footswitch está conectado.
        :param name: O nome do footswitch para identificação.
        :param on_press: Função a ser chamada quando o footswitch é pressionado.
        :param on_press_2: Função a ser chamada quando o footswitch é pressionado por um curto período.
        :param on_press_3: Função a ser chamada quando o footswitch é pressionado por um longo período.
        :param on_release: Função a ser chamada quando o footswitch é liberado, recebendo a duração da pressão como argumento.
        """
        super().__init__(pin)

        self._name = name

        self.on_press = on_press
        self.on_press_2 = on_press_2
        self.on_press_3 = on_press_3
        self.on_release = on_release
        self.press_time = None
        self.is_pressed = False
        self.long_press_triggered = False
        self.running = True

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self._pin, GPIO.BOTH, callback=self._handle_press)
        self.monitor_thread = threading.Thread(target=self._monitor_press)
        self.monitor_thread.start()

    def _handle_press(self, channel):
        if GPIO.input(self._pin) == GPIO.LOW and not self.is_pressed:
            self.press_time = time.time()
            self.is_pressed = True
            self.long_press_triggered = False

            if self.on_press:
                self.on_press(self._name)
        elif GPIO.input(self._pin) == GPIO.HIGH and self.is_pressed:
            press_duration = time.time() - self.press_time
            if press_duration < self.LONG_PRESS_THRESHOLD:
                if self.on_press_2:
                    self.on_press_2(self._name)
            if self.on_release:
                self.on_release(self._name, press_duration)

            self.is_pressed = False
            self.press_time = None

    def _monitor_press(self):
        while self.running:
            if self.is_pressed:
                press_duration = time.time() - self.press_time
                if press_duration >= self.LONG_PRESS_THRESHOLD and not self.long_press_triggered:
                    if self.on_press_3:
                        self.on_press_3(self._name)
                    self.long_press_triggered = True
            time.sleep(0.1)

    def is_pressed(self):
        return self.is_pressed

    def get_duration(self):
        if self.is_pressed:
            return time.time() - self.press_time
        else:
            return 0

    def get_name(self):
        return self._name

    def cleanup(self):
        self.running = False
        self.monitor_thread.join()
        super().cleanup()
