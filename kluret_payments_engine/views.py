import stripe
from datetime import datetime

# Set your secret key. You should ideally store this securely.
stripe.api_key = "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"

# Function to convert UNIX timestamp to human-readable date
def convert_timestamp(unix_timestamp):
    return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Retrieve the list of charges/payments
payments = stripe.PaymentIntent.list(limit=10)  # Adjust the limit as needed

# Iterate through the payments and print relevant data
for payment in payments.data:
    amount = payment.amount / 100  # Stripe returns amounts in cents, so convert to the main currency unit
    currency = payment.currency.upper()
    status = payment.status
    payment_method = payment.payment_method_types[0] if payment.payment_method_types else "Unknown method"
    
    # Check if the payment has charges and the charges data is available
    if hasattr(payment, 'charges') and payment.charges.data:
        customer_email = payment.charges.data[0].billing_details.email
    else:
        customer_email = "No email"
    
    payment_date = convert_timestamp(payment.created)
    
    # Try to retrieve the PaymentLink if available
    payment_link_id = payment.metadata.get('payment_link')  # Assuming it's stored in metadata
    if payment_link_id:
        # Fetch the PaymentLink
        payment_link = stripe.PaymentLink.retrieve(payment_link_id)
        payment_url = payment_link.url
    else:
        payment_url = "No Payment Link available"
    
    # Print all the information
    print(f"Amount: {amount} {currency}")
    print(f"Status: {status}")
    print(f"Payment method: {payment_method}")
    print(f"Customer email: {customer_email}")
    print(f"Payment date: {payment_date}")
    print(f"Payment Link: {payment_url}")
    print("-" * 40)
