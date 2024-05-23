from flask import Flask, request, jsonify
from pymongo import MongoClient
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import requests

app = Flask(__name__)

# mongodb setup
client = MongoClient('mongodb://localhost:27017/')
db = client['restaurant_db']
users = db['users']
restaurants = db['restaurants']

TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''
TWILIO_PHONE_NUMBER = ''

# claude api endpoint and key
CLAUDE_API_ENDPOINT = 'https://api.anthropic.com/v1/complete'
CLAUDE_API_KEY = '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'


def send_whatsapp_message(to, body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_=TWILIO_PHONE_NUMBER,
        body=body,
        to=f'whatsapp:{to}'
    )
    return message.sid


@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    sender = request.values.get('From', '')
    user_id = sender.split(':')[1]

    response = MessagingResponse()
    reply = process_message_with_llm(incoming_msg, user_id)
    response.message(reply)

    return str(response)


def process_message_with_llm(message, user_id):
    user = users.find_one({"phone_number": user_id})
    if not user:
        # handle new user and collect preferences
        users.insert_one({"phone_number": user_id, "state": "new"})
        return "Welcome! Please provide your name, DOB, email, and address."

    # handle the states for new user
    if user.get('state') == 'new':
        details = message.split(',')
        if len(details) < 4:
            return "Please provide all details: name, DOB, email, and address."

        users.update_one({"phone_number": user_id}, {
            "$set": {
                "name": details[0].strip(),
                "dob": details[1].strip(),
                "email": details[2].strip(),
                "addresses": [{"tag": "Home", "address": details[3].strip(), "google_pin": ""}],
                "food_preferences": {"veg": True, "preferences": [], "allergies": [], "dietary_restrictions": []},
                "state": "collected"
            }
        })
        return "Thank you! Please provide your food preferences: veg/non-veg, cuisine preferences, allergies, and dietary restrictions."

    if user.get('state') == 'collected':
        preferences = message.split(',')
        users.update_one({"phone_number": user_id}, {
            "$set": {
                "food_preferences.veg": preferences[0].strip().lower() == 'veg',
                "food_preferences.preferences": preferences[1].strip().split(),
                "food_preferences.allergies": preferences[2].strip().split(),
                "food_preferences.dietary_restrictions": preferences[3].strip().split(),
                "state": "ready"
            }
        })
        return "Preferences saved! How can I help you today?"

    # call claude api to process message and get response
    headers = {
        'Authorization': f'Bearer {CLAUDE_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'prompt': f'User: {message}\nAI:',
        'max_tokens': 150
    }
    response = requests.post(CLAUDE_API_ENDPOINT, headers=headers, json=data)
    response_json = response.json()
    reply = response_json['choices'][0]['text'].strip()

    return reply


if __name__ == '__main__':
    app.run(port=5000)

# QY2Z2LNVYZ2G5ZHCP16N8ZSE
