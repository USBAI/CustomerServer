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
