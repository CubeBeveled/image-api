from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from requests.exceptions import RequestException
import os

app = Flask(__name__)

@app.route('/welcomecard', methods=["GET"])
def generate_image():
  username = request.args.get("username")
  server = request.args.get("server")
  background = request.args.get("background")
  print(f"Generating welcome card for user {username} in server {server}")
  
  return generate_welcome_image(username, server, background)

def generate_welcome_image(username, server, background):
  width, height = 800, 200

  # Get background
  try:
    response = requests.get(background)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
  except RequestException as e:
    print(f"Error downloading background image: {e}")
    # Use a default solid color image if the background image can't be downloaded
    width, height = 1920, 1080
    background_color = (73, 109, 137)
    image = Image.new('RGB', (width, height), color=background_color)

  # Path to the font file
  font_path = os.path.join(os.path.dirname(__file__), "fonts", "Roboto-Black.ttf")

  # Ensure the font file exists
  if not os.path.exists(font_path):
    raise OSError(f"Font file not found: {font_path}")

  draw = ImageDraw.Draw(image)
  width, height = image.size

  font_size = 100
  font = ImageFont.truetype(font_path, size=font_size)
  top_text = f"Welcome {username}"
  bottom_text = f"to {server}"

  top_text_position = (width / 2, (height / 2) - 400)
  bottom_text_position = (width / 2, (height / 2) + 300)
  
  # Draw top text
  draw.text(
    xy=top_text_position,
    text=top_text,
    font=font, fill="white",
    stroke_width=1,
    stroke_fill="black",
    align="center",
    anchor="mt"
  )
  
  # Draw bottom text
  draw.text(
    xy=bottom_text_position,
    text=bottom_text,
    font=font, fill="white",
    stroke_width=1,
    stroke_fill="black",
    align="center",
    anchor="mt"
  )

  buffer = BytesIO()
  image.save(buffer, format='PNG')
  buffer.seek(0)

  return send_file(buffer, mimetype='image/png')

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True, port=25003)