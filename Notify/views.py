from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
from datetime import datetime
from twilio.rest import Client

# Twilio configuration
TWILIO_ACCOUNT_SID = 'ACd0f9c45cb4f7904a51b4c6412d25bc68'
TWILIO_AUTH_TOKEN = 'dc2b567d27a0fe3b9c9606fdffc329e4'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # Twilio WhatsApp Sandbox number
WHATSAPP_RECIPIENT_NUMBER = 'whatsapp:+46727759188'  # Verified WhatsApp recipient

# MongoDB configuration
MONGO_URI = "mongodb+srv://KluretUserDB:ojsgheotugfihjpeslufjpnöebkoNDEOwuflihsorufhgpdndxfouln@kluretai-users.bufni.mongodb.net/?retryWrites=true&w=majority&appName=KluretAI-Users"
DB_NAME = "kluret_db"

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

class EmailListCreate(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Insert email into MongoDB
            emails_collection = db["emails"]
            emails_collection.insert_one({'email': email, 'timestamp': datetime.utcnow()})
            return Response({'message': 'Email saved successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VisitorCreate(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Extract data from the request
            timestamp = request.data.get('timestamp')
            platform = request.data.get('platform')
            language = request.data.get('language')
            browser = request.data.get('browser')
            latitude = request.data.get('latitude')
            longitude = request.data.get('longitude')

            # Validate required fields
            if not timestamp or not platform or not language:
                return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

            # Insert visitor info into MongoDB collection "SiteTraffics"
            site_traffics_collection = db["SiteTraffics"]
            site_traffics_collection.insert_one({
                'timestamp': timestamp,
                'platform': platform,
                'language': language,
                'browser': browser,
                'location': {
                    'latitude': latitude,
                    'longitude': longitude
                }
            })
            
            # Count the total number of visitors in the "SiteTraffics" collection
            total_visitor_count = site_traffics_collection.count_documents({})

            # Send WhatsApp message via Twilio
            self.send_whatsapp_message(total_visitor_count)

            return Response({'message': 'Visitor recorded successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def send_whatsapp_message(self, total_visitor_count):
        try:
            # Initialize Twilio client
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            # Compose the WhatsApp message
            message_body = f"Hello Kluret, your platform currently has {total_visitor_count} visitors."

            # Send the message via WhatsApp
            message = client.messages.create(
                body=message_body,
                from_=TWILIO_WHATSAPP_NUMBER,
                to=WHATSAPP_RECIPIENT_NUMBER
            )

            print(f"WhatsApp message sent successfully: {message.sid}")
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")

    def get(self, request, *args, **kwargs):
        try:
            # Retrieve total number of visitors from the "SiteTraffics" collection
            site_traffics_collection = db["SiteTraffics"]
            total_visitor_count = site_traffics_collection.count_documents({})

            return Response({'total_visitors': total_visitor_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SiteTrafficList(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Access the MongoDB collection
            site_traffics_collection = db["SiteTraffics"]

            # Retrieve all documents from the collection
            all_traffic = list(site_traffics_collection.find({}, {'_id': 0}))

            # Return the data as a JSON response
            return Response({'site_traffic': all_traffic}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
