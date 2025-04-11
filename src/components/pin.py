import RPi.GPIO as GPIO

class Pin:
    FOOT_0 = 17
    FOOT_1 = 27
    FOOT_2 = 22
    FOOT_3 = 23

    LED_POWER = 24
    LED_TAP = 12
    LED_0 = 5
    LED_1 = 6
    LED_2 = 13
    LED_3= 19

    def __init__(self, pin:int):
        self._pin = pin

    def get_pin(self):
        return self._pin

    def cleanup(self):
        GPIO.cleanup(self._pin)