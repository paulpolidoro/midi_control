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
draw.rectangle((box_x, box_y, box_x + box_width, box_y + box_height), outline=255, fill=0)

# Define fonte e texto
font = ImageFont.load_default()
text = "Negativo"
text_width, text_height = font.getsize(text)  # Ajuste aqui para usar getsize

# Calcula posição para centralizar o texto
text_x = box_x + (box_width - text_width) // 2
text_y = box_y + (box_height - text_height) // 2

# Adiciona texto em negativo (invertido)
draw.text((text_x, text_y), text, font=font, fill=255)

# Exibe no display
oled.image(image)
oled.show()