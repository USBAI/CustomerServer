import stripe

# Set your Stripe secret key
stripe.api_key = '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'

def deactivate_all_payment_links():
    try:
        # Initialize an empty list to store all payment links
        all_payment_links = []

        # Retrieve payment links in batches (Stripe pagination)
        payment_links = stripe.PaymentLink.list(limit=100)
        all_payment_links.extend(payment_links['data'])

        # Continue fetching payment links if more are available
        while payment_links.has_more:
            payment_links = stripe.PaymentLink.list(limit=100, starting_after=payment_links['data'][-1]['id'])
            all_payment_links.extend(payment_links['data'])

        # Loop through each payment link and deactivate if it's active
        for link in all_payment_links:
            if link['active']:
                stripe.PaymentLink.modify(link['id'], active=False)
                print(f"Deactivated Payment Link ID: {link['id']}")

        print("All payment links have been processed and deactivated if they were active.")
    
    except stripe.error.StripeError as e:
        print(f"Stripe error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

# Call the function to deactivate all payment links
deactivate_all_payment_links()
