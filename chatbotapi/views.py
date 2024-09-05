from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
from groq import Groq

# Initialize the Groq client with your API key
API_KEY = "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"
client = Groq(api_key=API_KEY)

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

            # Construct the prompt to include user history
            prompt_tuning = f'''
                Your name is Kluret.
                You are Kluret, an advanced AI Search Engine in Sweden, capable of performing search engine tasks in Sweden only but for now you can assist users to find products online. In the future, you will be more powerful to find products on the Swedish internet since we are still working on the computer nodes network.
                Kluret was founded by Elias Luzwehimana in 2024 and is based in Stockholm, Sweden. Kluret Version 1 is set to be used under searching for products on the Swedish entire web.

                As Kluret, you must engage in continuous, coherent conversation with the user, remembering the context and flow of the dialogue. Avoid repeating greetings or introductory phrases if the conversation has already started. Only greet the user if the user greets first.

                Here is the conversation history so far:
                {user_history}

                The user's last input was: "{user_input}"
                Respond appropriately to the user's last input, maintaining context and ensuring a smooth conversational experience.

                Pay close attention to details in the conversation. If the user expresses interest in buying something, understand the product they want and identify the appropriate : all product that can be bought online like e-commerce products. 

                - If the user specifies a product name, respond directly with information about that product,. Use the format ((product name)).
                - If the user specifies a price range, acknowledge it but do not ask for further details unless necessary.
                - If the product name is clear, do not ask for additional details like features, storage capacity, or brand preferences unless explicitly mentioned by the user.

                Example responses:
                - If the user says "I want to buy an iPhone 13": you can mix up the producct name with some message the user to know that you found the product "((iPhone 13))"
                - If the user says "I am looking for a black iPhone 13 around 7000kr": you can mix up the producct name with some message the user to know that you found the product"((iPhone 13)) then tell them to click on the view botton and use an emoju shoing down or an arrow pointing down where they shall click to view the products remober not this  → it shall point down you can use any emoji or pointer to poin down but not always make sure when you tell the user that you found the product tthen it shall be in ((the product name in here))"

                Avoid these mistakes:
                - Do not ask for storage capacity, features, or specific brand preferences unless the user mentions them.
                - Do not greet the user multiple times in the same conversation.
                - Do not ask for clarification on details that the user has already provided clearly.

                Focus on:
                - Providing clear and concise responses.
                - Identifying the product name   correctly.
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
                Also, respond in a natural, conversational tone.
            '''

            # Indicate that the API call is being made
            print("Making API call to Groq...")

            # Create the completion using Groq
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": prompt_tuning},
                    {"role": "user", "content": user_input},
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=True,
                stop=None,
            )

            # Collect and print the streaming response
            output_text = ""
            for chunk in completion:
                output_text += chunk.choices[0].delta.content or ""
            print('AI Response output_text:', output_text)

            # Extract product category and name from the response
            product_info = re.search(r'\(\((.*?)\)\)', output_text)
            category_info = re.search(r'\[\[(.*?)\]\]', output_text)

            product_name = product_info.group(1) if product_info else None
            product_category = category_info.group(1) if category_info else None

            # Initialize additional_data with 'open' set to False
            additional_data = {
                'category': product_category or 'Unknown',
                'product': product_name or 'Unknown',
                'open': False
            }

            # Check if product name is found
            if product_name:
                additional_data['open'] = True

            # Clean up the response text by removing special formatting
            cleaned_output_text = re.sub(r'\(\(.*?\)\)', lambda m: m.group(0).strip('()'), output_text)
            cleaned_output_text = re.sub(r'\[\[.*?\]\]', lambda m: m.group(0).strip('[]'), cleaned_output_text)
            cleaned_output_text = cleaned_output_text.replace('(( ', '').replace(' ))', '')
            cleaned_output_text = cleaned_output_text.replace('[[ ', '').replace(' ]]', '')

            # Log the extracted product info for debugging
            print('Extracted product info:', product_name, product_category)
            print('Cleaned AI Response:', cleaned_output_text)

            # Update the user history with the latest response
            updated_user_history = f"{user_history}\nUser: {user_input}\nAI: {cleaned_output_text.strip()}"

            # Return the response as JSON with additional_data and updated_user_history
            return JsonResponse({
                "response": cleaned_output_text.strip(),
                "additional_data": additional_data,
                "updated_user_history": updated_user_history
            })

        except Exception as e:
            print("Exception occurred:", e)  # Print exception details for debugging
            return JsonResponse({"error": str(e)}, status=500)

    else:
        print("Request method is not POST")  # Indicate incorrect request method
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
