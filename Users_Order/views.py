import stripe
import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
import firebase_admin
from firebase_admin import credentials, db
import uuid
from threading import Timer

# Path to Firebase credentials JSON file
FIREBASE_CREDENTIALS_PATH = "Users_Order/firebase_credentials.json"

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://users-95da3-default-rtdb.europe-west1.firebasedatabase.app/'
    })

# Set your Stripe secret key
stripe.api_key = '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'

def check_payment_status(payment_intent_id, order_id):
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        order_ref = db.reference(f'Orders/{order_id}')

        if payment_intent.status == 'succeeded':
            order_ref.update({'status': 'paid'})
            move_order_to_all_orders(order_id, order_ref)
            return True
        else:
            return False
    except stripe.error.StripeError as e:
        print(f"Stripe error: {str(e)}")
        return False

def move_order_to_all_orders(order_id, order_ref):
    try:
        all_orders_ref = db.reference('All_Orders')

        if not all_orders_ref.get():
            all_orders_ref.set({})

        all_orders = all_orders_ref.get()
        next_index = len(all_orders) + 1 if all_orders else 1
        new_order_ref = all_orders_ref.child(str(next_index))

        order_data = order_ref.get()
        new_order_ref.set(order_data)

        deactivate_payment_link(order_data['payment_intent_id'])
        order_ref.delete()
    except Exception as e:
        print(f"Error moving order to All_Orders: {str(e)}")

@api_view(['POST'])
def add_user_order(request):
    print("Incoming request data:", request.data)

    user_id = request.data.get('user_id')
    payment_link = request.data.get('payment_link')
    payment_intent_id = payment_link

    product_name = request.data.get('product_name')
    product_url = request.data.get('product_url')
    product_price = request.data.get('product_price')
    quantity = request.data.get('quantity')

    if not user_id or not product_name or not product_url or not product_price or not quantity or not payment_link:
        return Response({"error": "All fields are required."}, status=400)

    try:
        # Create a unique order ID using UUID
        order_id = str(uuid.uuid4())
        order_ref = db.reference(f'Orders/{order_id}')

        # Add order details under the new order folder
        order_data = {
            'user_id': user_id,
            'status': 'unpaid',
            'payment_link': payment_link,
            'payment_intent_id': payment_intent_id,
            'products': {
                'product_1': {
                    'product_name': product_name,
                    'product_url': product_url,
                    'product_price': product_price,
                    'quantity': quantity
                }
            }
        }

        order_ref.set(order_data)

        # Schedule the payment status check
        schedule_payment_check(payment_intent_id, order_id, payment_link)

        return Response({"message": f"Order {order_id} created successfully."}, status=200)

    except Exception as e:
        print("Error:", str(e))
        return Response({"error": str(e)}, status=500)
