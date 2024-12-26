import stripe
import time
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
import uuid


# Set your Stripe secret key
stripe.api_key = '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'

# MongoDB connection
MONGO_URI = "mongodb+srv://KluretUserDB:ojsgheotugfihjpeslufjpnöebkoNDEOwuflihsorufhgpdndxfouln@kluretai-users.bufni.mongodb.net/?retryWrites=true&w=majority&appName=KluretAI-Users"
client = MongoClient(MONGO_URI)
db = client['kluret_db']
customers_orders = db['CustomersOrders']



@api_view(['POST'])
def add_product_to_db(request):
    """
    Adds a product to the database with an initial status of 'unpaid' and includes a timestamp.
    """
    try:
        user_id = request.data.get('user_id')
        user_full_name = request.data.get('user_full_name')
        product_name = request.data.get('product_name')
        product_url = request.data.get('product_url')
        product_price = request.data.get('product_price')
        quantity = request.data.get('quantity')
        shipping_address = request.data.get('shipping_address')
        shipping_city = request.data.get('shipping_city')
        shipping_postal_code = request.data.get('shipping_postal_code')
        shipping_country = request.data.get('shipping_country')
        phone_number = request.data.get('phone_number')  # Optional
        terms_conditions_allowed = request.data.get('terms_conditions_allowed')  # Must be true

        if not user_id or not user_full_name or not product_name or not product_url or not product_price or not quantity or not shipping_address or not shipping_city or not shipping_postal_code or not shipping_country or terms_conditions_allowed is not True:
            return Response({"error": "All fields are required and terms and conditions must be allowed."}, status=400)

        # Create a unique order ID using UUID
        order_id = str(uuid.uuid4())

        # Prepare order data
        order_data = {
            '_id': order_id,
            'user_id': user_id,
            'user_full_name': user_full_name,
            'status': 'unpaid',
            'timestamp': datetime.utcnow(),
            'products': [
                {
                    'product_name': product_name,
                    'product_url': product_url,
                    'product_price': product_price,
                    'quantity': quantity
                }
            ],
            'shipping_info': {
                'address': shipping_address,
                'city': shipping_city,
                'postal_code': shipping_postal_code,
                'country': shipping_country
            },
            'phone_number': phone_number,  # Optional field
            'terms_conditions_allowed': terms_conditions_allowed  # Added field
        }

        # Insert order data into MongoDB
        customers_orders.insert_one(order_data)

        return Response({"message": f"Order {order_id} created successfully.", "order_id": order_id}, status=200)

    except Exception as e:
        print("Error:", str(e))
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
def process_payment(request):
    """
    Processes the payment and updates the database if the payment is successful.
    """
    try:
        payment_id = request.data.get('payment_id')
        payment_method = request.data.get('payment_method')  # e.g., card, klarna, apple pay
        user_id = request.data.get('user_id')

        if not payment_id or not payment_method or not user_id:
            return Response({"error": "All fields are required."}, status=400)

        # Retrieve the order using the payment ID and user ID
        order = customers_orders.find_one({
            'user_id': user_id,
            'payment_id': payment_id
        })

        if not order:
            return Response({"error": "Order not found."}, status=404)

        # Check the payment status using Stripe
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_id)

            if payment_intent.status == 'succeeded':
                # Update order status in MongoDB
                customers_orders.update_one(
                    {'_id': order['_id']},
                    {'$set': {
                        'status': 'paid',
                        'payment_method': payment_method
                    }}
                )

                return Response({"message": f"Order {order['_id']} payment successful."}, status=200)

            else:
                return Response({"error": "Payment not successful yet."}, status=400)

        except stripe.error.StripeError as e:
            print(f"Stripe error: {str(e)}")
            return Response({"error": "Payment processing error."}, status=500)

    except Exception as e:
        print("Error:", str(e))
        return Response({"error": str(e)}, status=500)
