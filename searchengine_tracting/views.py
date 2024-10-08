from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import firebase_admin
from firebase_admin import credentials, db
import os
import random
import string

# Path to Firebase credentials JSON file for the second Firebase Realtime Database
FIREBASE_CREDENTIALS_FOR_TASK_PATH = os.path.join(os.path.dirname(__file__), 'bolagdb-c40e2-firebase-adminsdk-y8rnh-3905b9b493.json')

# Initialize Firebase Admin SDK for the second Realtime Database
try:
    cred_task = credentials.Certificate(FIREBASE_CREDENTIALS_FOR_TASK_PATH)
    firebase_admin.initialize_app(cred_task, {
        'databaseURL': 'https://bolagdb-c40e2-default-rtdb.europe-west1.firebasedatabase.app/',
        'storageBucket': 'bolagdb-c40e2.appspot.com'  # Replace with the actual bucket name if necessary
    }, name='bolagdb')
except FileNotFoundError as e:
    print(f"Firebase credentials file for tasks not found: {e}")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK for tasks: {str(e)}")

# Function to generate a unique alphanumeric string of length between 10-20 characters
def generate_unique_id(ref, length_range=(10, 20)):
    while True:
        length = random.randint(length_range[0], length_range[1])
        random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        
        # Check if the random_id already exists in the database
        if not ref.child(random_id).get():
            return random_id

@csrf_exempt  # Disable CSRF for testing purposes (not recommended for production)
def product_search_tracking(request):
    if request.method == 'POST':
        try:
            # Parse the request body
            data = json.loads(request.body)
            product_name = data.get('product_name', 'Unknown')
            response_status = data.get('response_status', 'Unknown')
            total_products_found = data.get('total_products_found', 0)

            # Print the search activity
            print(f"Product Searched: {product_name}")
            print(f"Response Status: {response_status}")
            print(f"Total Products Found: {total_products_found}")

            # Get Firebase app instance
            app = firebase_admin.get_app('bolagdb')
            ref = db.reference('Bolag_Kluret/Searchengine_Tracking', app=app)

            # Generate a unique folder name (random alphanumeric string) between 10 and 20 characters
            unique_id = generate_unique_id(ref)

            # Save the new product search data under the unique folder name
            ref.child(unique_id).set({
                'product_name': product_name,
                'response_status': response_status,
                'total_products_found': total_products_found
            })

            # Return a success response
            return JsonResponse({
                'message': 'Product search tracked successfully',
                'product_name': product_name,
                'response_status': response_status,
                'total_products_found': total_products_found,
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            print(f"Error tracking product search: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
