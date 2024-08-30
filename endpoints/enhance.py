from PIL import Image, ImageFilter
from flask import send_file
from io import BytesIO
import requests
from requests.exceptions import RequestException

def generate(image_url, cycles):
  try:
    response = requests.get(image_url, stream=True)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
    
    for i in range(int(cycles)):
      image = image.filter(ImageFilter.EDGE_ENHANCE)
  except RequestException as e:
    print(f"Error downloading background image: {e}")
  
  # Convert to buffer
  buffer = BytesIO()
  image.save(buffer, format="PNG")
  buffer.seek(0)
  
  return send_file(buffer, mimetype="image/png")