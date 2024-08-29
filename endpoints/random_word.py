import requests
import asyncio

def generate():
  word = requests.get("https://random-word-api.herokuapp.com/word")
  word = word.json()[0]
  print(word)
  dictionary = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word[0]}")
  
  if dictionary.status_code == 404:
    return generate()
  else:
    dictionary = dictionary.json()
    
    return {
      "word": word,
      "definitions": dictionary[0]["meanings"][0]["definitions"]
    }