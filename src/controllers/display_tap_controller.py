import threading
import time

from src.components.display import Display


class DisplayTapController(Display):
    def __init__(self):
        super().__init__()

        self._show_tap_duration = 2
        self._show_tap_start_time = 0
        self._tap_text = ''
        self._is_showing_tap = False

    def show_tap(self, number: int, duration: float = 2):
        self._show_tap_duration = duration

        if not (0 <= number <= 999):
            raise ValueError("O número deve estar entre 0 e 999.")

        self._tap_text = f"{number}"
        self._show_tap_start_time = time.time()

        if not self._is_showing_tap:
            thread = threading.Thread(target=self._show_tap)
            thread.start()

    def _show_tap(self):
        self._is_showing_tap = True
        while (time.time() - self._show_tap_start_time) < self._show_tap_duration:
            self.show_text_center(self._tap_text, title='TAP TEMPO')
            time.sleep(0.1)

        self._is_showing_tap = False

        self.show_preset(self._last_bank, self._last_preset)