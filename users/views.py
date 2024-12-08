import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import random
import string

# MongoDB connection settings
MONGO_URI = "mongodb+srv://KluretUserDB:ojsgheotugfihjpeslufjpnöebkoNDEOwuflihsorufhgpdndxfouln@kluretai-users.bufni.mongodb.net/?retryWrites=true&w=majority&appName=KluretAI-Users"
DB_NAME = "kluret_db"
COLLECTION_NAME = "Kluret_Users"

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({"status": "failed", "message": "Email and password are required"})

            # Check if user already exists
            if collection.find_one({"email": email}):
                return JsonResponse({"status": "failed", "message": "User already exists"})

            def generate_random_string(min_len, max_len):
                length = random.randint(min_len, max_len)
                characters = string.ascii_letters + string.digits
                random_string = ''.join(random.choice(characters) for _ in range(length))
                return random_string

            UserID = generate_random_string(20, 30)

            # Insert user data into MongoDB
            collection.insert_one({
                "email": email,
                "password": password,
                "User-ID": UserID
            })

            return JsonResponse({"status": "success", "message": "User registered successfully"})

        except json.JSONDecodeError as e:
            return JsonResponse({"status": "failed", "message": "Invalid JSON format"})

    return JsonResponse({"status": "failed", "message": "Only POST requests are allowed"})

@csrf_exempt
def login_authorizer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({"status": "failed", "message": "Email and password are required"})

            # Find the user in MongoDB
            user = collection.find_one({"email": email})

            if user:
                if user['password'] == password:
                    return JsonResponse({"status": "success", "message": "User exists", "user_id": user['User-ID']})
                else:
                    return JsonResponse({"status": "failed", "message": "Incorrect password"})
            else:
                return JsonResponse({"status": "failed", "message": "User doesn't exist"})

        except json.JSONDecodeError as e:
            return JsonResponse({"status": "failed", "message": "Invalid JSON format"})

    return JsonResponse({"status": "failed", "message": "Only POST requests are allowed for login"})

@csrf_exempt
def get_user_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')

            if not user_id:
                return JsonResponse({"status": "failed", "message": "User ID is required"})

            # Find the user by User-ID in MongoDB
            user = collection.find_one({"User-ID": user_id})

            if user:
                return JsonResponse({
                    "status": "success",
                    "email": user['email'],
                    "password": user['password']
                })

            return JsonResponse({"status": "failed", "message": "User not found"})

        except json.JSONDecodeError as e:
            return JsonResponse({"status": "failed", "message": "Invalid JSON format"})

    return JsonResponse({"status": "failed", "message": "Only POST requests are allowed for fetching user details"})


@csrf_exempt
def get_all_users_emails(request):
    if request.method == 'GET':
        try:
            # Find all users and return only the email and id fields
            users = collection.find({}, {"_id": 1, "email": 1})
            
            # Prepare the user data list
            user_list = [
                {"id": str(user["_id"]), "email": user.get("email", None)}
                for user in users
            ]
            
            return JsonResponse({"status": "success", "users": user_list})
        except Exception as e:
            return JsonResponse({"status": "failed", "message": str(e)})

    return JsonResponse({"status": "failed", "message": "Only GET requests are allowed"})
