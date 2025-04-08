import threading
import time
from typing import Callable, Optional

import RPi.GPIO as GPIO

from src.components.pin import Pin


class Foot(Pin):
    LONG_PRESS_THRESHOLD = 2

    def __init__(self, pin:int, controller, name: Optional[str] = None):
        super().__init__(pin)
        self._name = name
        self._controller = controller
        self.is_pressed = False
        self._press_time = 0
        self._disable_callback = False
        self._monitoring = False

        self.on_press:Optional[Callable[[str], None]] = None
        self.on_short_press:Optional[Callable[[str], None]] = None
        self.on_long_press:Optional[Callable[[str], None]] = None
        self.on_release:Optional[Callable[[str], None]] = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self._pin, GPIO.BOTH, callback=self._handle_press)

    def _handle_press(self, channel):
        if GPIO.input(self._pin) == GPIO.LOW:
            self._start_monitoring()
            self._press_time = time.time()
            self.is_pressed = True

            if not self._disable_callback and not self._controller.is_processing_multiple_press():
                self.on_press(self._name)
        elif GPIO.input(self._pin) == GPIO.HIGH:
            if (time.time() - self._press_time) < self.LONG_PRESS_THRESHOLD:
                if not self._disable_callback and not self._controller.is_processing_multiple_press():
                    self.on_short_press(self._name)

            self._stop_monitoring()
            self.is_pressed = False
            self._press_time = 0

            if not self._disable_callback and not self._controller.is_processing_multiple_press():
                self.on_release(self._name)

    def _monitor_press(self):
        self._monitoring = True

        while self._monitoring:
            if self.is_pressed:
                if (time.time() - self._press_time) >= self.LONG_PRESS_THRESHOLD:
                    if not self._disable_callback and not self._controller.is_processing_multiple_press():
                        self.on_long_press(self._name)
            time.sleep(0.1)

    def _start_monitoring(self):
        self.monitor_thread = threading.Thread(target=self._monitor_press)
        self.monitor_thread.start()

    def _stop_monitoring(self):
        self._monitoring = False
        self.monitor_thread.join()

    def is_pressed(self):
        return self.is_pressed

    def get_name(self)->str:
        return self._name

    def get_press_time(self)->float:
        return self._press_time

    def disable_callback(self):
        self._disable_callback = True

    def enable_callback(self):
        self._disable_callback = False

    def callback_state(self)->bool:
        return not self._disable_callback
