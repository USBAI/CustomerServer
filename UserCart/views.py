from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
import os

# MongoDB connection settings
MONGO_URI = "mongodb+srv://KluretUserDB:ojsgheotugfihjpeslufjpnöebkoNDEOwuflihsorufhgpdndxfouln@kluretai-users.bufni.mongodb.net/?retryWrites=true&w=majority&appName=KluretAI-Users"  # Update this with your MongoDB URI
DB_NAME = "kluret_db"
CART_COLLECTION_NAME = "cart"

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
cart_collection = db[CART_COLLECTION_NAME]

class UserCartView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('UserID')

        # Check if UserID is provided
        if not user_id:
            return Response({'error': 'UserID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Query the cart collection to find all products for the given user_id
            user_cart = cart_collection.find_one({"User-ID": user_id})

            if user_cart and 'products' in user_cart:
                # Return the cart products
                return Response(user_cart['products'], status=status.HTTP_200_OK)
            else:
                # Cart is empty or user doesn't exist in the cart collection
                return Response({'error': 'Cart is empty or not available'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(f"Error: {e}")  # Log the error to the server console
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AdminCartView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Query the cart collection to find all cart data
            all_carts = list(cart_collection.find({}, {"_id": 0}))

            # Check if any carts exist
            if not all_carts:
                return Response({'message': 'No carts found'}, status=status.HTTP_404_NOT_FOUND)

            # Return all cart data
            return Response({'carts': all_carts}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error fetching carts: {e}")  # Log the error to the server console
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
