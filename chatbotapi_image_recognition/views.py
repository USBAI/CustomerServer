from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
import random
import string
import base64
from groq import Groq
import firebase_admin
from firebase_admin import credentials, db
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Initialize the Groq client with your API key
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Initialize Firebase Admin SDK for the second Realtime Database
FIREBASE_CREDENTIALS_FOR_TASK_PATH = os.getenv('FIREBASE_CREDENTIALS_FOR_TASK_PATH')  # Assuming you have set the path in the environment

try:
    cred_task = credentials.Certificate(FIREBASE_CREDENTIALS_FOR_TASK_PATH)
    firebase_admin.initialize_app(cred_task, {
        'databaseURL': 'https://bolagdb-c40e2-default-rtdb.europe-west1.firebasedatabase.app/',
        'storageBucket': 'bolagdb-c40e2.appspot.com'
    }, name='bolagdb')
except FileNotFoundError as e:
    print(f"Firebase credentials file for tasks not found: {e}")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK for tasks: {str(e)}")

def encode_image_to_base64(image_path):
    """
    Encodes the image at the specified path to a Base64 string.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        try:
            # Initialize variables
            user_input = ''
            user_history = ''
            user_id = ''
            image_path = None

            # Check if the request contains files (multipart/form-data)
            if 'image' in request.FILES:
                image_file = request.FILES['image']  # Access the uploaded image
                print(image_file)
                image_path = handle_uploaded_file(image_file)  # Save and retrieve the path of the uploaded image
                user_input = request.POST.get('user_input', '')  # Extract additional fields from POST data
                user_history = request.POST.get('user_history', '')
                user_id = request.POST.get('user_id', '')
            else:
                # Parse JSON data from the request body
                data = json.loads(request.body.decode('utf-8'))
                user_input = data.get('user_input', '')
                user_history = data.get('user_history', '')
                user_id = data.get('user_id', '')

            # Validate input
            if not image_path:
                return JsonResponse({"error": "Image file is required"}, status=400)

            # Convert image to Base64
            base64_image = encode_image_to_base64(image_path)

            # Combine system prompt into the user message
            prompt_tuning = f'''
                Your name is Kluret.
                You are Kluret, an advanced AI capable of assisting users in analyzing images and finding products online. Your focus is on helping users by interpreting visual data and identifying products.

                Here is the conversation history so far:
                {user_history}

                The user's last input was: "{user_input}"

                Instructions:
                1. First, analyze the image to identify its content or describe what it shows.
                2. If the image contains a product, provide its name in the format ((product name)).
                3. If the user specifies a price range, acknowledge it and add the price using <<price number>> without the currency symbol.
                4. Provide concise responses, including the product name and price if available.
                5. Avoid repeating greetings or unnecessary clarifications if the user has already provided clear details.

                Example responses:
                - If the user says "What is in this image?": Identify the image content, e.g., "This is an image of ((Nike running shoes))."
                - If the user says "I want to buy an iPhone 13 for 7000kr": Respond with "I found ((iPhone 13)) <<7000>>."

                Remember to use a natural, conversational tone and the same language as the user's input.
                If the user asks about Kluret's internal functionality, respond with: "I'm sorry, I can't help you with that."

                i want you to make sure that you return the product name from the image and also the price if the user want you to include it
            '''

            print("Making API call to Groq...")

            # Send the Base64 image and text prompt to the Groq API
            chat_completion = client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_tuning + f"\n\nUser: {user_input}"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                },
                            },
                        ],
                    }
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )

            # Process the response
            output_text = chat_completion.choices[0].message.content
            print("AI Response:", output_text)

            # Extract product details using regex
            product_info = re.search(r'\(\((.*?)\)\)', output_text)
            price_info = re.search(r'<<(\d+(\.\d+)?)>>', output_text)

            product_name = product_info.group(1) if product_info else None
            product_price = price_info.group(1) if price_info else None

            additional_data = {
                'product': product_name or 'Unknown',
                'price': product_price or 'Unknown',
                'open': bool(product_name),
                'pricing': bool(product_price)
            }

            # Append "View Product" button if a product is found
            if product_name:
                additional_data['view_button'] = f"<button>View {product_name}</button>"

            # Update user history
            cleaned_output_text = re.sub(r'\(\(.*?\)\)', lambda m: m.group(0).strip('()'), output_text)
            cleaned_output_text = re.sub(r'<<.*?>>', lambda m: m.group(0).strip('<<>>'), cleaned_output_text)
            updated_user_history = f"{user_history}\nUser: {user_input}\nAI: {cleaned_output_text.strip()}"

            # Save chat history to Firebase Realtime Database
            app = firebase_admin.get_app('bolagdb')
            ref = db.reference(f'Bolag_Kluret/Chat_History/{user_id}', app=app)
            ref.push({
                'user_input': user_input,
                'ai_response': cleaned_output_text.strip(),
                'history': updated_user_history,
                'product': product_name,
                'price': product_price
            })

            # Return the final response
            return JsonResponse({
                "response": cleaned_output_text.strip(),
                "additional_data": additional_data,
                "updated_user_history": updated_user_history
            })

        except Exception as e:
            print("Exception occurred:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


def handle_uploaded_file(image_file):
    """
    Handles the uploaded image file and returns the file path.
    Saves the file temporarily with a randomly generated name.
    """
    # Generate a random filename with length between 20 and 100
    random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(20, 100))) + os.path.splitext(image_file.name)[1]

    # Save the image to a temporary file
    file_path = default_storage.save(f'temp/{random_filename}', ContentFile(image_file.read()))
    return default_storage.path(file_path)

@csrf_exempt
def get_chat_history(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id', '')  # Get the user_id from the request query parameter

            if not user_id:
                return JsonResponse({"error": "user_id is required"}, status=400)

            app = firebase_admin.get_app('bolagdb')
            ref = db.reference(f'Bolag_Kluret/Chat_History/{user_id}', app=app)

            chat_history = ref.get()

            if not chat_history:
                return JsonResponse({"status": "failed", "message": "No chat history found for this user"}, status=404)

            return JsonResponse({"status": "success", "chat_history": chat_history})

        except Exception as e:
            return JsonResponse({"status": "failed", "message": str(e)}, status=500)

    return JsonResponse({"status": "failed", "message": "Only GET requests are allowed for fetching chat history"}, status=405)
