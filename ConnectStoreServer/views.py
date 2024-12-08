from django.http import JsonResponse
from pymongo import MongoClient
import json
import random
import string
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


@csrf_exempt
def save_customer(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            
            store_id = data.get('store_id')  # The store ID to associate the customer with
            customer_email = data.get('email')  # Email of the customer (required)

            # Validate required fields
            if not store_id or not customer_email:
                return JsonResponse({'error': 'Store ID and customer email are required.'}, status=400)

            # Find the store by store_id
            store = connect_store_server_collection.find_one({'store_id': store_id})
            if not store:
                return JsonResponse({'error': 'Store not found.'}, status=404)

            # Calculate the next customer index
            current_customers = store.get('Customers', [])
            next_index = len(current_customers) + 1

            # Create the customer object
            customer = {
                'index': next_index,
                'email': customer_email,
                'name': data.get('name', ""),
                'phone': data.get('phone', ""),
                'location': data.get('location', ""),
                'lastOrder': data.get('lastOrder', ""),
                'orders': data.get('orders', ""),
                'totalSpent': data.get('totalSpent', "")
            }

            # Add the customer to the Customers array
            connect_store_server_collection.update_one(
                {'store_id': store_id},
                {'$push': {'Customers': customer}}
            )

            return JsonResponse({'message': 'Customer added successfully.', 'customer_index': next_index}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)




@csrf_exempt
def save_order(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            
            store_id = data.get('store_id')  # The store ID to associate the order with

            # Validate required field
            if not store_id:
                return JsonResponse({'error': 'Store ID is required.'}, status=400)

            # Check if the store exists
            store = connect_store_server_collection.find_one({'store_id': store_id})
            if not store:
                return JsonResponse({'error': 'Store not found.'}, status=404)

            # Generate a unique order ID
            while True:
                # Generate a random 6-character alphanumeric string
                order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                
                # Check if the generated order_id already exists in the Orders array
                existing_order = connect_store_server_collection.find_one(
                    {'store_id': store_id, 'Orders.order_id': order_id}
                )
                
                if not existing_order:  # If no duplicate, break the loop
                    break

            # Create the order object
            order = {
                'order_id': order_id,
                'customer': data.get('customer', ""),
                'date': data.get('date', ""),
                'items': data.get('items', ""),
                'total': data.get('total', ""),
                'status': data.get('status', ""),
                'payment': data.get('payment', "")
            }

            # Add the order to the Orders array
            connect_store_server_collection.update_one(
                {'store_id': store_id},
                {'$push': {'Orders': order}}
            )

            return JsonResponse({'message': 'Order added successfully.', 'order_id': order_id}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)
