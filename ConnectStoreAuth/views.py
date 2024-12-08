from django.shortcuts import render
from django.http import JsonResponse
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
import json
import jwt
import uuid

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
            # Parse incoming JSON data
            data = json.loads(request.body)
            
            store_name = data.get('store_name')  # Store Name
            email = data.get('email')  # Email Address
            website_url = data.get('website_url')  # Website URL
            store_type = data.get('store_type')  # Store Type
            password = data.get('password')  # Password
            confirm_password = data.get('confirm_password')  # Confirm Password

            # Validate required fields
            if not all([store_name, email, website_url, store_type, password, confirm_password]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # Validate password confirmation
            if password != confirm_password:
                return JsonResponse({'error': 'Passwords do not match.'}, status=400)

            # Check if email already exists
            if users_collection.find_one({'email': email}):
                return JsonResponse({'error': 'Email already exists'}, status=400)

            # Check if username (store name) already exists
            if users_collection.find_one({'store_name': store_name}):
                return JsonResponse({'error': 'Store name already exists'}, status=400)

            # Generate a random store_id
            store_id = str(uuid.uuid4())

            # Save the user to the ConnectStoreAuth database
            users_collection.insert_one({
                'store_id': store_id,  # Add the generated store_id
                'store_name': store_name,
                'email': email,
                'website_url': website_url,
                'store_type': store_type,
                'password': password  # Plain text (not secure)
            })

            # Save the store details to the ConnectStoreServer collection
            connect_store_server_collection = db['ConnectStoreServer']
            connect_store_server_collection.insert_one({
                'store_id': store_id,
                'store_name': store_name,
                'email': email,
                'website_url': website_url,
                'store_type': store_type
            })

            return JsonResponse({'message': 'Store registered successfully', 'store_id': store_id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Return JSON response for non-POST requests
    return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data['email']  # Change to email
            password = data['password']
            
            # Find the user by email
            user = users_collection.find_one({'email': email})
            if not user:
                return JsonResponse({'error': 'Invalid email or password'}, status=400)
            
            # Verify the password (plain text comparison)
            if user['password'] != password:
                return JsonResponse({'error': 'Invalid email or password'}, status=400)

            # Generate a JWT token
            token = jwt.encode({'email': email}, SECRET_KEY, algorithm='HS256')

            # Extract the store_id from the user document
            store_id = user.get('store_id')

            return JsonResponse({
                'message': 'Login successful',
                'token': token,
                'store_id': store_id
            }, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Return JSON response for non-POST requests
    return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)
