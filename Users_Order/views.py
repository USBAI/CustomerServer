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
        # Check the payment status using the payment_intent_id
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        # Get the user's order reference in Firebase
        user_order_ref = db.reference(f'User_Orders/{user_id}/{order_id}')

        if payment_intent.status == 'succeeded':
            # If the payment succeeded, update the order status in Firebase
            user_order_ref.update({'status': 'paid'})
            print("Payment succeeded, order marked as paid.")
            
            # Move order to All_Orders
            move_order_to_all_orders(user_id, order_id, user_order_ref)
            
            return True
        else:
            return False
    except stripe.error.StripeError as e:
        print(f"Stripe error: {str(e)}")
        return False

def move_order_to_all_orders(user_id, order_id, user_order_ref):
    try:
        # Reference to the 'All_Orders' node in Firebase
        all_orders_ref = db.reference('All_Orders')

        # Check if the All_Orders folder exists, if not, create it
        if not all_orders_ref.get():
            all_orders_ref.set({})

        # Find the next available index
        all_orders = all_orders_ref.get()
        next_index = len(all_orders) + 1 if all_orders else 1

        # Create a new folder with the next index
        order_folder_ref = all_orders_ref.child(str(next_index))

        # Get the order data
        order_data = user_order_ref.get()

        # Move the order data to the new folder
        order_folder_ref.set(order_data)

        print(f"Order {order_id} moved to All_Orders/{next_index}.")

        # Deactivate the payment link
        deactivate_payment_link(order_data['payment_intent_id'])

        # Delete the original order from User_Orders
        user_order_ref.delete()

    except Exception as e:
        print(f"Error moving order to All_Orders: {str(e)}")

def deactivate_payment_link(payment_intent_id):
    try:
        # Deactivate the payment link by canceling the PaymentIntent
        stripe.PaymentIntent.cancel(payment_intent_id)
        print(f"Payment intent {payment_intent_id} canceled.")
    except stripe.error.StripeError as e:
        print(f"Error canceling payment intent: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

def schedule_payment_check(payment_intent_id, user_id, order_id, payment_link, interval=5, duration=600):  # 600 seconds = 10 minutes
    elapsed_time = 0

    def check_and_reschedule():
        nonlocal elapsed_time
        payment_successful = check_payment_status(payment_intent_id, user_id, order_id)
        if payment_successful:
            print("Stopping further checks as payment was successful.")
        else:
            elapsed_time += interval
            print(f"Elapsed time: {elapsed_time} seconds")
            if elapsed_time < duration:
                print(f"Payment not yet received, checking again in {interval} seconds...")
                Timer(interval, check_and_reschedule).start()
            else:
                # If payment is still not done after the duration, delete the order and payment link
                delete_order_and_payment_link(user_id, order_id, payment_intent_id)
                print(f"Payment not received within {duration} seconds, order {order_id} and payment link deleted.")

    print("Starting payment check...")
    Timer(interval, check_and_reschedule).start()

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
