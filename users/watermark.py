from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os, sys


class Watermark:

    def add_watermark(image, watermark, opacity=0.5):
        """Метод добавляет водяной знак на картинку"""

        watermark = watermark.convert('RGBA')
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)

        layer = Image.new('RGBA', image.size, (0,0,0,0))
        layer.paste(watermark, (0, image.size[1]//2))

        return Image.composite(layer, image, layer)