import random
import string
import uuid  # For generating user UUIDs
import json
from django.http import JsonResponse
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
import jwt

# MongoDB connection settings
ACCESS_API_MONGO_URL = "mongodb+srv://AccessAPI:wiudshfihuHIEIUFoijofewhsfrfhfjKJDOEPAiJEiofsohuefdhuocohgbdvixfbicgjrieruigoreo@accessapi.silf8.mongodb.net/?retryWrites=true&w=majority&appName=AccessAPI"  # Replace with your MongoDB connection string
ACCESS_API_DB_NAME = "AccessAPI"  # Replace with your database name

# Initialize MongoDB client and database
client = MongoClient(ACCESS_API_MONGO_URL)
db = client[ACCESS_API_DB_NAME]

# Define the collection
access_users_collection = db['AccessUsers']

SECRET_KEY = 'pdouhpdofijcgoduhfgepgfoJJIHDwfiedifefihpkevvifhi959fjv9h5efdc9g39evfh9cgi3hr9'  # Replace with a strong secret key

# Helper function to generate a random API key
def generate_api_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            # Parse incoming JSON data
            data = json.loads(request.body)
            company_name = data.get('company_name')
            email = data.get('email')
            website_url = data.get('website_url')
            plan = data.get('plan')  # Basic, Professional, or Enterprise
            password = data.get('password')
            confirm_password = data.get('confirm_password')

            # Validate required fields
            if not all([company_name, email, website_url, plan, password, confirm_password]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # Validate password confirmation
            if password != confirm_password:
                return JsonResponse({'error': 'Passwords do not match.'}, status=400)

            # Check if email already exists
            if access_users_collection.find_one({'email': email}):
                return JsonResponse({'error': 'Email already exists.'}, status=400)

            # Generate user UUID and unique API key
            user_uuid = str(uuid.uuid4())
            while True:
                api_key = str(uuid.uuid4())
                if api_key != user_uuid:  # Ensure API key and user UUID are not the same
                    break

            # Save user to the AccessUsers collection
            access_users_collection.insert_one({
                'company_name': company_name,
                'email': email,
                'website_url': website_url,
                'plan': plan,
                'password': password,  # Plain text password (not secure)
                'api_key': api_key,
                'user_uuid': user_uuid,
                'active': False
            })

            return JsonResponse({
                'message': 'User registered successfully.',
                'api_key': api_key,
                'user_uuid': user_uuid
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # Find the user by email
            user = access_users_collection.find_one({'email': email})
            if not user:
                return JsonResponse({'error': 'Invalid email or password.'}, status=400)

            # Verify the password
            if user['password'] != password:
                return JsonResponse({'error': 'Invalid email or password.'}, status=400)

            # Generate a JWT token
            token = jwt.encode({'email': email}, SECRET_KEY, algorithm='HS256')

            return JsonResponse({
                'message': 'Login successful',
                'token': token,
                'api_key': user['api_key'],
                'user_uuid': user['user_uuid']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)

@csrf_exempt
def get_user_info(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_uuid = data.get('user_uuid')

            # Validate user_uuid
            user = access_users_collection.find_one({'user_uuid': user_uuid})
            if not user:
                return JsonResponse({'error': 'Invalid user UUID.'}, status=400)

            # Return user info
            user_info = {
                'company_name': user['company_name'],
                'email': user['email'],
                'website_url': user['website_url'],
                'plan': user['plan'],
                'active': user['active']
            }
            return JsonResponse({'user_info': user_info})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)

@csrf_exempt
def add_user_info(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_uuid = data.get('user_uuid')
            additional_info = data.get('additional_info')

            # Validate user_uuid
            user = access_users_collection.find_one({'user_uuid': user_uuid})
            if not user:
                return JsonResponse({'error': 'Invalid user UUID.'}, status=400)

            # Add user info
            access_users_collection.update_one(
                {'user_uuid': user_uuid},
                {'$set': {'additional_info': additional_info}}
            )

            return JsonResponse({'message': 'User information added successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)