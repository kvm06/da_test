from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os, sys
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile


def add_watermark(user_picture: InMemoryUploadedFile, watermark_path: str) -> InMemoryUploadedFile:
    image = Image.open(user_picture).convert('RGB')
    watermark = Image.open(watermark_path)

    # resize too big pictures
    if image.width > 512:
        image = image.resize((512, 512 * image.height // image.width))

    im_height, wm_height = image.size[1], watermark.size[1]
    image.paste(watermark, (0, im_height - wm_height), mask=watermark)
    output = BytesIO()
    image.save(output, format='JPEG', quality=95)
    image.close()
    watermark.close()
    output.seek(0)

    return InMemoryUploadedFile(output, None, user_picture.name, 'image/jpeg', None, None)
