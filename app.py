from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from requests.exceptions import RequestException
import os

app = Flask(__name__)

@app.route("/welcomecard", methods=["GET"])
def generate_image():
  text1 = request.args.get("text1")
  text2 = request.args.get("text2")
  background = request.args.get("background")
  avatar = request.args.get("avatar")
  
  print(f"Generating welcome card...")
  
  return send_file(generate_welcome_image(text1, text2, background, avatar), mimetype="image/png")

def generate_welcome_image(top_text, bottom_text, background, avatar):
  # Get background
  try:
    response = requests.get(background)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
    total_width, total_height = image.size
  except RequestException as e:
    print(f"Error downloading background image: {e}")
    # Use a default solid color image if the background image can't be downloaded
    total_width, total_height = 1920, 1080
    background_color = (73, 109, 137)
    image = Image.new('RGB', (total_width, total_height), color=background_color)
    
  # Get avatar
  if avatar == None:
    # If no avatar is specified
    try:
      response = requests.get("https://bevels-files.vercel.app/discordblue.png")
      response.raise_for_status()
      avatar = Image.open(BytesIO(response.content))
      
      avatar_width, avatar_height = avatar.size
      avatar_position = (int((total_width - avatar_width) // 2), int((total_height - avatar_height) // 2))
      image.paste(avatar, avatar_position)
    except RequestException as e:
      print(f"Error downloading default avatar image: {e}")
  else:
    # If an avatar is specified
    try:
      print("Getting pfp")
      response = requests.get(avatar)
      response.raise_for_status()
      avatar = Image.open(BytesIO(response.content))
      
      avatar_width, avatar_height = avatar.size
      avatar_position = (int((total_width - avatar_width) // 2), int((total_height - avatar_height) // 2))
      
      mask = Image.new('L', (avatar_width, avatar_height), 0)
      maskDraw = ImageDraw.Draw(mask)
      maskDraw.ellipse((0, 0, avatar_width, avatar_height), fill=255)
      
      image.paste(avatar, avatar_position, mask)
    except RequestException as e:
      # If retrieving the image fails
      print(f"Error downloading avatar image: {e}")
      
      try:
        response = requests.get("https://bevels-files.vercel.app/discordblue.png")
        response.raise_for_status()
        avatar = Image.open(BytesIO(response.content))
        
        avatar_width, avatar_height = avatar.size
        avatar_position = (int((total_width - avatar_width) // 2), int((total_height - avatar_height) // 2))
      except RequestException as e:
        print(f"Error downloading default avatar image: {e}")
    

  # Path to the font file
  font_path = os.path.join(os.path.dirname(__file__), "fonts", "Roboto-Black.ttf")

  # Ensure the font file exists
  if not os.path.exists(font_path):
    raise OSError(f"Font file not found: {font_path}")

  draw = ImageDraw.Draw(image)

  font_size = 100
  font = ImageFont.truetype(font_path, size=font_size)

  top_text_position = (total_width / 2, total_height - total_height / 1.1)
  bottom_text_position = (total_width / 2, total_height - 200)
  
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

  return buffer

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True, port=25265)