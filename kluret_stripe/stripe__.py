import stripe

# Set your secret key. Remember to switch to your live secret key in production!
stripe.api_key = ''

try:
    # Create a product
    product = stripe.Product.create(
        name="T-shirt",
        description="Comfortable cotton t-shirt",
    )

    # Create a price for the product
    price = stripe.Price.create(
        product=product.id,
        unit_amount=2000,  # Amount in cents (2000 cents = $20)
        currency='usd',
    )

    # Create a payment link
    payment_link = stripe.PaymentLink.create(
        line_items=[
            {
                'price': price.id,
                'quantity': 1,
            },
        ],
    )

    # Print the payment link URL
    print(f"Payment link created: {payment_link.url}")

except stripe.error.StripeError as e:
    # Handle error
    print(f"Stripe error: {e}")

except Exception as e:
    # Handle general error
    print(f"An error occurred: {e}")
