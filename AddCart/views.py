from rest_framework.decorators import api_view
from rest_framework.response import Response
import firebase_admin
from firebase_admin import credentials, db

# Path to Firebase credentials JSON file
FIREBASE_CREDENTIALS_PATH = "AddCart/firebase_credentials.json"

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://users-95da3-default-rtdb.europe-west1.firebasedatabase.app/'
    })

@api_view(['POST'])
def add_to_cart(request):
    # Extract the data from the request
    user_id = request.data.get('user_id')
    product_name = request.data.get('product_name')
    product_price = request.data.get('product_price')
    product_color = request.data.get('product_color', '')
    product_size = request.data.get('product_size', '')
    product_description = request.data.get('product_description', '')
    product_image = request.data.get('product_image')
    product_url = request.data.get('product_url')

    # Reference to the 'Kluret_Users' in Firebase
    ref = db.reference('All_Users/Kluret_Users')

    # Find the user by user_id
    users_snapshot = ref.get()
    matching_user = None

    for email_key, user_data in users_snapshot.items():
        if user_data.get('User-ID') == user_id:
            matching_user = email_key
            break

    if matching_user:
        # Create a new folder 'MyCart' under the user's node if it doesn't exist
        cart_ref = ref.child(f"{matching_user}/MyCart").push()  # Use push() to generate a unique key
        cart_ref.set({
            'product_name': product_name,
            'product_price': product_price,
            'product_color': product_color,
            'product_size': product_size,
            'product_description': product_description,
            'product_image': product_image,
            'product_url': product_url
        })

        return Response({"message": "Item added to cart successfully"}, status=201)
    else:
        return Response({"message": "User not found"}, status=404)

@api_view(['POST'])
def get_cart(request):
    # Extract the user_id from the request
    user_id = request.data.get('user_id')

    # Reference to the 'Kluret_Users' in Firebase
    ref = db.reference('All_Users/Kluret_Users')

    # Find the user by user_id
    users_snapshot = ref.get()
    matching_user = None

    for email_key, user_data in users_snapshot.items():
        if user_data.get('User-ID') == user_id:
            matching_user = email_key
            break

    if matching_user:
        # Reference to the 'MyCart' collection under the user's node
        cart_ref = ref.child(f"{matching_user}/MyCart")
        cart_items = cart_ref.get()

        if cart_items:
            # Convert the cart items to a list of dictionaries
            cart_list = []
            for key, value in cart_items.items():
                cart_list.append(value)

            return Response({"cart_items": cart_list}, status=200)
        else:
            return Response({"message": "Cart is empty"}, status=200)
    else:
        return Response({"message": "User not found"}, status=404)





@api_view(['POST'])
def remove_from_cart(request):
    # Extract the user_id and product_url from the request
    user_id = request.data.get('user_id')
    product_url = request.data.get('product_url')

    # Reference to the 'Kluret_Users' in Firebase
    ref = db.reference('All_Users/Kluret_Users')

    # Find the user by user_id
    users_snapshot = ref.get()
    matching_user = None

    for email_key, user_data in users_snapshot.items():
        if user_data.get('User-ID') == user_id:
            matching_user = email_key
            break

    if matching_user:
        # Reference to the 'MyCart' collection under the user's node
        cart_ref = ref.child(f"{matching_user}/MyCart")
        cart_items = cart_ref.get()

        if cart_items:
            item_to_remove = None
            for key, value in cart_items.items():
                if value.get('product_url') == product_url:
                    item_to_remove = key
                    break

            if item_to_remove:
                # Remove the item from the cart
                cart_ref.child(item_to_remove).delete()
                return Response({"message": "Item removed from cart successfully"}, status=200)
            else:
                return Response({"message": "Item not found in cart"}, status=404)
        else:
            return Response({"message": "Cart is empty"}, status=404)
    else:
        return Response({"message": "User not found"}, status=404)