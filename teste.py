import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# Configura o I2C e inicializa o display
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(128, 64, i2c)

# Limpa o display
oled.fill(0)
oled.show()

# Cria uma imagem para desenhar
width = oled.width
height = oled.height
image = Image.new("1", (width, height))

draw = ImageDraw.Draw(image)

# Desenha um quadro central
box_x = 32
box_y = 16
box_width = 64
box_height = 32
draw.rectangle((box_x, box_y, box_x + box_width, box_y + box_height), outline=255, fill=255)

# Define fonte e texto
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
text = "NEGATIVO"

# Teste para centralizar texto com aproximação manual
text_x = box_x + 8  # Ajuste baseado na posição desejada
text_y = box_y + 12

# Adiciona texto em negativo (invertido)
draw.text((text_x, text_y), text, font=font, fill=0)

# Exibe no display
oled.image(image)
oled.show()