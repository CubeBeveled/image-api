import random
from PIL import Image
import numpy as np

from utils import set_pixel, is_white, is_black, random_boolean, Filters, find_nearest, get_distance

image_name = "test2.jpg"
filter = Filters.FIREFLIES
fireflies_min_distance = 10

image = Image.open(image_name)

image = image.convert("RGB")
image_array = np.array(image)
height, width, channels = image_array.shape

modifications = []

# Arrays start at 0
height -= 1
width -= 1

print("Checking array")
for y in range(height):
  for x in range(width):
    pixel_position = (y, x)
    pixel_rgb = image_array[y, x]
    
    if y + 1 < height and x + 1 < width:
      if filter == Filters.GLITCHY_RANDOM_DOWN:
        if random_boolean(True):
          modifications.append((y, x, image_array[y - 2, x]))
          modifications.append((y + 2, x, pixel_rgb))

      elif filter == Filters.GLITCHY_CONSTANT_DOWN_ON_WHITE:
        if is_white(pixel_rgb):
          modifications.append((y, x, image_array[y - 1, x]))
          modifications.append((y + 1, x, pixel_rgb))

      elif filter == Filters.GLITCHY_CONSTANT_DOWN_ON_BLACK:
        if is_black(pixel_rgb):
          modifications.append((y, x, image_array[y - 1, x]))
          modifications.append((y + 1, x, pixel_rgb))

      elif filter == Filters.GLITCHY_CONSTANT:
        modifications.append((y, x, image_array[y - 1, x]))
        modifications.append((y + 1, x, pixel_rgb))
      
      elif filter == Filters.RANDOM_PIXELS:
        new_x = random.randint(0, width)
        new_y = random.randint(0, height), 
        
        modifications.append((y, x, image_array[y - 1, x]))
        modifications.append((new_y, new_x, pixel_rgb))
      
      elif filter == Filters.FIREFLIES:
        if is_black(pixel_rgb, 50):
          if modifications == []:
            if random_boolean(True):
              modifications.append((y, x, [255 - (pixel_rgb[0] / 2), 255 - (pixel_rgb[1] / 2), 0]))
          elif get_distance(find_nearest(modifications, x, y), (x, y)) <= fireflies_min_distance:
            modifications.append((y, x, [255 - (pixel_rgb[0] / 2), 255 - (pixel_rgb[1] / 2), 0]))
          else:
            modifications.append((y, x, [255, 0, 0]))

print("Modifying array " + str(len(modifications)))
for (y, x, rgb) in modifications:
  set_pixel(image_array, y, x, rgb)

print("Showing")
modified_image = Image.fromarray(image_array)
modified_image.show()