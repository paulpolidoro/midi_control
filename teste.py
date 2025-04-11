import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

display_width, display_height = 128, 64

# Configura o I2C e inicializa o display
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(display_width, display_height, i2c)

# Limpa o display
oled.fill(0)
oled.show()

# Cria uma imagem para desenhar
width = oled.width
height = oled.height
image = Image.new("1", (width, height))

draw = ImageDraw.Draw(image)

# Desenha um quadro central

box_width = 112
box_height = 32

box_x = (display_width - box_width) /2
box_y = (display_height - box_height) /2


draw.rectangle((box_x, box_y, box_x + box_width, box_y + box_height), outline=255, fill=255)

# Define fonte e texto
font = ImageFont.truetype("src/fonts/roboto/Roboto-Bold.ttf", 16)
text = "NEGATIVO"

bbox = font.getbbox(text)
text_width = bbox[2] - bbox[0]  # Largura do texto
text_height = bbox[3] - bbox[1]

print(f"Largura: {text_width}, Altura: {text_height}")


# Teste para centralizar texto com aproximação manual
# Teste para centralizar texto levando em conta a posição do retângulo
text_x = box_x + (box_width - text_width) / 2  # Centraliza dentro do retângulo e considera deslocamento
text_y = box_y + (box_height - text_height) / 2  # Centraliza dentro do retângulo e considera deslocamento

# Adiciona texto em negativo (invertido)
draw.text((text_x, text_y), text, font=font, fill=0)

# Exibe no display
oled.image(image)
oled.show()