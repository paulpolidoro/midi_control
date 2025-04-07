import time

import RPi.GPIO as GPIO

from src.components.tap import Tap
from src.hardware import pins
from src.components.foot import Foot
from src.components.led import Led

def main():
    led_power = Led(pins.LED_POWER)
    led_power.on()

    tap = Tap(Led(pins.LED_TAP))

    foot_ctl = Foot(pins.FOOT_4, on_press=tap.tap)

    try:
        while True:
            time.sleep(0.1)
            continue
    except KeyboardInterrupt:
        print("Programa finalizado com sucesso!")
    finally:
        GPIO.cleanup()

if __name__ =="__main__":
    main()