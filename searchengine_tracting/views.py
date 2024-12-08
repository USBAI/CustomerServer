from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
import string
from pymongo import MongoClient
from datetime import datetime

# MongoDB configuration
MONGO_URI = "mongodb+srv://KluretUserDB:ojsgheotugfihjpeslufjpnöebkoNDEOwuflihsorufhgpdndxfouln@kluretai-users.bufni.mongodb.net/?retryWrites=true&w=majority&appName=KluretAI-Users"  # Update this with your MongoDB URI
DB_NAME = "kluret_db"

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Function to generate a unique alphanumeric string of length between 10-20 characters
def generate_unique_id(length_range=(10, 20)):
    length = random.randint(length_range[0], length_range[1])
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

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

            # Access the MongoDB collection
            collection = db["ProductSearchTracking"]

            # Generate a unique folder name (random alphanumeric string)
            unique_id = generate_unique_id()

            # Save the new product search data in the MongoDB collection
            collection.insert_one({
                'unique_id': unique_id,
                'product_name': product_name,
                'response_status': response_status,
                'total_products_found': total_products_found,
                'timestamp': datetime.utcnow()
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

    elif request.method == 'GET':
        try:
            # Access the MongoDB collection
            collection = db["ProductSearchTracking"]

            # Fetch all data from the MongoDB collection
            all_data = list(collection.find({}, {'_id': 0}))  # Exclude MongoDB's default `_id` field

            if not all_data:
                return JsonResponse({'message': 'No data found'}, status=404)

            # Return the data as a JSON response
            return JsonResponse(all_data, safe=False, status=200)

        except Exception as e:
            print(f"Error fetching product search data: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)

    return JsonResponse({'error': 'Only POST and GET requests are allowed'}, status=405)
