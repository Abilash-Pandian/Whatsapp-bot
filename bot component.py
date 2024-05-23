import streamlit as st
from pymongo import MongoClient
import requests

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['restaurant_db']
users = db['users']

# Claude API endpoint and key
CLAUDE_API_ENDPOINT = 'https://api.anthropic.com/v1/complete'
CLAUDE_API_KEY = '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'

# Define Streamlit app
st.title("Restaurant Bot")


def process_message_with_llm(message, user_id):
    user = users.find_one({"user_id": user_id})
    if not user:
        # Handle new user and collect preferences
        users.insert_one({"user_id": user_id, "state": "new"})
        return "Welcome! Please provide your name, DOB, email, and address."

    # Handle the states for new user
    if user.get('state') == 'new':
        details = message.split(',')
        if len(details) < 4:
            return "Please provide all details: name, DOB, email, and address."

        users.update_one({"user_id": user_id}, {
            "$set": {
                "name": details[0].strip(),
                "dob": details[1].strip(),
                "email": details[2].strip(),
                "address": details[3].strip(),
                "state": "collected"
            }
        })
        return "Thank you! Please provide your food preferences: veg/non-veg, cuisine preferences, allergies, and dietary restrictions."

    if user.get('state') == 'collected':
        preferences = message.split(',')
        users.update_one({"user_id": user_id}, {
            "$set": {
                "food_preferences": {
                    "veg": preferences[0].strip().lower() == 'veg',
                    "preferences": preferences[1].strip().split(),
                    "allergies": preferences[2].strip().split(),
                    "dietary_restrictions": preferences[3].strip().split()
                },
                "state": "ready"
            }
        })
        return "Preferences saved! How can I help you today?"

    # Call Claude API to process message and get response
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


# Streamlit interface
user_id = st.text_input("Enter your user ID:")
message = st.text_area("Enter your message:")

if st.button("Send"):
    if not user_id or not message:
        st.error("Please enter your user ID and message.")
    else:
        reply = process_message_with_llm(message, user_id)
        st.success(reply)
