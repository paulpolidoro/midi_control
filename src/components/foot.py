import RPi.GPIO as GPIO
import time

class Foot:
    def __init__(self, pin, callback_press=None, callback_release=None):
        self._pin = pin
        self._callback_press = callback_press  # Callback opcional para pressionar
        self._callback_release = callback_release  # Callback opcional para liberar
        self._press_time = 0  # Contador de tempo total pressionado
        self._last_press = None  # Momento da última pressão

        # Configuração do GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Ativa pull-up interno

        # Configuração de eventos
        GPIO.add_event_detect(self._pin, GPIO.BOTH, callback=self._event_handler, bouncetime=200)

    def _event_handler(self, channel):
        """Lida com os eventos de pressão e liberação do botão."""
        if GPIO.input(self._pin) == GPIO.LOW:  # Botão pressionado
            self._last_press = time.time()
            if self._callback_press:
                self._callback_press()
        else:  # Botão liberado
            if self._last_press:
                press_duration = time.time() - self._last_press  # Calcula tempo pressionado
                self._press_time += press_duration
                self._last_press = None
                if self._callback_release:
                    self._callback_release(press_duration)  # Passa o tempo ao callback
            else:
                if self._callback_release:
                    self._callback_release(0)

    def get_press_time(self):
        """Retorna o tempo total em que o botão ficou pressionado (em segundos)."""
        return round(self._press_time, 2)

    def reset_press_time(self):
        """Reseta o tempo de pressão acumulado."""
        self._press_time = 0

    def get_pin(self):
        """Retorna o número do pino associado ao botão."""
        return self._pin

    def cleanup(self):
        """Libera os recursos GPIO."""
        GPIO.cleanup(self._pin)