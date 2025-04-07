import RPi.GPIO as GPIO
from src.hardware import pins
from src.components.foot import Foot
from src.components.led import Led


def main():
    FOOTS = [
        Foot(pins.FOOT_1),
        Foot(pins.FOOT_2),
        Foot(pins.FOOT_3),
        Foot(pins.FOOT_4)
    ]

    LEDS = [
        Led(pins.LED_1),
        Led(pins.LED_2),
        Led(pins.LED_3),
        Led(pins.LED_4)
    ]



    try:
        while True:

            continue
    except KeyboardInterrupt:
        print("Programa finalizado com sucesso!")
    finally:
        GPIO.cleanup()

if __name__ =="__main__":
    main()