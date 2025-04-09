import threading
import time

import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont


class Display:
    width = 128
    height = 64

    def __init__(self):
        self._last_bank = 1
        self._last_preset = 'A'
        self._is_bank_change_wait = False
        self._bank_change_wait_start = None
        self._time_wait_preset = 4
        self._next_bank = 0

        self._show_tap_duration = 2
        self._show_tap_start_time = 0
        self._tap_text = ''
        self._is_showing_tap = False

        self._show_ctrl_duration = 1
        self._show_ctrl_status_start_time = 0
        self._is_showing_ctrl = False
        self._show_ctrl_text = ''

        i2c = busio.I2C(board.SCL, board.SDA)
        self.oled = SSD1306_I2C(self.width, self.height, i2c)

    def clear(self):
        self.oled.fill(0)
        self.oled.show()

    def show_preset(self, bank: int, preset: str):
        self._last_bank = bank
        self._last_preset = preset

        if self._is_bank_change_wait:
            self._is_bank_change_wait = False

        text = f"{self._last_bank:02d}-{self._last_preset.upper()}"

        self.show_text_center(text, title='PRESET MODE')

    def bank_change_wait(self, bank: int):
        self._bank_change_wait_start = time.time()

        self._next_bank = bank

        if not self._is_bank_change_wait:
            self._is_bank_change_wait = True
            thread = threading.Thread(target=self._bank_change_wait)
            thread.start()

    def _bank_change_wait(self):
        while self._is_bank_change_wait and (time.time() - self._bank_change_wait_start) < self._time_wait_preset:
            text = f"{self._next_bank:02d}--"

            self.show_text_center(text, title='CHANGE BANK')
            time.sleep(0.3)
            self.show_text_center(title='CHANGE BANK')
            time.sleep(0.3)

        self._is_bank_change_wait = False
        self.show_preset(self._last_bank, self._last_preset)

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

    def show_ctrl_status(self, enabled):
        if enabled:
            self._show_ctrl_text = "CTRL ON"
        else:
            self._show_ctrl_text = "CTRL OFF"

        self._show_ctrl_status_start_time = time.time()

        if not self._is_showing_ctrl:
            thread = threading.Thread(target=self._show_ctrl_status)
            thread.start()

    def _show_ctrl_status(self):
        self._is_showing_ctrl = True

        while self._is_showing_ctrl and (time.time() - self._show_ctrl_status_start_time) < self._show_ctrl_duration:
            self.show_text_center(self._show_ctrl_text, text_size=24)
            time.sleep(0.1)

        self._is_showing_ctrl = False
        self.show_preset(self._last_bank, self._last_preset)


    def show_text_center(self, text: str='', text_size:int=50, title: str='', title_size:int=12, invert: bool = False):
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", text_size)
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", title_size)

        # Define a cor de fundo e do texto com base no parâmetro `invert`
        if invert:
            background_fill = 1  # Fundo branco
            text_fill = 0  # Texto preto
        else:
            background_fill = 0  # Fundo preto
            text_fill = 1  # Texto branco

        # Cria uma imagem com a cor de fundo configurada
        image = Image.new("1", (self.width, self.height), background_fill)
        draw = ImageDraw.Draw(image)

        # Desenha o título no topo da tela à esquerda
        draw.text((0, 0), title, font=title_font, fill=text_fill)

        # Centraliza o texto no centro da tela
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2

        # Desenha o texto no centro da tela
        draw.text((x, y), text, font=font, fill=text_fill)

        # Exibe a imagem no display
        self.oled.image(image)
        self.oled.show()
