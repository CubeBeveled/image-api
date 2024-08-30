from PIL import Image, ImageDraw, ImageOps
from io import BytesIO
import requests
from requests.exceptions import RequestException

def generate(text):
  try:
    response = requests.get("https://bevels-files.vercel.app/caution.png", stream=True)
    response.raise_for_status()
    background = Image.open(BytesIO(response.content))
    total_width, total_height = background.size
  except RequestException as e:
    print(f"Error downloading background image: {e}")