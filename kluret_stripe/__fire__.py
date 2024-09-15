import os
import firebase_admin
from firebase_admin import credentials, db

# Path to Firebase credentials JSON file
FIREBASE_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'firebase_credentials.json')

# Initialize Firebase Admin SDK
def initialize_firebase():
    if not firebase_admin._apps:  # Avoid re-initialization if already initialized
        try:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://users-95da3-default-rtdb.europe-west1.firebasedatabase.app/'
            })
            print("Firebase initialized successfully.")
        except FileNotFoundError as e:
            print(f"Firebase credentials file not found: {e}")
            exit(1)

# Function to fetch username (folder) by User-ID
def fetch_user_name_by_user_id(user_id):
    """
    Fetch the username (folder) by their User-ID from Kluret_Users.
    """
    kluret_users_ref = db.reference('All_Users/Kluret_Users')
    kluret_users = kluret_users_ref.get()

    if kluret_users:
        for user_name, user_data in kluret_users.items():
            # Check if 'User-ID' exists in the folder and matches the provided user_id
            if isinstance(user_data, dict) and 'User-ID' in user_data:
                if user_data['User-ID'] == user_id:
                    print(f"Found matching user: {user_name} with User-ID: {user_id}")
                    return user_name  # Return the folder name (e.g., 'bolagatkluredotse')
            else:
                print(f"No 'User-ID' found in folder {user_name}")

    print(f"No matching user found for User-ID: {user_id}")
    return None

if __name__ == "__main__":
    # User-ID to search for
    user_id = "N9ElplZeAYVZpEGJzhWJIOag0wMPT"

    # Initialize Firebase
    initialize_firebase()

    # Fetch the username (folder) for the given user_id
    user_name = fetch_user_name_by_user_id(user_id)

    if user_name:
        print(f"The username (folder) for User-ID '{user_id}' is: {user_name}")
    else:
        print(f"Could not find a user with User-ID: {user_id}")
