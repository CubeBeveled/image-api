from PIL import Image
import numpy as np
import random
import os

from utils import set_pixel, is_white, is_black, random_boolean, Filters, find_nearest, get_distance, get_similar_color, video_from_image_sequence

# General settings
image_path = "test5.png"
image_color_space = "RGB"
filter = Filters.GLITCHY_RANDOM_DOWN_ON_BLACK
log_progress = True
black_threshold = 50
white_threshold = 200

# Fireflies settings
fireflies_min_distance = 10

# Animation settings
animate = False
modifications_per_frame = 1000
frame_output_folder = "frames"

# Animation to video settings
convert_frames_to_video = False
output_filename = "animation.mp4"
output_framerate = 30

image = Image.open(image_path) # Load the image
image = image.convert(image_color_space) # Convert the image to a set color space
image_array = np.array(image) # Convert the image to an array

height, width, channels = image_array.shape # Get the size of the image
total_pixels = width * height # This is a variable so we dont have to calculate it every time when logging pixel progress

modifications = []
processed_pixels_count = 0

# Variables used for the animation
processed_modifications_count = 0
modifs_per_frame_counter = 0
frame_index = 0

# Arrays start at 0 cuh
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
          
      elif filter == Filters.GLITCHY_RANDOM_DOWN_ON_WHITE:
        if is_white(pixel_rgb, white_threshold) and random_boolean(True):
          modifications.append((y, x, image_array[y - 2, x]))
          modifications.append((y + 2, x, pixel_rgb))
        
      elif filter == Filters.GLITCHY_RANDOM_DOWN_ON_BLACK:
        if is_black(pixel_rgb, black_threshold) and random_boolean(True):
          modifications.append((y, x, image_array[y - 2, x]))
          modifications.append((y + 2, x, pixel_rgb))
        
      elif filter == Filters.GLITCHY_CONSTANT_DOWN_ON_WHITE:
        if is_white(pixel_rgb, white_threshold):
          modifications.append((y, x, image_array[y - 1, x]))
          modifications.append((y + 1, x, pixel_rgb))

      elif filter == Filters.GLITCHY_CONSTANT_DOWN_ON_BLACK:
        if is_black(pixel_rgb, black_threshold):
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
      processed_pixels_count += 1
      processed_percentage = (processed_pixels_count / total_pixels) * 100
      
      if processed_percentage % 1 == 0:
        print(f"Processed {processed_percentage}%", end="\r")

total_modifications = len(modifications)
print("\nModifying array " + str(total_modifications))

if not os.path.exists(frame_output_folder) and not os.path.isdir(frame_output_folder):
  os.makedirs(frame_output_folder, exist_ok=True)

for (y, x, rgb) in modifications: 
  set_pixel(image_array, y, x, rgb)
  modifs_per_frame_counter += 1
  
  if animate:
    if modifs_per_frame_counter >= modifications_per_frame:
      modified_image = Image.fromarray(image_array)
      modified_image.save(f"frames/{frame_index}.png")
      frame_index += 1
      modifs_per_frame_counter = 0
  
  if log_progress:
    processed_modifications_count += 1
    processed_percentage = (processed_modifications_count / total_modifications) * 100
    
    if processed_percentage % 1 == 0:
      print(f"Processed {processed_percentage}%", end="\r")

if animate and convert_frames_to_video:
  video_from_image_sequence(frame_output_folder, output_filename, output_framerate)
else:
  print("\nShowing")
  modified_image = Image.fromarray(image_array)
  modified_image.show()