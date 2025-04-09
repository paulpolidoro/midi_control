import threading
import time

import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont


class Display:
    width = 128
    height = 64
    text_blik_duration = 0.3
    _default_font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.oled = SSD1306_I2C(self.width, self.height, i2c)

        self._is_alerting = False
        self._alert_text = ""
        self._alert_title = ""
        self._alert_start_time = 0
        self._alert_duration = 2
        self._default_view = None
        self._alert_thread = None

    def show(self, text: str='', text_size:int=50, title: str='', title_size:int=12, invert: bool = False):
        text_font = ImageFont.truetype(self._default_font, text_size)
        title_font = ImageFont.truetype(self._default_font, title_size)

        if invert:
            background_fill = 1
            text_fill = 0
        else:
            background_fill = 0
            text_fill = 1

        image = Image.new("1", (self.width, self.height), background_fill)
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), title, font=title_font, fill=text_fill)

        text_bbox = draw.textbbox((0, 0), text, font=text_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2

        draw.text((x, y), text, font=text_font, fill=text_fill)

        self.oled.image(image)
        self.oled.show()

    def alert(self, text:str, title:str="", blink_text=False, duration:int=2, text_size:int=50, invert:bool=False):
        self._alert_text = text
        self._alert_title = title
        self._alert_duration = duration
        self._alert_start_time = time.time()

        if not self._is_alerting:
            self._alert_thread = threading.Thread(target=self._show_alert, args=[text_size, invert, blink_text])
            self._alert_thread.start()

    def _show_alert(self, text_size=50, invert=False, blink_text=False):
        self._is_alerting = True

        while self._is_alerting and (time.time() - self._alert_start_time) < self._alert_duration:
            if blink_text:
                self.show(self._alert_text, title=self._alert_title, text_size=text_size, invert=invert)
                time.sleep(self.text_blik_duration)
                self.show(title=self._alert_title, text_size=text_size, invert=invert)
                time.sleep(self.text_blik_duration)
            else:
                self.show(self._alert_text, title=self._alert_title, text_size=text_size, invert=invert)

            time.sleep(0.1)

        self._is_alerting = False

        if self._default_view:
            self._default_view()
        else:
            self.clear()

    def hide_alert(self):
        if self._is_alerting:
            self._is_alerting = False
            self._alert_thread.join()

    def set_default_view(self, callback):
        self._default_view = callback

    def clear(self):
        self.oled.fill(0)
        self.oled.show()
