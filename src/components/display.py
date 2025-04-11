import os
import threading
import time

import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont


class Display:
    _display_width = 128
    _display_height = 64


    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.oled = SSD1306_I2C(self._display_width, self._display_height, i2c)

        self._text_blink_duration = 0.3

        self._is_alerting = False
        self._alert_text = ""
        self._alert_title = ""
        self._alert_start_time = 0
        self._alert_duration = 2
        self._default_view = None
        self._alert_thread = None
        self._alert_text_size = 50

        self._is_toasting = False
        self._toast_start_time = 0
        self._toast_thread = None
        self._toast_text = None
        self._toast_image = None
        self._toast_size = 20
        self._toast_duration = 2

    def show(self, text: str='', text_size:int=50, title: str='', title_size:int=12, invert: bool = False):
        font = "src/fonts/roboto/Roboto-Medium.ttf"
        text_font = ImageFont.truetype(font, text_size)
        title_font = ImageFont.truetype(font, title_size)

        if invert:
            background_fill = 1
            text_fill = 0
        else:
            background_fill = 0
            text_fill = 1

        image = Image.new("1", (self._display_width, self._display_height), background_fill)
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), title, font=title_font, fill=text_fill)

        text_bbox = draw.textbbox((0, 0), text, font=text_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        x = (self._display_width - text_width) // 2
        y = (self._display_height - text_height) // 2

        draw.text((x, y), text, font=text_font, fill=text_fill)

        self.oled.image(image)
        self.oled.show()

    def alert(self, text:str, title:str="", blink_text=False, duration:int=2, text_size:int=50, invert:bool=False):
        self._alert_text = text
        self._alert_title = title
        self._alert_duration = duration
        self._alert_start_time = time.time()
        self._alert_text_size = text_size

        if not self._is_alerting:
            self._alert_thread = threading.Thread(target=self._alert_task, args=[invert, blink_text])
            self._alert_thread.start()

    def _alert_task(self, invert=False, blink_text=False):
        self._is_alerting = True
        current_text = None
        current_title = None
        current_text_size = None

        while self._is_alerting and (time.time() - self._alert_start_time) < self._alert_duration:
            if blink_text:
                self.show(self._alert_text, title=self._alert_title, text_size=self._alert_text_size , invert=invert)
                time.sleep(self._text_blink_duration)
                self.show(title=self._alert_title, text_size=self._alert_text_size , invert=invert)
                time.sleep(self._text_blink_duration)
            else:
                if current_text != self._alert_text or current_title != self._alert_title or current_text_size != self._alert_text_size:
                    self.show(self._alert_text, title=self._alert_title, text_size=self._alert_text_size , invert=invert)

                    current_text = self._alert_text
                    current_title = self._alert_title
                    current_text_size = self._alert_text_size

            time.sleep(0.1)

        self._is_alerting = False

        if self._default_view:
            self._default_view()
        else:
            self.clear()

    def toast(self, text:str=None, image_path:str=None, size:int=20, duration:int=2, clear:bool=False):
        self.hide_alert()

        self._toast_text = text
        self._toast_image = image_path
        self._toast_size = size
        self._toast_duration = duration
        self._toast_start_time = time.time()

        if not self._is_toasting:
            self._toast_thread = threading.Thread(target=self._toast_task, args=[clear])
            self._toast_thread.start()

    def _toast_task(self, clear=False):
        self._is_toasting = True
        current_text = None
        current_image = None
        current_text_size = None

        while self._is_toasting and (time.time() - self._toast_start_time) < self._toast_duration:
            if clear:
                self._default_view()
                time.sleep(0.5)
                clear = False

            if self._toast_image:
                if current_image != self._toast_image or current_text_size != self._toast_size:
                    self._toast_show(image_path=self._toast_image, text_size=self._toast_size)
                    current_image = self._toast_image
                    current_text_size = self._toast_size

            elif self._toast_text:
                if current_text != self._toast_text or current_text_size != self._toast_size:
                    self._toast_show(text=self._toast_text, text_size=self._toast_size)
                    current_text = self._toast_text
                    current_text_size = self._toast_size



            time.sleep(0.1)

        self._is_toasting = False
        self._default_view()

    def _toast_show(self, text: str = None, image_path: str = None, text_size: int = 20):
        if not text and not image_path:
            return

        image = Image.new("1", (self._display_width, self._display_height))
        draw = ImageDraw.Draw(image)

        box_width = 120
        box_height = 48

        box_x = (self._display_width - box_width) / 2
        box_y = (self._display_height - box_height) / 2

        draw.rounded_rectangle((box_x, box_y, box_x + box_width, box_y + box_height), outline=255, fill=255, radius=4)

        if image_path and os.path.exists(image_path):
            try:
                img = self._config_image(image_path, text_size)
                if img:
                    img_x = int(box_x + (box_width - img.size[0]) / 2)
                    img_y = int(box_y + 2+ (box_height - img.size[1]) / 2)
                    image.paste(img, (img_x, img_y))
            except Exception as e:
                print(f"Erro ao carregar a imagem: {e}")
        elif text:
            font = ImageFont.truetype("src/fonts/roboto/Roboto-Black.ttf", text_size)
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            text_x = box_x + ((box_width - text_width) / 2)
            text_y = box_y - ((text_size / 4) - 2) + ((box_height - text_height) / 2)

            draw.text((text_x, text_y), text, font=font, fill=0)

        self.oled.image(image)
        self.oled.show()

    @staticmethod
    def _config_image(path: str, size:int):
        try:
            image = Image.open(path).convert("RGBA")

            new_image = Image.new("RGBA", image.size, (255, 255, 255, 255))  # Fundo branco
            new_image.paste(image, (0, 0), mask=image)

            mono_image = new_image.convert("1")

            mono_image_w, mono_image_h = mono_image.size

            width = int((size / mono_image_h) * mono_image_w)

            # Redimensiona a imagem
            imagem_redimensionada = mono_image.resize((width, size))

            return imagem_redimensionada
        except FileNotFoundError:
            print(f"Erro: O arquivo '{path}' não foi encontrado.")
            return None
        except Exception as e:
            print(f"Erro ao processar a imagem: {e}")
            return None

    def hide_alert(self):
        if self._is_alerting:
            self._is_alerting = False
            if self._alert_thread:
                self._alert_thread.join()

    def set_default_view(self, callback):
        self._default_view = callback

    def clear(self):
        self.oled.fill(0)
        self.oled.show()
