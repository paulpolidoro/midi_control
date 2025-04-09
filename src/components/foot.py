from gpiozero import Button
from time import time, sleep
from threading import Thread, Lock

# Define um dicionário compartilhado para rastrear os estados dos botões
button_states = {}
lock = Lock()


def detect_multiple_press():
    with lock:
        pressed_buttons = [name for name, state in button_states.items() if state]
        return len(pressed_buttons) > 1


class Foot:
    LONG_PRESS_THRESHOLD = 1

    def __init__(self, pin, name):
        self.pin = pin
        self.name = name
        self.button = Button(pin)

        # Variáveis para callbacks individuais
        self._on_press = None
        self._on_short_press = None
        self._on_long_press = None
        self._on_release = None

        self._enabled_callbacks = True

        # Controle de tempo e estado
        self._press_start_time = None
        self._is_long_press_active = False

        # Adiciona o estado do botão ao dicionário compartilhado
        with lock:
            button_states[self.name] = False

        # Configuração de eventos
        self.button.when_pressed = self._handle_press
        self.button.when_released = self._handle_release

    def _handle_press(self):
        self._press_start_time = time()
        self._is_long_press_active = False

        with lock:
            button_states[self.name] = True

        Thread(target=self._delayed_press_callback, daemon=True).start()

        Thread(target=self._monitor_long_press, daemon=True).start()

    def _delayed_press_callback(self):
        sleep(0.1)  # Atraso de 100ms
        if not detect_multiple_press() and self._on_press:
            self._enabled_callbacks = True
            self._on_press()
        else:
            self._enabled_callbacks = False

    def _monitor_long_press(self):
        while self.button.is_pressed:
            press_duration = time() - self._press_start_time
            if press_duration > self.LONG_PRESS_THRESHOLD and not self._is_long_press_active:
                self._is_long_press_active = True

                if self._enabled_callbacks and self._on_long_press:
                    self._on_long_press()
            sleep(0.1)

    def _handle_release(self):
        press_duration = time() - self._press_start_time if self._press_start_time else 0

        if press_duration < self.LONG_PRESS_THRESHOLD and self._enabled_callbacks and self._on_short_press:
            self._on_short_press()

        if self._enabled_callbacks and self._on_release:
            self._on_release()

        with lock:
            button_states[self.name] = False

    def set_on_press(self, callback):
        self._on_press = callback

    def set_on_short_press(self, callback):
        self._on_short_press = callback

    def set_on_long_press(self, callback):
        self._on_long_press = callback

    def set_on_release(self, callback):
        self._on_release = callback
