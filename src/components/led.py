import RPi.GPIO as GPIO

class Led:
    def __init__(self, pin):
        self._pin = pin  # Número do pino
        self._state = False  # Estado inicial do LED (desligado)
        GPIO.setmode(GPIO.BCM)  # Define o modo de numeração BCM
        GPIO.setup(self._pin, GPIO.OUT)  # Configura o pino como saída

    def on(self):
        """Liga o LED"""
        GPIO.output(self._pin, GPIO.HIGH)
        self._state = True

    def off(self):
        """Desliga o LED"""
        GPIO.output(self._pin, GPIO.LOW)
        self._state = False

    def toggle(self):
        """Alterna o estado do LED"""
        if self._state:
            self.off()
        else:
            self.on()

    def state(self):
        """Retorna o estado atual do LED (on ou off)"""
        return "on" if self._state else "off"

    def pin(self):
        """Retorna o número do pino associado ao LED"""
        return self._pin

    def cleanup(self):
        """Libera os recursos GPIO"""
        GPIO.cleanup(self._pin)