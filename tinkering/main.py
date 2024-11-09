from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import numpy as np
import random
import os

from utils import set_pixel, is_white, is_black, random_boolean, Filters, find_nearest, get_distance, get_similar_color

image_name = "test5.png"
filter = Filters.GLITCHY_CONSTANT
fireflies_min_distance = 10
log_progress = True
animate = True

image = Image.open(image_name)

image = image.convert("RGB")
image_array = np.array(image)
height, width, channels = image_array.shape
total_pixels = width * height

modifications = []
processed_count = 0
frame_image_index = 0

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
              modifications.append((y, x, [255, 255, 0]))
          else:
            if random_boolean(True) and get_distance(find_nearest(modifications, x, y), (x, y)) >= fireflies_min_distance:
              modifications.append((y + 1, x, get_similar_color([255, 255, 0])))
              modifications.append((y, x, [255, 255, 0]))
    
    if log_progress:
      processed_count += 1
      processed_percentage = (processed_count / total_pixels) * 100
      if processed_percentage % 1 == 0:
        print(f"Processed {processed_percentage}%", end="\r")

print("\nModifying array " + str(len(modifications)))
if not os.path.exists("frames") and not os.path.isdir("frames"):
  os.makedirs("frames", exist_ok=True)

def process_modification(y, x, rgb):
  set_pixel(image_array, y, x, rgb)
  
  if animate:
    modified_image = Image.fromarray(image_array)
    modified_image.save(f"frames/{frame_image_index}")

with ThreadPoolExecutor() as executor:
  for (y, x, rgb) in modifications:
    executor.submit(process_modification, y, x, rgb)

print("Showing")
modified_image = Image.fromarray(image_array)
if not animate: modified_image.show()