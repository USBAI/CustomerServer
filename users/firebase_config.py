# firebase_config.py
import os
import firebase_admin
from firebase_admin import credentials, firestore

# Path to your Firebase service account key JSON file
cred_path = os.path.dirname(__file__) + '/firebase_credentials.json'

# Check if Firebase Admin SDK is not initialized
if not firebase_admin._apps:
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, name='users-95da3')  # Provide a unique app name

# Function to get Firestore client
def get_firestore_client():
    return firestore.client(app=firebase_admin.get_app(name='users-95da3'))
