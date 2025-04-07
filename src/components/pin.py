import RPi.GPIO as GPIO

class Pin:
    def __init__(self, pin):
        """
        Classe Pin funções básicas dos pinos físicos da placa.
        :param pin: Número do pino selecionado.
        """
        self._pin = pin

    def get_pin(self):
        """
        Retorna o número do pino.
        :return: int
        """
        return self._pin

    def cleanup(self):
        """
        Limpa a utilização do pino.
        """
        GPIO.cleanup(self._pin)