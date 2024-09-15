import time
import threading
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Set your Stripe secret key and webhook secret
stripe.api_key = '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'
stripe_webhook_secret = 'whsec_9kfdlR7UdzvDCg0mbdW2xQokbtrLaIhh'


@csrf_exempt
def create_payment_and_poll_status(request):
    if request.method == 'POST':
        try:
            # Step 1: Parse the request data
            data = json.loads(request.body)
            user_id = data.get('user_id')
            product_description = data.get('product_description')
            total_cost = float(data.get('total_cost'))
            total_products = int(data.get('total_products'))

            # Step 2: Create a product in Stripe
            product = stripe.Product.create(
                name=f"Kluret User: {user_id}",
                description=f"Products: {product_description}",
            )

            # Step 3: Create a price for the product
            price = stripe.Price.create(
                product=product.id,
                unit_amount=int(total_cost * 100),  # Convert SEK to cents
                currency='sek',
            )

            # Step 4: Create a payment link
            payment_link = stripe.PaymentLink.create(
                line_items=[{
                    'price': price.id,
                    'quantity': total_products,  # Use total_products as quantity
                }],
                shipping_address_collection={
                    'allowed_countries': ['SE']  # Only allow shipping within Sweden
                },
                metadata={
                    'user_id': user_id,
                    'product_description': product_description
                }
            )

            # Step 5: Return the payment link URL to the frontend immediately
            response_data = {
                "status": "success",
                "payment_link": payment_link.url,
                "payment_link_id": payment_link.id
            }
            print(f"Payment link created: {payment_link.url}")

            # Start background thread to poll for payment status
            thread = threading.Thread(target=poll_payment_status, args=(payment_link.id,))
            thread.start()

            return JsonResponse(response_data)

        except stripe.error.StripeError as e:
            # Handle Stripe errors
            print(f"Stripe error: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

        except Exception as e:
            # Handle other general errors
            print(f"Error: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


def poll_payment_status(payment_link_id):
    # Step 6: Polling the payment link status every second, up to 1000 retries
    retries = 1000
    while retries > 0:
        retries -= 1

        try:
            # Fetch the sessions tied to the payment link
            sessions = stripe.checkout.Session.list(payment_link=payment_link_id)

            if sessions and sessions['data']:
                session = sessions['data'][0]

                # Check if the payment status is 'paid'
                if session['payment_status'] == 'paid':
                    # Disable the payment link after successful payment
                    stripe.PaymentLink.modify(payment_link_id, active=False)
                    print(f"Payment for link {payment_link_id} has been paid and deactivated.")
                    break
                else:
                    print(f"Payment link {payment_link_id} is not yet paid. Status: {session['payment_status']}")
            else:
                print(f"No active session found for the payment link {payment_link_id}.")
        
        except Exception as e:
            print(f"Error while polling payment status: {e}")

        # Wait for 1 second before checking again
        time.sleep(1)

    if retries == 0:
        print(f"Payment link {payment_link_id} has not been paid after 1000 retries.")
