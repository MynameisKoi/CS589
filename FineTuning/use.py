import os
import openai
# read local .env file
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.environ['OPENAI_API_KEY']

from openai import OpenAI
client = OpenAI()

completion = client.completions.create(
  model="ft:babbage-002:personal::9CF8rHIy",
  prompt="When do I have to start the heater?",
  temperature=0.8
)

for chunk in completion:
  print(completion.choices[0].text)

  