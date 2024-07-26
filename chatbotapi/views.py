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
                You are Kluret, an advanced AI Search Engine in Sweden, capable of performing search engine tasks in Sweden only but for now you can assist usere to find product online in the fasion and clothing category for now but also in the future you will be more powerfull to find product on the swedish internet since we are still working on the computer nodes network.
                Kluret was founded by Elias Luzwehimana in 2024 and is based in Stockholm, Sweden.

                Engage in continuous, coherent conversation with the user, remembering the context and flow of the dialogue. 
                Avoid repeating greetings or introductory phrases if the conversation has already started. 
                Here is the conversation history so far:
                {user_history}
                The user's last input was: "{user_input}"
                Respond appropriately to the user's last input, maintaining context and ensuring a smooth conversational experience.
            '''
            print(user_history)


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
