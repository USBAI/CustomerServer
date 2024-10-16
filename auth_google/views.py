# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import firebase_admin
from firebase_admin import credentials, auth, db
from firebase_admin.exceptions import FirebaseError

# Path to Firebase credentials JSON file
FIREBASE_CREDENTIALS_PATH = "auth_google/firebase_credentials.json"

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://users-95da3-default-rtdb.europe-west1.firebasedatabase.app/'
    })

@csrf_exempt
def google_register(request):
    if request.method == 'POST':
        try:
            # Extract the ID token from the Authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse({"error": "Authorization header missing"}, status=400)

            id_token = auth_header.split('Bearer ')[1]

            # Verify the ID token using Firebase Admin SDK
            decoded_token = auth.verify_id_token(id_token)
            user_id = decoded_token['uid']
            email = decoded_token['email']
            display_name = decoded_token.get('name')

            # Save user info to Firebase Realtime Database
            user_ref = db.reference(f"All_Users/Kluret_USERS_Google/{user_id}")
            user_ref.set({
                'uid': user_id,
                'email': email,
                'displayName': display_name,
                'provider': 'google',
            })

            return JsonResponse({"message": "User registered successfully"}, status=200)

        except FirebaseError as e:
            return JsonResponse({"error": str(e)}, status=500)

        except Exception as e:
            return JsonResponse({"error": "Invalid token or request"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
