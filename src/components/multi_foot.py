import threading
import time

from src.components.foot import button_states as foot_states


class MultiFoot:
    LONG_PRESS_THRESHOLD = 2

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

        self._monitoring = True
        self._thread = threading.Thread(target=self._monitor_multi_press)
        self._thread.start()


    def _monitor_multi_press(self):
        while self._monitoring:
            pressed_buttons = [name for name, state in foot_states.items() if state]

            self._handler_multi_press(pressed_buttons, 0, self._on_press_AB, self._on_short_AB, self._on_long_AB, self._on_release_AB)
            self._handler_multi_press(pressed_buttons, 1, self._on_press_BC, self._on_short_BC, self._on_long_BC, self._on_release_BC)
            self._handler_multi_press(pressed_buttons, 2, self._on_press_CD, self._on_short_CD, self._on_long_CD, self._on_release_CD)


            # if 'ft0' in pressed_buttons and 'ft1' in pressed_buttons:
            #     if not self._is_pressed_AB:
            #         self._start_press_time_AB = time.time()
            #         self._is_pressed_AB = True
            #         self.press()
            #     else:
            #         if time.time() - self._start_press_time_AB >= self.LONG_PRESS_THRESHOLD and not self._is_long_pressed_AB:
            #             self.long_press()
            #             self._is_long_pressed_AB = True
            #
            # else:
            #     if self._is_pressed_AB:
            #
            #         if time.time() - self._start_press_time_AB < self.LONG_PRESS_THRESHOLD:
            #             self.short_press()
            #
            #         self._start_press_time_AB = None
            #         self._is_pressed_AB = False
            #         self._is_long_pressed_AB = False
            #         self.release()

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

    def stop(self):
        self._monitoring = False
        self._thread.join()