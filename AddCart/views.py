from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient

# MongoDB connection settings
MONGO_URI = "mongodb+srv://KluretUserDB:ojsgheotugfihjpeslufjpnöebkoNDEOwuflihsorufhgpdndxfouln@kluretai-users.bufni.mongodb.net/?retryWrites=true&w=majority&appName=KluretAI-Users"  # Update this with your MongoDB URI
DB_NAME = "kluret_db"
USERS_COLLECTION = "Kluret_Users"
CART_COLLECTION = "cart"

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db[USERS_COLLECTION]
cart_collection = db[CART_COLLECTION]

@api_view(['POST'])
def add_to_cart(request):
    # Extract the data from the request
    user_id = request.data.get('user_id')
    product_name = request.data.get('product_name')
    product_price = request.data.get('product_price')
    product_color = request.data.get('product_color', '')
    product_size = request.data.get('product_size', '')
    product_description = request.data.get('product_description', '')
    product_image = request.data.get('product_image')
    product_url = request.data.get('product_url')

    # Check if the user exists in the users collection
    user = users_collection.find_one({"User-ID": user_id})

    if user:
        # Add the product to the cart collection
        cart_collection.insert_one({
            "User-ID": user_id,
            "product_name": product_name,
            "product_price": product_price,
            "product_color": product_color,
            "product_size": product_size,
            "product_description": product_description,
            "product_image": product_image,
            "product_url": product_url
        })
        return Response({"message": "Item added to cart successfully"}, status=201)
    else:
        return Response({"message": "User not found"}, status=404)

@api_view(['POST'])
def get_cart(request):
    # Extract the user_id from the request
    user_id = request.data.get('user_id')

    # Check if the user exists in the users collection
    user = users_collection.find_one({"User-ID": user_id})

    if user:
        # Fetch the user's cart items from the cart collection
        cart_items = list(cart_collection.find({"User-ID": user_id}, {"_id": 0}))

        if cart_items:
            return Response({"cart_items": cart_items}, status=200)
        else:
            return Response({"message": "Cart is empty"}, status=200)
    else:
        return Response({"message": "User not found"}, status=404)

@api_view(['POST'])
def remove_from_cart(request):
    # Extract the user_id and product_url from the request
    user_id = request.data.get('user_id')
    product_url = request.data.get('product_url')

    # Check if the user exists in the users collection
    user = users_collection.find_one({"User-ID": user_id})

    if user:
        # Find and delete the product in the cart collection
        result = cart_collection.delete_one({"User-ID": user_id, "product_url": product_url})

        if result.deleted_count > 0:
            return Response({"message": "Item removed from cart successfully"}, status=200)
        else:
            return Response({"message": "Item not found in cart"}, status=404)
    else:
        return Response({"message": "User not found"}, status=404)
