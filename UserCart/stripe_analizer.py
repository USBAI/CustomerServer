import stripe
import firebase_admin
from firebase_admin import credentials, db
import os
from datetime import datetime
import time  # Import time module to add delay between iterations

# Set your Stripe secret key
stripe.api_key = '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'

# Path to Firebase credentials JSON file
FIREBASE_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'firebase_credentials.json')

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://users-95da3-default-rtdb.europe-west1.firebasedatabase.app/'
        })
    except FileNotFoundError as e:
        print(f"Firebase credentials file not found: {e}")

def check_payments_from_firebase():
    while True:  # Continuous loop to keep checking orders
        try:
            # Get a reference to the Firebase Realtime Database
            ref = db.reference('Orders')
            all_orders = ref.get()

            # Loop through all orders in Firebase
            for order_id, order_info in all_orders.items():
                payment_link = order_info.get('payment_link')
                user_id = order_info.get('user_id')

                if not payment_link:
                    print(f"No payment link found for order {order_id}")
                    continue

                print(f"Checking payment link for order {order_id}, user {user_id}: {payment_link}")

                # Query Stripe to see if there are any payments related to this link
                try:
                    payment_intents = stripe.PaymentIntent.list(limit=10)

                    for payment in payment_intents['data']:
                        try:
                            # Safely check if 'charges' exist in the payment object
                            if 'charges' in payment and len(payment['charges']['data']) > 0:
                                charge = payment['charges']['data'][0]
                                receipt_url = charge.get('receipt_url')
                                payment_date = datetime.fromtimestamp(payment['created']).strftime('%Y-%m-%d %H:%M:%S')

                                # Check if this payment link matches and the payment was successful
                                if receipt_url == payment_link and payment['status'] == 'succeeded':
                                    print(f"Payment successful for order {order_id} on {payment_date}.")
                                    print(f"Amount: {payment['amount'] / 100} {payment['currency'].upper()}")
                                    return  # Stop the loop when a successful payment is found
                                else:
                                    print(f"No successful payment found for order {order_id} with this payment link.")
                            else:
                                print(f"No charges found for payment intent {payment['id']} for order {order_id}.")
                        except KeyError as key_error:
                            print(f"Key error: {key_error} while processing payment for order {order_id}")
                except stripe.error.StripeError as e:
                    print(f"Stripe error for order {order_id}: {str(e)}")

            # If no successful payment is found, wait for a while and restart
            print("No successful payment found in this cycle. Restarting check...")
            time.sleep(1)  # Wait for 30 seconds before checking again (adjust as needed)

        except Exception as e:
            print(f"Error retrieving orders from Firebase: {e}")
            time.sleep(60)  # Wait for 1 minute before retrying if an error occurs

# Call the function to start checking payments
check_payments_from_firebase()
