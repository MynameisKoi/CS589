import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai.api_key  = os.environ['OPENAI_API_KEY']

from openai import OpenAI
client = OpenAI()


# Configure the model ID. Change this to your model ID.
model = "ft:babbage-002:personal:drug-malady-data:9CPfhWiC"

# Let's use a drug from each class
drugs = [
    "A CN Gel(Topical) 20gmA CN Soap 75gm",  # Class 0
    "Addnok Tablet 20'S",                    # Class 1
    "ABICET M Tablet 10's",                  # Class 2
]

# Returns a drug class for each drug
for drug_name in drugs:
    prompt = "Drug: {}\nMalady:".format(drug_name)

    response = client.completions.create(
        model=model,
        prompt=prompt,
        temperature=1,
        max_tokens=2,
    )

    # Print the generated text
    drug_class = response.choices[0].text
    # The result should be 0, 1, and 2
    print(drug_class)

# Let's use a drug from each class
drugs = [
    "What is 'A CN Gel(Topical) 20gmA CN Soap 75gm' used for?",  # Class 0
    "What is 'Addnok Tablet 20'S' used for?",  # Class 1
    "What is 'ABICET M Tablet 10's' used for?",  # Class 2
]

class_map = {
    0: "Acne",
    1: "Adhd",
    2: "Allergies",
    # ...
}

# Returns a drug class for each drug
for drug_name in drugs:
    prompt = "Drug: {}\nMalady:".format(drug_name)

    response = client.completions.create(
        model=model,
        prompt=prompt,
        temperature=1,
        max_tokens=2,
    )

    response = response.choices[0].text
    try:
        print(drug_name + " is used for " + class_map[int(response)])
    except:
        print("I don't know what " + drug_name + " is used for.")
    print()
