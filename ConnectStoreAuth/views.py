from django.shortcuts import render
from django.http import JsonResponse
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
import json
import jwt

# MongoDB connection settings
CONNECTSTORE_MONGO_URL = "mongodb+srv://ConnectStoreDB:iwrsohdgjokosdifgodJI0erjdfsigjoxigjfjb4poedfjpicedf@connectstores.vqiwf.mongodb.net/?retryWrites=true&w=majority&appName=ConnectStores"
CONNECTSTORE_DB_NAME = "ConnectStoreDB"

# Connect to MongoDB
client = MongoClient(CONNECTSTORE_MONGO_URL)
db = client[CONNECTSTORE_DB_NAME]
users_collection = db['users']

SECRET_KEY = 'diofhefge9jocgpwgkrsdwedihffihsdfwuh84fhd8sfuh8s4e2h9sdhfwfu3h8rhe8airjfinwvrwd8hr'  # Replace with a strong secret key

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            
            # Check if username already exists
            if users_collection.find_one({'username': username}):
                return JsonResponse({'error': 'Username already exists'}, status=400)

            # Save user to database without hashing
            users_collection.insert_one({
                'username': username,
                'password': password  # Storing plain text password (not secure)
            })

            return JsonResponse({'message': 'User registered successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Return JSON response for non-POST requests
    return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            
            # Find the user
            user = users_collection.find_one({'username': username})
            if not user:
                return JsonResponse({'error': 'Invalid username or password'}, status=400)
            
            # Verify the password (plain text comparison)
            if user['password'] != password:
                return JsonResponse({'error': 'Invalid username or password'}, status=400)

            # Generate a JWT token
            token = jwt.encode({'username': username}, SECRET_KEY, algorithm='HS256')

            return JsonResponse({'message': 'Login successful', 'token': token})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Return JSON response for non-POST requests
    return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)
