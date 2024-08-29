import requests
import asyncio

def get_word():
  res = requests.get("https://random-word-api.herokuapp.com/word")
  return res.json()[0]

def generate(length):
  result = ""
  
  for i in range(int(length)):
    result = f"{result} {get_word()}"
    
  return result