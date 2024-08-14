import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import firebase_admin
from firebase_admin import credentials, db
import random, string

# Path to Firebase credentials JSON file
FIREBASE_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'firebase_credentials.json')

# Initialize Firebase Admin SDK
try:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://users-95da3-default-rtdb.europe-west1.firebasedatabase.app/'
    })
except FileNotFoundError as e:
    print(f"Firebase credentials file not found: {e}")

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({"status": "failed", "message": "Email and password are required"})

            # Get a reference to the Firebase Realtime Database
            ref = db.reference('All_Users/Kluret_Users')

            # Save data to Realtime Database
            user_ref = ref.child(email.replace('.', 'dot').replace('@', 'at'))

            def generate_random_string(min_len, max_len):
                length = random.randint(min_len, max_len)
                characters = string.ascii_letters + string.digits
                random_string = ''.join(random.choice(characters) for _ in range(length))
                return random_string

            UserID = generate_random_string(20, 30)

            print(UserID)
            user_ref.set({
                "User-ID": UserID,
                "password": password,
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

            # Get a reference to the Firebase Realtime Database
            ref = db.reference('All_Users/Kluret_Users')

            # Check if the user exists in the database
            snapshot = ref.child(email.replace('.', 'dot').replace('@', 'at')).get()

            if snapshot:
                user_password = snapshot.get('password')
                if user_password == password:
                    user_id = snapshot.get('User-ID')
                    return JsonResponse({"status": "success", "message": "User exists", "user_id": user_id})
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

            # Get a reference to the Firebase Realtime Database
            ref = db.reference('All_Users/Kluret_Users')

            # Iterate through all users to find the user by User-ID
            all_users = ref.get()
            for email, user_data in all_users.items():
                if user_data.get('User-ID') == user_id:
                    return JsonResponse({
                        "status": "success",
                        "email": email.replace('dot', '.').replace('at', '@'),
                        "password": user_data.get('password')
                    })

            return JsonResponse({"status": "failed", "message": "User not found"})

        except json.JSONDecodeError as e:
            return JsonResponse({"status": "failed", "message": "Invalid JSON format"})

    return JsonResponse({"status": "failed", "message": "Only POST requests are allowed for fetching user details"})
