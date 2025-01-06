from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
import datetime
import stripe

# MongoDB connection settings
MONGO_URI = "mongodb+srv://KluretUserDB:ojsgheotugfihjpeslufjpnöebkoNDEOwuflihsorufhgpdndxfouln@kluretai-users.bufni.mongodb.net/?retryWrites=true&w=majority&appName=KluretAI-Users"  # Update this with your MongoDB URI
DB_NAME = "kluret_db"
USERS_COLLECTION = "Kluret_Users"
CART_COLLECTION = "cart"
ORDER_COLLECTIONS = "orders"
stripe.api_key = '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'


# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db[USERS_COLLECTION]
cart_collection = db[CART_COLLECTION]
order_collection = db[ORDER_COLLECTIONS]


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




@api_view(['POST'])
def place_order(request):
    user_id = request.data.get('user_id')
    stripe_payment_id = request.data.get('payment_id')
    print(f"user id {user_id}")
    print(f"Stripe PaymentID {stripe_payment_id}")

    if not user_id or not stripe_payment_id:
        return Response({'error': 'UserID and StripePaymentID are required'}, status=400)

    try:
        # Verify payment using Stripe
        try:
            # Retrieve the payment intent from Stripe
            payment_intent = stripe.PaymentIntent.retrieve(stripe_payment_id)
            print(f"Stripe PaymentIntent: {payment_intent}")

            # Check if the payment intent's status is 'succeeded'
            if payment_intent.get('status') != 'succeeded':
                return Response({'error': 'Payment verification failed or payment not succeeded'}, status=400)
        except stripe.error.StripeError as e:
            print(f"Stripe API error: {e}")
            return Response({'error': 'Stripe API error'}, status=500)
        except Exception as e:
            print(f"Unexpected error during payment verification: {e}")
            return Response({'error': 'Unexpected error during payment verification'}, status=500)

        # Fetch user's cart
        user_cart = cart_collection.find({"User-ID": user_id})

        if not user_cart:
            return Response({'error': 'Cart is empty or not available'}, status=404)

        # Prepare order details
        products = list(user_cart)
        order = {
            "User-ID": user_id,
            "products": products,
            "StripePaymentID": stripe_payment_id,
            "order_date": datetime.datetime.utcnow()
        }
        order_collection.insert_one(order)

        # Clear only this user's cart
        cart_collection.delete_many({"User-ID": user_id})

        return Response({'message': 'Order placed successfully'}, status=200)

    except Exception as e:
        print(f"Error: {e}")
        return Response({'error': str(e)}, status=500)



@api_view(['POST'])
def get_user_orders(request):
    # Extract the user_id from the request
    user_id = request.data.get('user_id')  # Fixed key to match POST request body format
    print(f"user_id: {user_id}")

    if not user_id:
        return Response({'error': 'UserID is required'}, status=400)

    try:
        # Fetch user's orders from the orders collection
        user_orders = list(order_collection.find({"User-ID": user_id}))
        
        # Convert ObjectId fields to strings for JSON serialization
        for order in user_orders:
            if "_id" in order:
                order["_id"] = str(order["_id"])  # Convert ObjectId to string

            # If the order contains products with nested ObjectId, handle them as well
            if "products" in order and isinstance(order["products"], list):
                for product in order["products"]:
                    if "_id" in product:
                        product["_id"] = str(product["_id"])  # Convert nested ObjectId to string

        # Check if the user has orders
        if not user_orders:
            return Response({'message': 'No orders found for this user'}, status=404)

        # Return the orders
        return Response({'orders': user_orders}, status=200)

    except Exception as e:
        print(f"Error fetching user orders: {e}")  # Log the error for debugging
        return Response({'error': str(e)}, status=500)