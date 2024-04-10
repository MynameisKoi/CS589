import os
import openai
# read local .env file
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.environ['OPENAI_API_KEY']

from openai import OpenAI
client = OpenAI()

train_file = client.files.create(
  file=open("data_prepared.jsonl", "rb"),
  purpose="fine-tune"
)

model = client.fine_tuning.jobs.create(
  training_file="file-KlOHYmDdtWSixgLefq4DalcI",
  model="babbage-002"
)

print(f"Train file: {train_file}\n")
print(f"Model: {model}\n")

