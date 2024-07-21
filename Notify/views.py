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

class EmailListCreate(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Reference to the Firebase database
            ref = db.reference('emails')
            # Save the email in Firebase
            new_email_ref = ref.push({'email': email})
            return Response({'message': 'Email saved successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VisitorCreate(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Reference to the Firebase database
            ref = db.reference('visitors')
            # Save the visitor info in Firebase
            new_visitor_ref = ref.push({'timestamp': request.data.get('timestamp')})
            return Response({'message': 'Visitor recorded successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
