import threading
import time
from typing import List, Callable, Optional
from src.components.foot import Foot

class FootController:
    LONG_PRESS_THRESHOLD = 2
    SIMULTANEOUS_PRESS_THRESHOLD = 0.5

    def __init__(self, foots: List[Foot]):
        self.foots = foots
        self._monitoring = False
        self._processing_multi_press = False
        self._multi_press_called = False
        self._multi_long_press_called = False
        self.on_multi_press: Optional[Callable[[List[str]], None]] = None
        self.on_multi_short_press: Optional[Callable[[List[str]], None]] = None
        self.on_multi_long_press: Optional[Callable[[List[str]], None]] = None
        self.on_multi_release: Optional[Callable[[List[str]], None]] = None

    def _monitor_foots(self):
        self._monitoring = True

        while self._monitoring:
            pressed_foots = [foot for foot in self.foots if foot.is_pressed]
            if len(pressed_foots) > 1:
                press_times = [foot.get_press_time() for foot in pressed_foots]
                if max(press_times) - min(press_times) <= self.SIMULTANEOUS_PRESS_THRESHOLD:
                    self._processing_multi_press = True
                    self._disable_all_callbacks()

                    if not self._multi_press_called and self.on_multi_press:
                        self.on_multi_press([foot.get_name() for foot in pressed_foots])
                        self._multi_press_called = True

                    if all((time.time() - foot.get_press_time()) >= self.LONG_PRESS_THRESHOLD for foot in pressed_foots):
                        if not self._multi_long_press_called and self.on_multi_long_press:
                            self.on_multi_long_press([foot.get_name() for foot in pressed_foots])
                            self._multi_long_press_called = True

                    self._processing_multi_press = False

            released_foots = [foot for foot in self.foots if not foot.is_pressed]
            if len(released_foots) > 1:
                if all((time.time() - foot.get_press_time()) < self.LONG_PRESS_THRESHOLD for foot in released_foots):
                    if self.on_multi_short_press:
                        self.on_multi_short_press([foot.get_name() for foot in released_foots])
                if self.on_multi_release:
                    self.on_multi_release([foot.get_name() for foot in released_foots])
                self._multi_press_called = False
                self._multi_long_press_called = False

            time.sleep(0.1)

    def _disable_all_callbacks(self):
        for foot in self.foots:
            foot.disable_callback()

    def _enable_all_callbacks(self):
        for foot in self.foots:
            foot.enable_callback()

    def start_monitoring(self):
        self._monitor_thread = threading.Thread(target=self._monitor_foots)
        self._monitor_thread.start()

    def stop_monitoring(self):
        self._monitoring = False
        self._monitor_thread.join()

    def set_multi_press_callback(self, callback: Callable[[List[str]], None]):
        self.on_multi_press = callback

    def set_multi_short_press_callback(self, callback: Callable[[List[str]], None]):
        self.on_multi_short_press = callback

    def set_multi_long_press_callback(self, callback: Callable[[List[str]], None]):
        self.on_multi_long_press = callback

    def set_multi_release_callback(self, callback: Callable[[List[str]], None]):
        self.on_multi_release = callback

    def is_processing_multi_press(self):
        return self._processing_multi_press