from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import requests
import os
from requests.exceptions import RequestException


def generate(top_text, bottom_text, background_url, avatar, fallback_avatar):
  print("- Getting background...")
  
  try:
    response = requests.get(background_url, stream=True)
    response.raise_for_status()
    background = Image.open(BytesIO(response.content))
    total_width, total_height = background.size
  except RequestException as e:
    print(f"Error downloading background image: {e}")
    # Use a solid color image if the background image can't be downloaded
    total_width, total_height = 1920, 1080
    background_color = (73, 109, 137)
    background = Image.new("RGBA", (total_width, total_height), color=background_color)

  print("- Getting avatar...")
  try:
    response = requests.get(avatar, stream=True)
    response.raise_for_status()
    avatar = Image.open(BytesIO(response.content))
  except RequestException as e:
    # If retrieving the image fails
    print(f"Error downloading avatar image: {e}")
    
    # Apply fallback image
    try:
      response = requests.get(fallback_avatar, stream=True)
      response.raise_for_status()
      avatar = Image.open(BytesIO(response.content))
    except RequestException as e:
      print(f"Error downloading default avatar image: {e}")
  
  # Get avatar size and apply it
  avatar_size_ratio = 0.3 
  avatar_size = (int(min(total_width, total_height) * avatar_size_ratio),) * 2
  avatar = ImageOps.fit(avatar, avatar_size, centering=(0.5, 0.5))
  
  # Define dimensions and position
  avatar_width, avatar_height = avatar.size
  avatar_position = (int((total_width - avatar_width) / 2), int((total_height - avatar_height) / 2))
  
  # Make the circular mask
  avatar_mask = Image.new("L", (avatar_width, avatar_height), 0)
  maskDraw = ImageDraw.Draw(avatar_mask)
  maskDraw.ellipse((0, 0, avatar_width, avatar_height), fill=255)
  
  print("- Drawing")
  # Paste (applying mask)
  background.paste(avatar, avatar_position, avatar_mask)
  
  # Path to the font file
  font_path = os.path.join(os.path.dirname(__file__), "fonts", "Roboto-Black.ttf")

  # Ensure the font file exists
  if not os.path.exists(font_path):
    raise OSError(f"Font file not found: {font_path}")

  draw = ImageDraw.Draw(background)

  # Define font
  font_size_ratio = 0.15
  font_size = int(min(total_width, total_height) * font_size_ratio)
  font = ImageFont.truetype(font_path, size=font_size)

  # Define the positions of the text
  top_text_position = (total_width / 2, total_height / 4)
  bottom_text_position = (total_width / 2, (total_height / 4) + (total_height / 2))
  
  # Draw top text
  draw.text(
    xy=top_text_position,
    text=top_text,
    font=font, fill="white",
    stroke_width=0,
    stroke_fill="black",
    align="center",
    anchor="mb"
  )
  
  # Draw bottom text
  draw.text(
    xy=bottom_text_position,
    text=bottom_text,
    font=font, fill="white",
    stroke_width=0,
    stroke_fill="black",
    align="center",
    anchor="mt"
  )

  # Convert to buffer
  buffer = BytesIO()
  background.save(buffer, format="PNG")
  buffer.seek(0)
  
  print("- Done")
  return buffer