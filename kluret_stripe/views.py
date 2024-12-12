import time
import threading
import stripe
import os
import firebase_admin
from firebase_admin import credentials, db
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Set your Stripe secret key
stripe.api_key = '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'

# Path to Firebase credentials JSON file
FIREBASE_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'firebase_credentials.json')

# Initialize Firebase Admin SDK
def initialize_firebase():
    if not firebase_admin._apps:  # Avoid re-initialization if already initialized
        try:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://users-95da3-default-rtdb.europe-west1.firebasedatabase.app/'
            })
            print("Firebase initialized successfully.")
        except FileNotFoundError as e:
            print(f"Firebase credentials file not found: {e}")
            exit(1)

if not firebase_admin._apps:
    initialize_firebase()

@csrf_exempt
def create_payment_intent(request):
    if request.method == 'POST':
        try:
            # Step 1: Parse the request data
            data = json.loads(request.body)
            user_id = data.get('user_id')
            product_description = data.get('product_description')
            total_cost = float(data.get('total_cost'))
            currency = data.get('currency', 'usd').lower()

            # Step 2: Create a PaymentIntent in Stripe
            payment_intent = stripe.PaymentIntent.create(
                amount=int(total_cost * 100),  # Convert amount to smallest currency unit
                currency=currency,
                metadata={
                    'user_id': user_id,
                    'product_description': product_description
                }
            )

            # Step 3: Return the client secret to the frontend for confirmation
            response_data = {
                "status": "success",
                "client_secret": payment_intent.client_secret,
                "payment_intent_id": payment_intent.id
            }
            print(f"PaymentIntent created: {payment_intent.id}")

            return JsonResponse(response_data)

        except stripe.error.StripeError as e:
            print(f"Stripe error: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@csrf_exempt
def confirm_payment(request):
    if request.method == 'POST':
        try:
            # Parse the request data
            data = json.loads(request.body)
            payment_intent_id = data.get('payment_intent_id')
            user_id = data.get('user_id')

            # Retrieve the PaymentIntent from Stripe
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            if payment_intent.status == 'succeeded':
                # Fetch user name from Kluret_Users using User-ID
                user_name = fetch_user_name_by_user_id(user_id)
                if user_name:
                    # Move paid products from user's cart to "paid_products"
                    update_firebase_after_payment(user_name, payment_intent_id)
                else:
                    print(f"User with ID {user_id} not found in Kluret_Users.")

                return JsonResponse({"status": "success", "message": "Payment confirmed and processed."})
            else:
                return JsonResponse({"status": "error", "message": "Payment not successful."})

        except stripe.error.StripeError as e:
            print(f"Stripe error: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

# Helper functions

def fetch_user_name_by_user_id(user_id):
    kluret_users_ref = db.reference('All_Users/Kluret_Users')
    kluret_users = kluret_users_ref.get()

    if kluret_users:
        for user_name, user_data in kluret_users.items():
            if isinstance(user_data, dict) and 'User-ID' in user_data:
                if user_data['User-ID'] == user_id:
                    print(f"Found matching user: {user_name} with User-ID: {user_id}")
                    return user_name

    print(f"No matching user found for User-ID: {user_id}")
    return None

def update_firebase_after_payment(user_name, payment_intent_id):
    ref = db.reference(f'All_Users/Kluret_Users/{user_name}/MyCart')
    cart_items = ref.get()

    if cart_items:
        print(f"Cart items for user {user_name}: {cart_items}")
        paid_products_ref = db.reference(f'All_Users/Kluret_Users/{user_name}/paid_products')
        paid_products = paid_products_ref.get()

        if not paid_products:
            paid_products = []

        for key, item in cart_items.items():
            paid_products_ref.push(item)

        ref.delete()
        print(f"All items in the cart for user {user_name} have been moved to 'paid_products'.")
    else:
        print(f"No cart items found for user {user_name}.")
