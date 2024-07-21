from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import firebase_admin
from firebase_admin import credentials, db
import os

# Path to Firebase credentials JSON file
FIREBASE_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'firebase_credentials.json')

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://users-95da3-default-rtdb.europe-west1.firebasedatabase.app/'
        })
    except FileNotFoundError as e:
        print(f"Firebase credentials file not found: {e}")

class UserCartView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('UserID')

        # Check if UserID is provided
        if not user_id:
            return Response({'error': 'UserID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get a reference to the Firebase Realtime Database
            ref = db.reference('All_Users/Kluret_Users')
            all_users = ref.get()

            # Find the user with the given user_id
            user_email = None
            for email, user_info in all_users.items():
                if user_info.get('User-ID') == user_id:
                    user_email = email
                    break

            if user_email:
                # User exists, fetch cart data if 'Cart' node exists
                user_ref = ref.child(user_email)
                cart_ref = user_ref.child('Cart')
                cart_data = cart_ref.get()

                if not cart_data:
                    return Response({'error': 'Cart is empty or not available'}, status=status.HTTP_404_NOT_FOUND)

                return Response(cart_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(f"Error: {e}")  # Log the error to the server console
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
