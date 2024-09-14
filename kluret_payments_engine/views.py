import stripe
from datetime import datetime

# Set your Stripe secret key
stripe.api_key = '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'

def list_all_payments():
    try:
        # Pagination parameters
        has_more = True
        starting_after = None
        
        # Print header
        print(f"{'Amount':<10} {'Currency':<10} {'Status':<15} {'Payment Method':<20} {'Date':<20} {'Customer Email':<30} {'Payment Intent ID'}")
        print('-' * 120)

        # Loop through all pages of payment intents
        while has_more:
            # Fetch payment intents (maximum 100 at a time)
            payment_intents = stripe.PaymentIntent.list(limit=100, starting_after=starting_after)

            # Check if we received any data
            if not payment_intents['data']:
                print("No payment intents found.")
                return

            # Iterate over each payment intent
            for payment in payment_intents['data']:
                # Debug: Print payment intent raw data (optional)
                # print(payment)  # Uncomment this line if you need to debug the raw data

                # Check if charges exist, and get the first charge if available
                if 'charges' in payment and len(payment['charges']['data']) > 0:
                    for charge in payment['charges']['data']:
                        payment_method_details = charge.get('payment_method_details', {})
                        payment_method = payment_method_details.get('type', 'N/A').capitalize()
                        customer_email = payment.get('receipt_email', 'N/A')
                        amount = charge['amount'] / 100  # Convert amount from cents
                        currency = charge['currency'].upper()
                        payment_date = datetime.fromtimestamp(payment['created']).strftime('%Y-%m-%d %H:%M:%S')
                        payment_intent_id = payment['id']
                        status = payment['status'].capitalize()

                        # Print the details in a format similar to your Stripe dashboard
                        print(f"{amount:<10} {currency:<10} {status:<15} {payment_method:<20} {payment_date:<20} {customer_email:<30} {payment_intent_id}")
                else:
                    # In case there are no charges associated, print basic info
                    print(f"No charges found for payment intent {payment['id']} with status {payment['status']}.")

            # Prepare for the next batch of results
            has_more = payment_intents['has_more']
            if has_more:
                starting_after = payment_intents['data'][-1]['id']

    except stripe.error.StripeError as e:
        print(f"Stripe API error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to print all payments
list_all_payments()
