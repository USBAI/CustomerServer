from django.http import JsonResponse
from pymongo import MongoClient
import json
from django.views.decorators.csrf import csrf_exempt

# MongoDB connection settings
CONNECTSTORE_MONGO_URL = "mongodb+srv://ConnectStoreDB:iwrsohdgjokosdifgodJI0erjdfsigjoxigjfjb4poedfjpicedf@connectstores.vqiwf.mongodb.net/?retryWrites=true&w=majority&appName=ConnectStores"
CONNECTSTORE_DB_NAME = "ConnectStoreDB"
# Initialize MongoDB client and database
client = MongoClient(CONNECTSTORE_MONGO_URL)
db = client[CONNECTSTORE_DB_NAME]

# Define the collection
connect_store_server_collection = db['ConnectStoreServer']

@csrf_exempt
def get_store_info(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            store_id = data.get('store_id')  # Extract store_id from the JSON body
            
            if not store_id:
                return JsonResponse({'error': 'Store ID is required.'}, status=400)

            # Find the store by store_id
            store = connect_store_server_collection.find_one({'store_id': store_id}, {'_id': 0})
            
            if not store:
                return JsonResponse({'error': 'Store not found.'}, status=404)

            return JsonResponse({'store': store}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)



@csrf_exempt
def save_store_info(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            
            # Extract fields from the data
            store_id = data.get('store_id')
            store_name = data.get('store_name')
            store_email = data.get('store_email')
            phone_number = data.get('phone_number')
            store_currency = data.get('store_currency')
            street_address = data.get('street_address')
            city = data.get('city')
            postal_code = data.get('postal_code')
            country = data.get('country')

            # Validate required field: store_id
            if not store_id:
                return JsonResponse({'error': 'Store ID is required.'}, status=400)

            # Find the store by store_id
            store = connect_store_server_collection.find_one({'store_id': store_id})
            if not store:
                return JsonResponse({'error': 'Store not found.'}, status=404)

            # Prepare the update dictionary with non-empty fields
            update_fields = {}
            if store_name is not None:
                update_fields['store_name'] = store_name
            if store_email is not None:
                update_fields['store_email'] = store_email
            if phone_number is not None:
                update_fields['phone_number'] = phone_number
            if store_currency is not None:
                update_fields['store_currency'] = store_currency
            if street_address is not None:
                update_fields['street_address'] = street_address
            if city is not None:
                update_fields['city'] = city
            if postal_code is not None:
                update_fields['postal_code'] = postal_code
            if country is not None:
                update_fields['country'] = country

            # Update the store information in the database
            connect_store_server_collection.update_one(
                {'store_id': store_id},
                {'$set': update_fields}
            )

            return JsonResponse({'message': 'Store information updated successfully.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)
