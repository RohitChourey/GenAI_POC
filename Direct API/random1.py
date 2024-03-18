from openai import OpenAI

client = OpenAI()



import os
from openai import OpenAI

#Get API Key
client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
 )

              #Test generarion
# completion = client.completions.create(
#     model="gpt-3.5-turbo-instruct",
#     prompt="Write a short story about Rohit Chourey being the biggest Hero.",
#     max_tokens=300,
#     temperature=0.7,
# )
# print(completion.choices[0].text)

#               #Stream feature in text generation
# stream = client.completions.create(
#     model="gpt-3.5-turbo-instruct",
#     prompt="Write python code to copy data from one excel to another present in different or same directory",
#     max_tokens=300,
#     temperature=0.7,
#     stream = True
# )
# for chunk in stream:
#         print(chunk.choices[0].text, end="")

              #Chat feature
# completion = client.chat.completions.create(
#     model="gpt-3.5-turbo-1106",
#     messages=[
#         {
#             "role": "system",
#             "content": "You are an experienced data scientist, adept at presenting complex data concepts with creativity.",
#         },
#         {
#             "role": "user",
#             "content": "What is Feature Engineering, and what are some common methods?",
#         },
#     ],
# )
# print(completion.choices[0].message.content)
# chat=[
#     {"role": "system", "content": "You are an experienced data scientist, adept at presenting complex data concepts with creativity."},
#     {"role": "user", "content": "What is Feature Engineering, and what are some common methods?"}
#   ]
# chat.append({"role": "assistant", "content": str(completion.choices[0].message.content)})
# chat.append({"role": "user", "content": "Can you summarize it, please?"})
# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo-1106",
#   messages=chat
# )
# print(completion.choices[0].message.content)

              #Audio to transcript file
# audio_file= open("gotilo.mp3", "rb")
# transcript = client.audio.transcriptions.create(
#   model="whisper-1",
#   file=audio_file
# )
# print(transcript.text)

              #Translation
# translations = client.audio.transcriptions.create(
#     model="whisper-1",
#     response_format="text",
#     language="en",
#     file=audio_file,
# )

# print(translations)

              #Text to Speech
# from pathlib import Path
# speech_file_path = Path(__file__).parent / "speech.mp3"
# response = client.audio.speech.create(
#   model="tts-1",
#   voice="alloy",
#   input= '''I see skies of blue and clouds of white
#             The bright blessed days, the dark sacred nights
#             And I think to myself
#             What a wonderful world
#          '''
# )
# response.stream_to_file(speech_file_path)

               #Image recognition
# response = client.chat.completions.create(
#     model="gpt-4-vision-preview",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "Could you please identify this image's contents and provide its location?",
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": "https://images.pexels.com/photos/235731/pexels-photo-235731.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
#                     },
#                 },
#             ],
#         }
#     ],
#     max_tokens=300,
# )

# print(response.choices[0].message.content)

                #Image recognition

# import base64

# def encode_image(image_path):
#   with open(image_path, "rb") as image_file:
#     return base64.b64encode(image_file.read()).decode('utf-8')

# image_path = "img1.jpg"

# # generating the base64 string
# base64_image = encode_image(image_path)

# response = client.chat.completions.create(
#     model="gpt-4-vision-preview",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "Could you please identify this image's contents.",
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": f"data:image/jpeg;base64,{base64_image}"
#                     },
#                 },
#             ],
#         }
#     ],
#     max_tokens=100,
# )

# print(response.choices[0].message.content)

                #image generation

response = client.images.generate(
  model="dall-e-3",
  prompt="Can you generate image showing how Artificial intelligence will be dangerous to Humans?",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url

import urllib.request

from PIL import Image

urllib.request.urlretrieve(image_url, 'img.jpg')

img = Image.open('img.jpg')

img.show()

