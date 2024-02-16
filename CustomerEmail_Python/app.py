import os
from dotenv import load_dotenv, find_dotenv
import openai
from flask import Flask, redirect, render_template, request, url_for
_ = load_dotenv(find_dotenv()) # read local .env file

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define your delimiter
delimiter = "####"

# General function to get response with gpt-3.5
def get_completion_from_messages(messages,
                                 model="gpt-3.5-turbo-instruct",
                                 temperature=0,
                                 max_tokens=1000):
    response = openai.Completion.create(
        model=model,
        prompt=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].text.strip()


# Step 1: Generate a customer's comment
# System message include product details
def generate_comment():
    system_message_comment=f"""
    Product details can be found as below

        "TechPro Ultrabook":
            "name": "TechPro Ultrabook",
            "category": "Computers and Laptops",
            "brand": "TechPro",
            "model_number": "TP-UB100",
            "warranty": "1 year",
            "rating": 4.5,
            "features": ["13.3-inch display", "8GB RAM",
                    "256GB SSD", "Intel Core i5 processor"],
            "description": "A sleek and lightweight ultrabook for everyday use.",
            "price": 799.99

        "BlueWave Gaming Laptop":
            "name": "BlueWave Gaming Laptop",
            "category": "Computers and Laptops",
            "brand": "BlueWave",
            "model_number": "BW-GL200",
            "warranty": "2 years",
            "rating": 4.7,
            "features": ["15.6-inch display", "16GB RAM",
                    "512GB SSD", "NVIDIA GeForce RTX 3060"],
            "description": "A high-performance gaming laptop for
                    an immersive experience.",
            "price": 1199.99

        "PowerLite Convertible":
            "name": "PowerLite Convertible",
            "category": "Computers and Laptops",
            "brand": "PowerLite",
            "model_number": "PL-CV300",
            "warranty": "1 year",
            "rating": 4.3,
            "features": ["14-inch touchscreen", "8GB RAM",
                    "256GB SSD", "360-degree hinge"],
            "description": "A versatile convertible laptop with
                    a responsive touchscreen.",
            "price": 699.99

        "TechPro Desktop":
            "name": "TechPro Desktop",
            "category": "Computers and Laptops",
            "brand": "TechPro",
            "model_number": "TP-DT500",
            "warranty": "1 year",
            "rating": 4.4,
            "features": ["Intel Core i7 processor", "16GB RAM",
                    "1TB HDD", "NVIDIA GeForce GTX 1660"],
            "description": "A powerful desktop computer for work
                    and play.",
            "price": 999.99

    "BlueWave Chromebook":
            "name": "BlueWave Chromebook",
            "category": "Computers and Laptops",
            "brand": "BlueWave",
            "model_number": "BW-CB100",
            "warranty": "1 year",
            "rating": 4.1,
            "features": ["11.6-inch display", "4GB RAM",
                    "32GB eMMC",
                    "Chrome OS"],
            "description": "A compact and affordable Chromebook
                    for everyday tasks.",
            "price": 249.99

        "SmartX ProPhone":
            "name": "SmartX ProPhone",
            "category": "Smartphones and Accessories",
            "brand": "SmartX",
            "model_number": "SX-PP10",
            "warranty": "1 year",
            "rating": 4.6,
            "features": ["6.1-inch display", "128GB storage",
                    "12MP dual camera", "5G"],
            "description": "A powerful smartphone with advanced
                    camera features.",
            "price": 899.99

        "MobiTech PowerCase":
            "name": "MobiTech PowerCase",
            "category": "Smartphones and Accessories",
            "brand": "MobiTech",
            "model_number": "MT-PC20",
            "warranty": "1 year",
            "rating": 4.3,
            "features":
                ["5000mAh battery", "Wireless charging",
                "Compatible with SmartX ProPhone"],
            "description":
                "A protective case with built-in battery
                for extended usage.",
            "price": 59.99

        "SmartX MiniPhone":
            "name": "SmartX MiniPhone",
            "category": "Smartphones and Accessories",
            "brand": "SmartX",
            "model_number": "SX-MP5",
            "warranty": "1 year",
            "rating": 4.2,
            "features": ["4.7-inch display", "64GB storage",
                    "8MP camera", "4G"],
            "description": "A compact and affordable smartphone
                    for basic tasks.",
            "price": 399.99

        "MobiTech Wireless Charger":
            "name": "MobiTech Wireless Charger",
            "category": "Smartphones and Accessories",
            "brand": "MobiTech",
            "model_number": "MT-WC10",
            "warranty": "1 year",
            "rating": 4.5,
            "features": ["10W fast charging", "Qi-compatible",
                    "LED indicator", "Compact design"],
            "description": "A convenient wireless charger for
                    a clutter-free workspace.",
            "price": 29.99

        "SmartX EarBuds":
            "name": "SmartX EarBuds",
            "category": "Smartphones and Accessories",
            "brand": "SmartX",
            "model_number": "SX-EB20",
            "warranty": "1 year",
            "rating": 4.4,
            "features": ["True wireless", "Bluetooth 5.0",
                    "Touch controls", "24-hour battery life"],
            "description": "Experience true wireless freedom with
                    these comfortable earbuds.",
            "price": 99.99

        "CineView 4K TV":
            "name": "CineView 4K TV",
            "category": "Televisions and Home Theater Systems",
            "brand": "CineView",
            "model_number": "CV-4K55",
            "warranty": "2 years",
            "rating": 4.8,
            "features": ["55-inch display", "4K resolution",
                    "HDR", "Smart TV"],
            "description": "A stunning 4K TV with vibrant colors
                    and smart features.",
            "price": 599.99

        "SoundMax Home Theater":
            "name": "SoundMax Home Theater",
            "category": "Televisions and Home Theater Systems",
            "brand": "SoundMax",
            "model_number": "SM-HT100",
            "warranty": "1 year",
            "rating": 4.4,
            "features": ["5.1 channel", "1000W output",
                    "Wireless subwoofer", "Bluetooth"],
            "description": "A powerful home theater system for
                    an immersive audio experience.",
            "price": 399.99

        "CineView 8K TV":
            "name": "CineView 8K TV",
            "category": "Televisions and Home Theater Systems",
            "brand": "CineView",
            "model_number": "CV-8K65",
            "warranty": "2 years",
            "rating": 4.9,
            "features": ["65-inch display", "8K resolution",
                    "HDR", "Smart TV"],
            "description": "Experience the future of television
                    with this stunning 8K TV.",
            "price": 2999.99

        "SoundMax Soundbar":
            "name": "SoundMax Soundbar",
            "category": "Televisions and Home Theater Systems",
            "brand": "SoundMax",
            "model_number": "SM-SB50",
            "warranty": "1 year",
            "rating": 4.3,
            "features": ["2.1 channel", "300W output",
                    "Wireless subwoofer", "Bluetooth"],
            "description": "Upgrade your TV's audio with this
                    sleek and powerful soundbar.",
            "price": 199.99

        "CineView OLED TV":
            "name": "CineView OLED TV",
            "category": "Televisions and Home Theater Systems",
            "brand": "CineView",
            "model_number": "CV-OLED55",
            "warranty": "2 years",
            "rating": 4.7,
            "features": ["55-inch display", "4K resolution",
                    "HDR", "Smart TV"],
            "description": "Experience true blacks and vibrant
                    colors with this OLED TV.",
            "price": 1499.99

        "GameSphere X":
            "name": "GameSphere X",
            "category": "Gaming Consoles and Accessories",
            "brand": "GameSphere",
            "model_number": "GS-X",
            "warranty": "1 year",
            "rating": 4.9,
            "features": ["4K gaming", "1TB storage",
                    "Backward compatibility",
                    "Online multiplayer"],
            "description":
                    "A next-generation gaming console for
                    the ultimate gaming experience.",
            "price": 499.99

        "ProGamer Controller":
            "name": "ProGamer Controller",
            "category": "Gaming Consoles and Accessories",
            "brand": "ProGamer",
            "model_number": "PG-C100",
            "warranty": "1 year",
            "rating": 4.2,
            "features": ["Ergonomic design",
                    "Customizable buttons",
                    "Wireless", "Rechargeable battery"],
            "description": "A high-quality gaming controller
                    for precision and comfort.",
            "price": 59.99

        "GameSphere Y":
            "name": "GameSphere Y",
            "category": "Gaming Consoles and Accessories",
            "brand": "GameSphere",
            "model_number": "GS-Y",
            "warranty": "1 year",
            "rating": 4.8,
            "features": ["4K gaming", "500GB storage",
                    "Backward compatibility",
                    "Online multiplayer"],
            "description": "A compact gaming console
                    with powerful performance.",
            "price": 399.99

        "ProGamer Racing Wheel":
            "name": "ProGamer Racing Wheel",
            "category": "Gaming Consoles and Accessories",
            "brand": "ProGamer",
            "model_number": "PG-RW200",
            "warranty": "1 year",
            "rating": 4.5,
            "features": ["Force feedback", "Adjustable pedals",
                    "Paddle shifters",
                    "Compatible with GameSphere X"],
            "description": "Enhance your racing games with
                    this realistic racing wheel.",
            "price": 249.99

        "GameSphere VR Headset":
            "name": "GameSphere VR Headset",
            "category": "Gaming Consoles and Accessories",
            "brand": "GameSphere",
            "model_number": "GS-VR",
            "warranty": "1 year",
            "rating": 4.6,
            "features": ["Immersive VR experience",
                "Built-in headphones",
                "Adjustable headband",
                "Compatible with GameSphere X"],
            "description":
                "Step into the world of virtual reality
                with this comfortable VR headset.",
            "price": 299.99

        "AudioPhonic Noise-Canceling Headphones":
            "name": "AudioPhonic Noise-Canceling Headphones",
            "category": "Audio Equipment",
            "brand": "AudioPhonic",
            "model_number": "AP-NC100",
            "warranty": "1 year",
            "rating": 4.6,
            "features": ["Active noise-canceling", "Bluetooth",
                    "20-hour battery life", "Comfortable fit"],
            "description": "Experience immersive sound with
                    these noise-canceling headphones.",
            "price": 199.99

        "WaveSound Bluetooth Speaker":
            "name": "WaveSound Bluetooth Speaker",
            "category": "Audio Equipment",
            "brand": "WaveSound",
            "model_number": "WS-BS50",
            "warranty": "1 year",
            "rating": 4.5,
            "features": ["Portable", "10-hour battery life",
                    "Water-resistant", "Built-in microphone"],
            "description": "A compact and versatile Bluetooth
                    speaker for music on the go.",
            "price": 49.99

        "AudioPhonic True Wireless Earbuds":
            "name": "AudioPhonic True Wireless Earbuds",
            "category": "Audio Equipment",
            "brand": "AudioPhonic",
            "model_number": "AP-TW20",
            "warranty": "1 year",
            "rating": 4.4,
            "features": ["True wireless", "Bluetooth 5.0",
                    "Touch controls", "18-hour battery life"],
            "description": "Enjoy music without wires with these
                    comfortable true wireless earbuds.",
            "price": 79.99

        "WaveSound Soundbar":
            "name": "WaveSound Soundbar",
            "category": "Audio Equipment",
            "brand": "WaveSound",
            "model_number": "WS-SB40",
            "warranty": "1 year",
            "rating": 4.3,
            "features": ["2.0 channel", "80W output",
                    "Bluetooth", "Wall-mountable"],
            "description": "Upgrade your TV's audio with
                    this slim and powerful soundbar.",
            "price": 99.99

    """

    user_message_comment=f"""
    A less than 100 words comment about the products"""

    messages_comment =  [
    {'role':'system',
    'content': system_message_comment},
    {'role':'user',
    'content': f"{delimiter}{user_message_comment}{delimiter}"},
    {'role':'assistant',
    'content':'talk as a customer'}
    ]
    comment = get_completion_from_messages(messages_comment)

    print("Comment from customers: ")
    print(comment+"\n")

    return comment

# Step 2: Generate email subject
def get_subject(comment):
    system_message_subject=comment
    user_message_subject=f"""
    Subject of an email from the comment using Inferring technique within 10 words"""
    messages_subject =  [
    {'role':'system',
    'content': system_message_subject},
    {'role':'user',
    'content': f"{delimiter}{user_message_subject}{delimiter}"},
    ]
    subject = get_completion_from_messages(messages_subject)

    print("Subject of customer comment: ")
    print(subject+"\n")

    return subject

# Step 3:  Generate the summary of the customer's comment
def get_summary(comment):
    system_message_summary=comment
    user_message_summary=f"""
    Give the summary in English of the comment using Summarizing technique within 35 words."""
    messages_summary =  [
    {'role':'system',
    'content': system_message_summary},
    {'role':'user',
    'content': f"{delimiter}{user_message_summary}{delimiter}"},
    ]
    summary=get_completion_from_messages(messages_summary)

    print("Summary of customer comment:")
    print(summary+"\n")

    return summary

# Step 4: Sentiment analysis of the customer's comment
def get_sentiment(comment):
    system_message_sentiment=comment
    user_message_sentiment=f"""
    Sentiment analysis of the customer's comment using Inferring technique. Positive or Negative?"""
    messages_sentiment =  [
    {'role':'system',
    'content': system_message_sentiment},
    {'role':'user',
    'content': f"{delimiter}{user_message_sentiment}{delimiter}"},
    ]
    sentiment=get_completion_from_messages(messages_sentiment)

    print(sentiment+"\n")

    return sentiment

# Step 5: Generate an email to be sent to the customer
def get_email(comment, subject, summary, sentiment):
    system_message_email = comment + subject + summary + sentiment
    user_message_email = f"""
    Please create an email to be sent to the customer based on {comment}, including the {subject}, {summary} and \
        {sentiment} with proper email format with subject and extra."""
    messages_email = [
        {'role': 'system',
         'content': system_message_email},
        {'role': 'user',
         'content': f"{delimiter}{user_message_email}{delimiter}"},
    ]
    email = get_completion_from_messages(messages_email)

    return email  # Return the email without printing it

def get_translation(summary, language):
    system_message_translate=summary
    user_message_translate=f"""
    Translate the summary into {language} using Transforming technique"""
    messages_translate =  [
    {'role':'system',
    'content': system_message_translate},
    {'role':'user',
    'content': f"{delimiter}{user_message_translate}{delimiter}"},
    ]
    translate=get_completion_from_messages(messages_translate)

    print("Translation of customer comment summary in "+language+":")
    print(translate+"\n")

    return translate

# Define the index route
@app.route('/', methods=['GET', 'POST'])
def index():
    comment = None
    email = None
    language = "English"  # Initialize the language variable here

    if request.method == 'POST':
        language = request.form['language']
        comment = generate_comment()
        subject = get_subject(comment)
        summary = get_summary(comment)
        sentiment = get_sentiment(comment)
        email = get_email(comment, subject, summary, sentiment)

        # Check if the user wants to translate the comment and email
        translate_comment = 'translate-comment' in request.form
        translate_email = 'translate-email' in request.form

        if translate_comment:
            comment = get_translation(comment, language)

        if translate_email:
            email = get_translation(email, language)

    return render_template('index.html', comment=comment, email=email, language=language)


if __name__ == '__main__':
    app.run(debug=True)
