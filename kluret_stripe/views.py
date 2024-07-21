import stripe
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.http import JsonResponse

# Set your Stripe secret key here
stripe.api_key = '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'

@method_decorator(csrf_exempt, name='dispatch')
class CollectDataView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        user_id = data.get('user_id')
        product_description = data.get('product_description')
        total_cost = float(data.get('total_cost'))
        total_products = int(data.get('total_products'))

        # Create a product
        product = stripe.Product.create(
            name=f"Kluret User: {user_id}",
            description=f"Products: {product_description}",
        )

        # Create a price for the product
        price = stripe.Price.create(
            product=product.id,
            unit_amount=int(total_cost * 100),  # Convert dollars to cents
            currency='Sek',
        )

        # Create a payment link
        try:
            payment_link = stripe.PaymentLink.create(
                line_items=[
                    {
                        'price': price.id,
                        'quantity': 1,  # Use total_products as quantity
                    },
                ],
            )

            # Return the payment link URL to the frontend
            return JsonResponse({"status": "success", "payment_link": payment_link.url})

        except stripe.error.StripeError as e:
            # Handle Stripe errors
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

        except Exception as e:
            # Handle other errors
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
