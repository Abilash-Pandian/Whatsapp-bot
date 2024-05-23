from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['restaurant_db']
users = db['users']
restaurants = db['restaurants']


restaurants.insert_many([
    {
        "name": "Restaurant A",
        "menu": [
            {"dish": "Spicy Noodles", "portion_size": "Full", "price": 200,
                "pic": "url_to_pic", "spicy": True, "cuisine": "Chinese"},
            {"dish": "Manchurian", "portion_size": "Half", "price": 150,
                "pic": "url_to_pic", "spicy": True, "cuisine": "Chinese"},
        ],
        "address": "Location A",
        "google_pin": "11°01'53.7\"N 77°01'02.0\"E",
        "branches": [{"address": "Branch A1", "google_pin": "Google PIN A1"}]
    },
    {
        "name": "Restaurant B",
        "menu": [
            {"dish": "Sweet and Sour Chicken", "portion_size": "Full", "price": 250,
                "pic": "url_to_pic", "spicy": False, "cuisine": "Chinese"},
            {"dish": "Spring Rolls", "portion_size": "Half", "price": 100,
                "pic": "url_to_pic", "spicy": False, "cuisine": "Chinese"},
        ],
        "address": "Location B",
        "google_pin": "11°00'50.8\"N 77°01'14.8\"E",
        "branches": [{"address": "Branch B1", "google_pin": "Google PIN B1"}]
    }
])

users.insert_many([
    {
        "phone_number": "6369625511",
        "name": "Abilash Pandian",
        "dob": "2002-09-26",
        "email": "abilashpandian39@gmail.com",
        "addresses": [{"tag": "Home", "address": "L-12 PQ", "google_pin": "11°02'42.4\"N 76°59'52.5\"E"
                       }],
        "food_preferences": {"veg": True, "preferences": ["Chinese"], "allergies": [], "dietary_restrictions": []},
    },
])
