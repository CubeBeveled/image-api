from PIL import Image, ImageDraw, ImageOps
from io import BytesIO
import requests
from requests.exceptions import RequestException

def generate(avatar, fallback_avatar):
  print("- Getting background...")
  try:
    response = requests.get("https://bevels-files.vercel.app/wanted.png")
    response.raise_for_status()
    background = Image.open(BytesIO(response.content))
    total_width, total_height = background.size
  except RequestException as e:
    print(f"Error downloading background image: {e}")

  print("- Getting avatar...")
  try:
    response = requests.get(avatar)
    response.raise_for_status()
    avatar = Image.open(BytesIO(response.content))
  except RequestException as e:
    # If retrieving the image fails
    print(f"Error downloading avatar image: {e}")
    
    # Apply fallback image
    try:
      response = requests.get(fallback_avatar)
      response.raise_for_status()
      avatar = Image.open(BytesIO(response.content))
    except RequestException as e:
      print(f"Error downloading default avatar image: {e}")
      
  avatar_size_ratio = 0.5
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
  
  # Convert to buffer
  buffer = BytesIO()
  background.save(buffer, format="PNG")
  buffer.seek(0)
  
  print("- Done")
  return buffer