import stripe
import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
import uuid
from threading import Timer

# Set your Stripe secret key
stripe.api_key = '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'

# MongoDB connection
MONGO_URI = "mongodb+srv://KluretUserDB:ojsgheotugfihjpeslufjpnöebkoNDEOwuflihsorufhgpdndxfouln@kluretai-users.bufni.mongodb.net/?retryWrites=true&w=majority&appName=KluretAI-Users"
client = MongoClient(MONGO_URI)
db = client['kluret_db']
customers_orders = db['CustomersOrders']

def check_payment_status(payment_intent_id, order_id):
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        if payment_intent.status == 'succeeded':
            # Update order status in MongoDB
            customers_orders.update_one(
                {'_id': order_id},
                {'$set': {'status': 'paid'}}
            )
            return True
        else:
            return False
    except stripe.error.StripeError as e:
        print(f"Stripe error: {str(e)}")
        return False

@api_view(['POST'])
def add_user_order(request):
    print("Incoming request data:", request.data)

    user_id = request.data.get('user_id')
    payment_id = request.data.get('payment_id')  # Payment ID as shown in the image
    product_name = request.data.get('product_name')
    product_url = request.data.get('product_url')
    product_price = request.data.get('product_price')
    quantity = request.data.get('quantity')

    if not user_id or not product_name or not product_url or not product_price or not quantity or not payment_id:
        return Response({"error": "All fields are required."}, status=400)

    try:
        # Create a unique order ID using UUID
        order_id = str(uuid.uuid4())

        # Prepare order data
        order_data = {
            '_id': order_id,
            'user_id': user_id,
            'status': 'unpaid',
            'payment_id': payment_id,
            'products': [
                {
                    'product_name': product_name,
                    'product_url': product_url,
                    'product_price': product_price,
                    'quantity': quantity
                }
            ]
        }

        # Insert order data into MongoDB
        customers_orders.insert_one(order_data)

        # Schedule the payment status check
        schedule_payment_check(payment_id, order_id)

        return Response({"message": f"Order {order_id} created successfully."}, status=200)

    except Exception as e:
        print("Error:", str(e))
        return Response({"error": str(e)}, status=500)

def schedule_payment_check(payment_id, order_id):
    def check():
        payment_success = check_payment_status(payment_id, order_id)
        if payment_success:
            print(f"Payment for order {order_id} succeeded.")
        else:
            print(f"Payment for order {order_id} failed or is still pending.")

    # Check payment status after a delay (e.g., 1 minute)
    Timer(60, check).start()