from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import openai
import re

# Set your OpenAI API key
openai.api_key = "sk-proj-Q1JLGoe7A3rRoZaqyUh9T3BlbkFJv7YuuWTvZccPiUAyp9Ji"

product_data = [
    {
        "id": 1,
        "category": "Mobile_phones",
        "api": "https://webnodes-1ac3b80d6a1c.herokuapp.com/Mobile_phones/Mobile_phones",
        "indexes": {
            "start": 1,
            "end": 10515
        }
    },
    {
        "id": 2,
        "category": "Mobile_phone_case",
        "api": "https://webnodes-1ac3b80d6a1c.herokuapp.com/Mobile_phone_case/Mobile_phone_case",
        "indexes": {
            "start": 1,
            "end": 16000
        }
    },
    {
        "id": 3,
        "category": "Camera_Phone_Accessories",
        "api": "https://webnodes-1ac3b80d6a1c.herokuapp.com/Camera_Phone_Accessories/Camera_Phone_Accessories",
        "indexes": {
            "start": 1,
            "end": 263
        }
    }
]

@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            user_input = data.get('user_input', '')
            user_history = data.get('user_history', '')

            # Print the received data for debugging
            print("Received user input:", user_input)
            print("Received user history:", user_history)

            # Define product categories
            product_categories = ", ".join([category["category"] for category in product_data])

            prompt_tuning = f'''
                Your name is Kluret.
                You are Kluret, an advanced AI Search Engine in Sweden, capable of performing search engine tasks in Sweden only but for now you can assist users to find products online. In the future, you will be more powerful to find products on the Swedish internet since we are still working on the computer nodes network.
                Kluret was founded by Elias Luzwehimana in 2024 and is based in Stockholm, Sweden. Kluret Version 1 is set to be used under searching for products on the Swedish entire web.

                As Kluret, you must engage in continuous, coherent conversation with the user, remembering the context and flow of the dialogue. Avoid repeating greetings or introductory phrases if the conversation has already started. Only greet the user if the user greets first.

                Here is the conversation history so far:
                {user_history}

                The user's last input was: "{user_input}"
                Respond appropriately to the user's last input, maintaining context and ensuring a smooth conversational experience.

                Pay close attention to details in the conversation. If the user expresses interest in buying something, understand the product they want and identify the appropriate category from these options: all product that can be bougt online like eccommerce products. 

                - If the user specifies a product name, respond directly with information about that product, including its category. Use the format ((product name)) for the product and [[category]] for the category.
                - If the user specifies a price range, acknowledge it but do not ask for further details unless necessary.
                - If the product name is clear, do not ask for additional details like features, storage capacity, or brand preferences unless explicitly mentioned by the user.

                Example responses:
                - If the user says "I want to buy an iPhone 13": "You are looking for an ((iPhone 13)) in the [[Mobile_phones]] category."
                - If the user says "I am looking for a black iPhone 13 around 7000kr": "You are looking for a black ((iPhone 13)) around 7000kr in the [[Mobile_phones]] category."

                Avoid these mistakes:
                - Do not ask for storage capacity, features, or specific brand preferences unless the user mentions them.
                - Do not greet the user multiple times in the same conversation.
                - Do not ask for clarification on details that the user has already provided clearly.

                Focus on:
                - Providing clear and concise responses.
                - Identifying the product name and category correctly.
                - Setting the 'open' attribute to True if the product is found.

                The user's last input was about finding a product. Your response should focus on confirming the product and its category. Here is an example of how you should structure your responses:

                - User input: "I am looking for a black iPhone 13 around 7000kr."
                - Correct response: "You are looking for a black ((iPhone 13)) around 7000kr in the [[Mobile_phones]] category."

                If a product name is provided:
                - Confirm the product name and category in your response.
                - Include the product name using ((product name)).
                - Include the category using [[category]].

                If the product is found, return the product details and set 'open' to True in the response.

                Additional instructions:
                - Always provide the product name and category in the response.
                - Do not repeat greetings or introductory phrases if the conversation has already started.
                - Maintain a coherent and contextually appropriate dialogue.

                If the user expresses interest in a product and you identify the product name and category, set 'open' to True. Your response should be informative and focused on the product the user wants to buy.

                Do not ask about:
                - Storage capacities.
                - Additional features.
                - Brand preferences.

                Only ask for clarification if the product name is unclear or ambiguous.

                Remember, your goal is to assist the user in finding products online and to provide accurate and relevant information based on their input.
            '''

            # Indicate that the API call is being made
            print("Making API call to OpenAI...")

            # Create the completion using GPT-4
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompt_tuning},
                    {"role": "user", "content": user_input},
                ]
            )

            # Extract output text from response
            output_text = response["choices"][0]["message"]["content"]

            # Print the response from OpenAI for debugging
            print('AI Response output_text:', output_text)

            # Extract product category and name from the response
            product_info = re.search(r'\(\((.*?)\)\)', output_text)
            category_info = re.search(r'\[\[(.*?)\]\]', output_text)

            product_name = product_info.group(1) if product_info else 'Unknown'
            product_category = category_info.group(1) if category_info else 'Unknown'

            # Find the API endpoint for the product category
            api_endpoint = None
            start_index = None
            end_index = None
            for category in product_data:
                if category['category'] == product_category:
                    api_endpoint = category['api']
                    start_index = category['indexes']['start']
                    end_index = category['indexes']['end']

            # Initialize additional_data with 'open' set to False
            additional_data = {
                'category': product_category,
                'product': product_name,
                'open': False,
                'api_endpoint': api_endpoint,
                'start': start_index,
                'end': end_index
            }

            # Check if product name is found
            if product_name != 'Unknown':
                additional_data['open'] = True

            # Log the extracted product info for debugging
            print('Extracted product info:', product_name, product_category)

            # Return the response as JSON with additional_data
            return JsonResponse({"response": output_text, "additional_data": additional_data})

        except Exception as e:
            print("Exception occurred:", e)  # Print exception details for debugging
            return JsonResponse({"error": str(e)}, status=500)

    else:
        print("Request method is not POST")  # Indicate incorrect request method
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
