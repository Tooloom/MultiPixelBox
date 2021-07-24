import os
from sys import platform
from PIL import Image
import numpy as np
import MultiPixelBox

image_count = 0
progress = 0
file_name = ''
done = True

# ---------------------------------- Selecting a special letter for the current OS -------------------------------------
if platform == "linux" or platform == "linux2":
    sp_letter = '/'
elif platform == "darwin" or platform == "win32":
    sp_letter = '\\'


# ---------------------------------- Image searching and transform function calling ------------------------------------
def multiplier(path_from, path_to, scale):
    global image_count, progress, done, file_name

    try:
        for i in os.listdir(path_from):
            if not os.path.isdir(path_from + sp_letter + i):
                image_count += 1

        for i in os.listdir(path_from):
            if not os.path.isdir(path_from + sp_letter + i):
                file_name = i
                transform(path_from + sp_letter + i, scale, i, path_to)
                progress += 1

    except OSError:
        print('Path error')
        done = False
        image_count = 0
        progress = 0
    done = False
    image_count = 0
    progress = 0


# ------------------------------------------- All given images transforming --------------------------------------------
def transform(path_from, scale, name, path_to):
    try:
        image = Image.open(path_from)
        width = image.size[0]
        height = image.size[1]
        pixels = image.load()
        image_format = image.format.lower()
        image_mode = image.mode
    except ValueError:
        return 'File error'

    if image_mode == 'RGB':
        channels = 3
    elif image_mode == 'RGBA':
        channels = 4

    w, h = width * scale, height * scale
    data = np.zeros((h, w, channels), dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            data[i * scale:i * scale + scale, j * scale:j * scale + scale] = pixels[j, i]

    image = Image.fromarray(data, image_mode)
    image.save(f'{path_to}{sp_letter}{name}.{image_format}')

    return f'{name}.{image_format} is successful scaled!'
