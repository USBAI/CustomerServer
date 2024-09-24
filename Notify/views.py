from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import firebase_admin
from firebase_admin import credentials, db
import os
from twilio.rest import Client

# Twilio configuration
TWILIO_ACCOUNT_SID = 'ACd0f9c45cb4f7904a51b4c6412d25bc68'
TWILIO_AUTH_TOKEN = 'dc2b567d27a0fe3b9c9606fdffc329e4'
TWILIO_PHONE_NUMBER = '+17722131346'

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
            # Reference to the Firebase database for visitors
            ref = db.reference('visitors')
            # Save the current visitor info in Firebase
            new_visitor_ref = ref.push({'timestamp': request.data.get('timestamp')})
            
            # Retrieve the total number of visitors after saving
            total_visitors = ref.get()
            total_visitor_count = len(total_visitors) if total_visitors else 0

            # Send SMS via Twilio
            self.send_sms(total_visitor_count)

            return Response({'message': 'Visitor recorded successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def send_sms(self, total_visitor_count):
        try:
            # Initialize Twilio client
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            # Compose the SMS message
            message_body = f"Hello Kluret, your platform currently has {total_visitor_count} visitors."

            # Send the SMS to the specified phone number
            message = client.messages.create(
                body=message_body,
                from_=TWILIO_PHONE_NUMBER,
                to='+46727759188'
            )

            print(f"SMS sent successfully: {message.sid}")
        except Exception as e:
            print(f"Error sending SMS: {e}")
