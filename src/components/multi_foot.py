import threading
import time
from typing import Callable, Optional

from src.components.foot import button_states as foot_states


class MultiFoot:
    LONG_PRESS_THRESHOLD = 1

    def __init__(self):
        self._start_press_time_AB = None
        self._is_pressed_AB = False
        self._is_long_pressed_AB = False

        self.foots = [
            {'ft1': 'ft0',
             'ft2': 'ft1',
             'start_time': 0.0,
             'pressed': False,
             'long_pressed': False},

            {'ft1': 'ft1',
             'ft2': 'ft2',
             'start_time': 0.0,
             'pressed': False,
             'long_pressed': False},

            {'ft1': 'ft2',
             'ft2': 'ft3',
             'start_time': 0.0,
             'pressed': False,
             'long_pressed': False}
        ]

        self._on_press_AB:Optional[Callable[[], None]] = None
        self._on_short_AB:Optional[Callable[[], None]] = None
        self._on_long_AB:Optional[Callable[[], None]] = None
        self._on_release_AB:Optional[Callable[[], None]] = None

        self._on_press_BC:Optional[Callable[[], None]] = None
        self._on_short_BC:Optional[Callable[[], None]] = None
        self._on_long_BC:Optional[Callable[[], None]] = None
        self._on_release_BC:Optional[Callable[[], None]] = None

        self._on_press_CD:Optional[Callable[[], None]] = None
        self._on_short_CD:Optional[Callable[[], None]] = None
        self._on_long_CD:Optional[Callable[[], None]] = None
        self._on_release_CD:Optional[Callable[[], None]] = None

        self._monitoring = True
        self._thread = threading.Thread(target=self._monitor_multi_press)
        self._thread.start()

    def _monitor_multi_press(self):
        while self._monitoring:
            pressed_buttons = [name for name, state in foot_states.items() if state]

            self._handler_multi_press(pressed_buttons, 0, self._on_press_AB, self._on_short_AB, self._on_long_AB, self._on_release_AB)
            self._handler_multi_press(pressed_buttons, 1, self._on_press_BC, self._on_short_BC, self._on_long_BC, self._on_release_BC)
            self._handler_multi_press(pressed_buttons, 2, self._on_press_CD, self._on_short_CD, self._on_long_CD, self._on_release_CD)

            time.sleep(0.1)

    def _handler_multi_press(self, pressed_foots, index, on_press=None, on_short=None, on_long=None, on_release=None):
        foot = self.foots[index]

        if foot['ft1'] in pressed_foots and foot['ft2'] in pressed_foots:
            if not foot['pressed']:
                foot['start_time'] = time.time()
                foot['pressed'] = True

                if on_press:
                    on_press()
            else:
                if time.time() - foot['start_time'] >= self.LONG_PRESS_THRESHOLD and not foot['long_pressed']:
                    if on_long:
                        on_long()

                    foot['long_pressed'] = True

        else:
            if foot['pressed']:

                if time.time() - foot['start_time'] < self.LONG_PRESS_THRESHOLD:
                    print('short pressed multi')
                    if on_short:
                        on_short()

                foot['start_time'] = 0.0
                foot['pressed'] = False
                foot['long_pressed'] = False

                if on_release:
                    on_release()

    # Sets dos calbacks par A + B
    def set_on_press_ab(self, callback):
        self._on_press_AB = callback

    def set_on_short_press_ab(self, callback):
        self._on_short_AB = callback

    def set_on_long_press_ab(self, callback):
        self._on_long_AB = callback

    def set_on_release_ab(self, callback):
        self._on_release_AB = callback

    # Sets dos calbacks par B + C
    def set_on_press_bc(self, callback):
        self._on_press_BC = callback

    def set_on_short_press_bc(self, callback):
        self._on_short_BC = callback

    def set_on_long_press_bc(self, callback):
        self._on_long_BC = callback

    def set_on_release_bc(self, callback):
        self._on_release_BC = callback

    # Sets dos calbacks par C + D
    def set_on_press_cd(self, callback):
        self._on_press_CD = callback

    def set_on_short_press_cd(self, callback):
        self._on_short_CD = callback

    def set_on_long_press_cd(self, callback):
        self._on_long_CD = callback

    def set_on_release_cd(self, callback):
        self._on_release_CD = callback

    def callback_is_in_use(self, callback_name: str):
        try:
            return getattr(self, f'_{callback_name}') is not None
        except AttributeError:
            return None

    def callback_release(self, callback_name: str):
        try:
            getattr(self, f'_{callback_name}')
            setattr(self, f'_{callback_name}', True)
            return True
        except AttributeError:
            return False

    def callback_release_all(self):
        self._on_press_AB = None
        self._on_short_AB = None
        self._on_long_AB = None
        self._on_release_AB = None

        self._on_press_BC = None
        self._on_short_BC = None
        self._on_long_BC = None
        self._on_release_BC = None

        self._on_press_CD = None
        self._on_short_CD = None
        self._on_long_CD = None
        self._on_release_CD = None

    def stop(self):
        self._monitoring = False
        self._thread.join()