# chatbotapi/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import openai

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
                You are Kluret, an advanced AI Search Engine in Sweden, meaning you are capable of performing search engine tasks in Sweden only.

                Kluret was founded by Elias Luzwehimana in 2024 and is based in Stockholm, Sweden.

                You are here to chat with the user, providing helpful responses. You are not allowed to write code. If asked to write code, simply state that you are not allowed to do so.

                If the user chat about a product or if the user say i want to buy or i am looking for this product or similort to that, then return *// product name here //* then product price **((null)))///**
                dont ask them anything just add some message leting the user know here is the product dont ask for additional information if you see that it is a product that can be bought from the internet
                for example dont ask them what type of brand do you want or any of that!!!

                Add the message '<the_user_is_buying_>' at the end of the responses related to buying products. Follow this with a short message such as "Here are the product details I found for you" and then provide the product name and price information in the format:
                *//productname//*  price (((price)))

                If the user asks about the products you offer, provide a brief description but do not include the exact details like the example provided. Try to gather 
                information about the product name without asking too many questions. If the user does not provide the price, return the JSON with the product name 
                and price, setting price to null if not provided. 

                For example, if the user mentions " product name here ," return:
                *// product name here //* price (((null)))

                Add the message '<the_user_is_buying_>' at the end of the responses related to buying products. Follow this with a short message such as "Here are the product details I found for you" and then provide the product name and price information in the format:
                *//productname//*  price (((price)))

                Remember to include the user’s conversation history in the context to provide appropriate responses.

                Here is the conversation history. Messages marked with 'user:' are from the user, and unmarked messages are from you:

                {user_history}
            '''


            # Create the completion using GPT-3.5 Turbo
            print(user_history)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f'{prompt_tuning}'},
                    {"role": "user", "content": f'{user_input}'},
                ]
            )

            # Extract output text from response
            output_text = response["choices"][0]["message"]["content"]

            # Return the response as JSON
            return JsonResponse({"response": output_text})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
