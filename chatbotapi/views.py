# chatbotapi/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import openai
import re

# Set your OpenAI API key
openai.api_key = "sk-proj-Q1JLGoe7A3rRoZaqyUh9T3BlbkFJv7YuuWTvZccPiUAyp9Ji"

@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            user_input = data.get('user_input', '')
            user_history = data.get('user_history', '')

            prompt_tuning = f'''
                Your name is Kluret.
                You are Kluret, an advanced AI Search Engine in Sweden, capable of performing search engine tasks in Sweden only but for now you can assist users to find products online. In the future, you will be more powerful to find products on the Swedish internet since we are still working on the computer nodes network.
                Kluret was founded by Elias Luzwehimana in 2024 and is based in Stockholm, Sweden. Kluret Version 1 is set to be used under searching for products on the Swedish entire web. 
                As Kluret, you must engage in continuous, coherent conversation with the user, remembering the context and flow of the dialogue. Avoid repeating greetings or introductory phrases if the conversation has already started. Only greet the user if the user greets first.

                Here is the conversation history so far:
                {user_history}

                The user's last input was: "{user_input}"
                Respond appropriately to the user's last input, maintaining context and ensuring a smooth conversational experience.

                Pay close attention to details in the conversation. If the user expresses interest in buying something in the fashion category, understand the product they want and ask them for a specific price range if they don't provide one. If they provide a product name, include the product name in your response using the format ((product name)). If they provide a price range, include the price in the format [[price]]. Do not ask the user about brands or any technical details related to computer programming code.

                When you have found products that match the user's request, respond with the top 5 product information directly without stating that you are looking for it. Use the following format for each product: "Here is a product I found for you: ((product name)) for [[price]]. You can buy it [here]((product URL)). Description: ((product description))." Ensure to provide all product details in your response.

                Respond in HTML format without styling. Name all the anchor links' id as 'product-link'. Under the links, they shall have the valid URLs linked to the product page. Ensure the URLs are valid and accessible before including them in your response.
                in the html when you have a list of links use br*2 and i need then link to have target= _blank and remeber never forgot to include the links in <a href(here)>poruct name</a>
            
                previus mistakes you are not allowed to repeat
                [
                    1[
                        Sure! I have found some makeup products within your price range of 400kr. Here are the top 5 I recommend: 1. Here is a product I found for you: MAC Studio Fix Fluid Foundation for [360kr](https://www.macmakeup.se/product-link "MAC Studio Fix Fluid Foundation"). Description: A modern foundation that combines a natural matte finish and medium to full buildable coverage with broad spectrum SPF 15 protection.

                        2. Here is a product I found for you: Benefit They're Real Mascara for [375kr](https://www.benefitmakeup.se/product-link "Benefit They're Real Mascara"). Description: Lengthens, curls, volumizes, lifts and separates lashes for a spectacular "out-to-here!" look.
                        
                        3. Here is a product I found for you: Nars Blush in Orgasm for [395kr](https://www.narscosmetics.se/product-link "Nars Blush in Orgasm"). Description: Gives a sheer, natural hint of color made with transparent pigments for a soft and sheer look.
                        
                        4. Here is a product I found for you: Anastasia Beverly Hills Brow Wiz for [385kr](https://www.anastasiabeverlyhills.se/product-link "Anastasia Beverly Hills Brow Wiz"). Description: A pencil for outlining and highlighting brows.
                        
                        5. Here is a product I found for you: Urban Decay Naked2 Palette for [400kr](https://www.urbandecay.se/product-link "Urban Decay Naked2 Palette"). Description: Ranging from burnt orange and raspberry to shiny copper and bronze. This collection lets you achieve lots of neutral looks, smoky dramatic eyes, and everything in between.
                        
                        Each link will open up in a new tab for your convenience. Let me know if you need any further assistance.
                    ]
                ]


            '''

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

            # Parse the output text to find product details
            products = re.findall(r'Here is a product I found for you: \(\((.*?)\)\) for \[\[(.*?)\]\]\. You can buy it \[here\]\((.*?)\)\. Description: \(\((.*?)\)\)\.', output_text)

            additional_data = []
            for index, (product_name, product_price, product_url, product_description) in enumerate(products, start=1):
                additional_data.append({
                    'open': True,
                    'product': product_name,
                    'price': product_price,
                    'url': product_url,
                    'description': product_description,
                    'index': index
                })

            # Log the additional_data to the console
            print('AI Response additional_data:', additional_data)

            # Return the response as JSON with additional_data
            return JsonResponse({"response": output_text, "additional_data": additional_data})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
