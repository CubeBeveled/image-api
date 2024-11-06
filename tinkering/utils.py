from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import Enum
import random
import math

def get_distance(point1, point2):
  x1, y1 = point1
  x2, y2 = point2
  distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
  return distance

def set_pixel(image_array, y, x, rgb):
  image_array[y, x] = rgb
  
def get_pixel(image_array, y, x):
  return image_array[y, x]

def is_black(rgb, threshold = 20):
  return rgb[0] < threshold and rgb[1] < threshold and rgb[2] < threshold

def is_white(rgb):
  return rgb[0] > 200 and rgb[1] > 200 and rgb[2] > 200

def random_boolean(tendency = False):
  if tendency:
    return 0 < random.randint(-5, 5)
  else:
    return random.randint(-5, 5) < 0

def find_nearest(modifications, x2, y2, threaded=False, num_threads=4):
  nearest_point = None
  min_distance = float("inf")
  
  if threaded:
    def find_nearest_point(y1, x1):
      nonlocal nearest_point, min_distance
      
      distance = get_distance((x1, y1), (x2, y2))
      if distance < min_distance:
        nearest_point = (x1, y1)
        min_distance = distance

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
      futures = [executor.submit(find_nearest_point, y1, x1) for (y1, x1, rgb) in modifications]
      
    for future in as_completed(futures):
      future.result()
  else:
    for (y1, x1, rgb) in modifications:
      distance = get_distance((x1, y1), (x2, y2))
      
      if distance < min_distance:
        nearest_point = (x1, y1)
        min_distance = distance
    
  return nearest_point

def get_similar_color(rgb, variation=30):
  r, g, b = rgb
  new_r = max(0, min(255, r + random.randint(-variation, variation)))
  new_g = max(0, min(255, g + random.randint(-variation, variation)))
  new_b = max(0, min(255, b + random.randint(-variation, variation)))
  
  return (new_r, new_g, new_b)
  
class Filters(Enum):
  GLITCHY_RANDOM_DOWN = 1
  GLITCHY_CONSTANT = 2
  GLITCHY_CONSTANT_DOWN_ON_WHITE = 3
  GLITCHY_CONSTANT_DOWN_ON_BLACK = 4
  RANDOM_PIXELS = 5
  FIREFLIES = 6