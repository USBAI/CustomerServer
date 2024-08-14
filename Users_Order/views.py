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

def check_payment_status(payment_intent_id, user_id, order_id):
    try:
        # Check the payment status using the payment_intent_id (currently simulated with payment_link)
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        # Get the user's order reference in Firebase
        user_order_ref = db.reference(f'User_Orders/{user_id}/{order_id}')

        if payment_intent.status == 'succeeded':
            # If the payment succeeded, update the order status in Firebase
            user_order_ref.update({'status': 'paid'})
            print("Payment succeeded, order marked as paid.")
            return True
        else:
            return False
    except stripe.error.StripeError as e:
        print(f"Stripe error: {str(e)}")
        return False

def delete_order_and_payment_link(user_id, order_id, payment_link):
    # Delete the order from Firebase
    user_order_ref = db.reference(f'User_Orders/{user_id}/{order_id}')
    user_order_ref.delete()
    print(f"Order {order_id} deleted.")

    # Cancel the payment intent (if this functionality is required)
    # If the payment link corresponds to a Stripe Checkout Session or PaymentIntent, you may need to cancel it.
    try:
        # If payment_intent_id is the actual intent ID, you can cancel it:
        # stripe.PaymentIntent.cancel(payment_intent_id)
        # or if it's a checkout session, you can expire it
        stripe.checkout.Session.expire(payment_link)
        print(f"Payment link {payment_link} expired.")
    except Exception as e:
        print(f"Error while trying to cancel payment: {str(e)}")

def schedule_payment_check(payment_intent_id, user_id, order_id, payment_link, interval=5, duration=60):
    elapsed_time = 0

    def check_and_reschedule():
        nonlocal elapsed_time
        if elapsed_time < duration:
            payment_successful = check_payment_status(payment_intent_id, user_id, order_id)
            if not payment_successful:
                elapsed_time += interval
                Timer(interval, check_and_reschedule).start()
            else:
                print("Stopping further checks as payment was successful.")
        else:
            # If payment is still not done after the duration, delete the order and payment link
            delete_order_and_payment_link(user_id, order_id, payment_link)
            print(f"Payment not received within {duration} seconds, order {order_id} and payment link deleted.")

    check_and_reschedule()

@api_view(['POST'])
def add_user_order(request):
    # Log the incoming request data
    print("Incoming request data:", request.data)
    
    # Extract user_id, product details, and payment link from the request
    user_id = request.data.get('user_id')
    product_name = request.data.get('product_name')
    product_url = request.data.get('product_url')
    product_price = request.data.get('product_price')
    quantity = request.data.get('quantity')
    payment_link = request.data.get('payment_link')
    payment_intent_id = payment_link  # Use the payment link as a stand-in for payment_intent_id

    # Log extracted values
    print("Extracted values:")
    print("User ID:", user_id)
    print("Product Name:", product_name)
    print("Product URL:", product_url)
    print("Product Price:", product_price)
    print("Quantity:", quantity)
    print("Payment Link:", payment_link)
    print("Payment Intent ID:", payment_intent_id)

    # Check if all required fields are present
    if not user_id or not product_name or not product_url or not product_price or not quantity or not payment_link:
        return Response({"error": "All fields are required."}, status=400)

    try:
        # Reference to the 'User_Orders' node in Firebase
        user_orders_ref = db.reference('User_Orders')

        # Check if the user already has an order folder
        user_ref = user_orders_ref.child(user_id)

        # If the user folder doesn't exist, create it
        if not user_ref.get():
            user_ref.set({})

        # Generate a unique order ID for this product entry
        order_id = str(uuid.uuid4())

        # Create the product data dictionary
        product_data = {
            'product_name': product_name,
            'product_url': product_url,
            'product_price': product_price,
            'quantity': quantity,
            'payment_link': payment_link,
            'status': 'unpaid',  # Start with unpaid status
            'payment_intent_id': payment_intent_id  # Store the payment intent ID
        }

        # Save the product data under the unique order ID within the user's folder
        user_ref.child(order_id).set(product_data)

        # Schedule the payment status check
        schedule_payment_check(payment_intent_id, user_id, order_id, payment_link)

        return Response({"message": "Product added to user orders successfully."}, status=200)

    except Exception as e:
        print("Error:", str(e))
        return Response({"error": str(e)}, status=500)
